#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

# Colors for formatting output
red='\e[0;31m'
brown='\e[0;33m'
green='\e[1;32m'
blue='\e[1;34m'
reset='\033[0m'

# Function to install packages
function install() {
    if command -v "$1" &> /dev/null ; then
        echo -e "    ${green}Package already installed: ${brown}${1}${reset}"
    else
        echo -e "    Installing: ${brown}$1${reset}"
        sudo apt-get update -y -qq && sudo apt-get install -y "$1" -qq
        echo -e "\n"
    fi
}

# Function to create directories
function create_directory() {
    local directory="$1"

    if [ ! -d "$directory" ]; then
        mkdir -p "$directory"
    else
        echo -e "    ${green}Directory already exists: ${brown}$directory${reset}"
    fi
}

# Function to create html file
function create_html_file() {
    local file_path="/data/web_static/releases/test/index.html"
    local content="<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>"
    echo -e "$content" > "$file_path"
}

# Function to Check/Update /data/ ownership.
function check_owner() {
    local owner=$(stat -c "%U" "/data/")
    local group=$(stat -c "%G" "/data/")
    local expected_owner="ubuntu"
    local expected_group="ubuntu"

    if [ "$owner" != "$expected_owner" ] || [ "$group" != "$expected_group" ]; then
        echo -e "    ${brown}Changing ownership of /data/ to ubuntu:ubuntu...${reset}"
        sudo chown -R ubuntu:ubuntu /data/ || handle_error 1 "Failed to change ownership of /data/"
    else
        echo -e "    ${green}Ownership of /data/ is already set: ${brown}ubuntu:ubuntu.${reset}"
    fi
}

# Function for updating nginx config
function update_nginx_config() {
    local config_file="/etc/nginx/sites-available/default"

    # Backup the current configuration file if backup doesn't exist
    if [ ! -f "${config_file}.backup" ]; then
        sudo cp "$config_file" "${config_file}.backup"
        echo -e "    Backed up the current configuration file to ${brown}${config_file}.backup${reset}"
    fi

    # Remove any existing configuration for serving hbnb_static
    sudo sed -i '/location \/hbnb_static {/,/}/d' "$config_file"

    # Add new configuration for serving hbnb_static using alias
    sudo sed -i '/server_name _;/a \
        location /hbnb_static {\
            alias /data/web_static/current/;\
        }' "$config_file"
}

# Function to restart nginx service.
function restart_nginx() {
    sudo service nginx restart
}


# Error handling function
function handle_error() {
    local exit_code="$1"
    local error_message="$2"
    echo -e "${red}Error: ${error_message}${reset}"
    exit "$exit_code"
}

# Array of packages to install
packages=(
    "nginx"
)

# Array of directories to create
directories=(
    "/data/"
    "/data/web_static/"
    "/data/web_static/releases/"
    "/data/web_static/shared/"
    "/data/web_static/releases/test/"
)

echo -e "${blue}Setting up your web server & doing some minor checks...${reset}"

# Install packages
for package in "${packages[@]}"; do
    install "$package" || handle_error 1 "Failed to install package: $package"
done

# Create the directories
for directory in "${directories[@]}"; do
    create_directory "$directory" || handle_error 1 "Failed to create directory: $directory"
done

# Create the fake HTML file
create_html_file || handle_error 1 "Failed to create HTML file"

# Create or recreate the symbolic link
symbolic_link="/data/web_static/current"
if [ -L "$symbolic_link" ]; then
    rm "$symbolic_link"
fi
ln -s "/data/web_static/releases/test/" "$symbolic_link"

# Check and update ownership of /data/ to ``ubuntu``
check_owner

echo -e "${blue}Updating Nginx configuration.${reset}"

# Update Nginx configuration
update_nginx_config || handle_error 1 "Failed to update Nginx configuration"

# Restart Nginx
restart_nginx || handle_error 1 "Failed to restart Nginx"

echo -e "${blue}Setting up Done!${reset}"
# Successful exit
exit 0
