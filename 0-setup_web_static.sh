#!/bin/bash

# Colors for formatting output
red='\e[0;31m'
brown='\e[0;33m'
green='\e[1;32m'
blue='\e[1;34m'
reset='\033[0m'

# Function to install packages
function install() {
    if command -v "$1" &> /dev/null ; then
        echo -e "    ${green}${1} is already installed.${reset}\n"
    else
        echo -e "    Installing: ${brown}$1${reset}\n"
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
        echo -e "    Directory already exists: $directory"
    fi
}

# Function to create html file
function create_html_file() {
    local file_path="/data/web_static/releases/test/index.html"
    local content="<html><body><h1>This is a fake HTML file.</h1></body></html>"
    echo "$content" > "$file_path"
}

# Function for updating nginx config
function update_nginx_config() {
    local config_file="/etc/nginx/sites-available/default"

    # Backup the current configuration file if backup doesn't exist
    if [ ! -f "${config_file}.backup" ]; then
        sudo cp "$config_file" "${config_file}.backup"
        echo -e "    Backed up the current configuration file to ${config_file}.backup"
    fi

    # Remove any existing configuration for serving hbnb_static
    sudo sed -i '/location \/hbnb_static {/,/}/d' "$config_file"

    # Add new configuration for serving hbnb_static using alias
    sudo sed -i '/server {/a \
        location /hbnb_static {\
            alias /data/web_static/current/;\
        }' "$config_file"
}

# Function to restart nginx service.
function restart_nginx() {
    sudo service nginx restart
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

# Error handling function
function handle_error() {
    local exit_code="$1"
    local error_message="$2"
    echo -e "${red}Error: ${error_message}${reset}"
    exit "$exit_code"
}

echo -e "${blue}Setting up your web server & doing some minor checks...${reset}\n"

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

echo -e "\n${blue}Updating Nginx configuration.${reset}\n"

# Update Nginx configuration
update_nginx_config || handle_error 1 "Failed to update Nginx configuration"

# Restart Nginx
restart_nginx || handle_error 1 "Failed to restart Nginx"

# Successful exit
exit 0
