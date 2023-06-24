#!/usr/bin/python3
"""Defines class 'HBNBCommand' """

import cmd
import models

from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Defines a command-line interpreter based on ``cmd.Cmd`` """

    prompt = "(hbnb) "
    __class_list = ['BaseModel', 'Amenity', 'City',
                    'Place', 'Review', 'State', 'User']

    def emptyline(self, line=''):
        """Ignore empty lines """
        pass

    def do_EOF(self, line=''):
        """Send ``EOF`` signal, exiting the console """
        print()
        return True

    def do_quit(self, line=''):
        """
        Quit program

        Usage: quit
        """
        return self.do_EOF()

    def do_create(self, line=''):
        """
        Create and save a new class instance

        Usage: create <class name> [`<attribute_key>`="<attribute_value>" ...]

        Ex:
        (hbnb) create BaseModel
        """
        arg = line.split()
        if len(arg) == 0:
            print("** class name missing **")
        else:
            cls_name = arg[0]
            if cls_name not in self.__class_list:
                print("** class doesn't exist **")
            else:
                try:
                    obj = eval(cls_name)()
                    if arg[1:]:
                        for param in arg[1:]:
                            if '=' in param:
                                key, value = param.split('=')
                                key = key.strip()
                                value = value.strip()
                                # Handle string values
                                if value.startswith('"') and\
                                        value.endswith('"'):
                                    value = value[1:-1].replace('\\"', '"')\
                                            .replace('_', ' ')

                                # Handle float values
                                elif "." in value:
                                    try:
                                        value = float(value)
                                    except ValueError:
                                        continue  # Skip invalid value

                                # Handle integer values
                                else:
                                    try:
                                        value = int(value)
                                    except ValueError:
                                        continue
                                setattr(obj, key, value)
                    obj.save()
                    print(obj.id)
                except Exception as e:
                    print(f"{e}")

    def do_show(self, line):
        """
        Print a description of an instance based on the class name

        Usage: show <class name> <id>

        Ex:
        (hbnb) show BaseModel 1234-1234-1234
        """
        args = line.split()
        obj_dict = models.storage.all()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__class_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            obj_dict = models.storage.all()
            obj_key = "{}.{}".format(args[0], args[1])
            obj = obj_dict.get(obj_key, None)
            if obj is None:
                print("** no instance found **")
            else:
                print(obj)

    def do_destroy(self, line=''):
        """
        Delete an instance based on the class name and id

        Usage: destroy <class name> <id>

        Ex:
        (hbnb) destroy BaseModel 1234-1234-1234
        """

        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__class_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            obj_dict = models.storage.all()
            obj_key = "{}.{}".format(args[0], args[1])
            obj = obj_dict.get(obj_key, None)
            if obj is None:
                print("** no instance found **")
            else:
                try:
                    del obj_dict[obj_key]
                    models.storage.save()
                except Exception as e:
                    print(e)

    def do_all(self, line=''):
        """
        Print decriptions of all objects of all classes or a specific class
        if the second argument is supplied

        Usage: all [<class name>]

        Ex:
        (hbnb) all
        (hbnb) all BaseModel
        """

        args = line.split()
        all_list = []
        obj_dict = models.storage.all()
        if args and args[0] not in self.__class_list:
            print("** class doesn't exist **")
            return
        elif not args:
            for key, value in obj_dict.items():
                all_list.append(value.__str__())
        else:
            for key, value in obj_dict.items():
                if key.split('.')[0] == args[0]:
                    all_list.append(value.__str__())
        print(all_list)

    def do_update(self, line=''):
        """
        Update an object based on the class name and id

        Usage: update <class name> <id> <attribute name> "<attribute value>"

        Ex:
        (hbnb) update BaseModel 1234-1234-1234 email "airbnb@mail.com"
        """
        args = line.split()
        obj_dict = models.storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__class_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            key = '.'.join(args[:2])
            setattr(obj_dict[key], args[2], args[3])
            models.storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
