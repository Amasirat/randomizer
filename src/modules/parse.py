# core functionality of the program
from . import core
# to display help message
from . import help
# for path and directory management
import os

# function for add-group arg
def arg_add_group(arg):
    groupname = arg
    try:
        core.create_group(groupname)
    except FileExistsError:
        print("group already exists")
    else:
        print(f"group {groupname} has been created...")

# function for delete-group arg
def arg_delete_group(arg):
    groupname = arg
    dir = f"{core.GROUP_DIR}{groupname}.csv"
    if not os.path.isfile(dir):
        raise FileNotFoundError
    
    print(f"Are you sure you want to delete group '{arg}'?")
    while True:
        usr_input = input("Deleting this group will also delete all its elements[y/n]:")
        usr_input.lower().rstrip()

        match usr_input:
            case 'y':
                os.remove(dir)
                print("group successfuly deleted")
                return
            case 'n':
                return
            case _:
                print("invalid input, try again")

#function for add-elements arg
def arg_add_elements(args : list):
    group = args[0]
    group_dir = f"{core.GROUP_DIR}{group}.csv"
    if not os.path.isfile(group_dir):
        raise FileNotFoundError
    for element in args[1:]:
        core.append_element(element, group)
    print(f"Elements added to {group}")

# function for random-pull operation
def arg_pull_random(group : str, loop_count : int):
    element_ids = set() # empty set that contains random id numbers
    
    if loop_count >= core.row_counter(group):
        print("This group is not great enough to get this many random elements from it")
        return
    
    count = 0 # loop counter
    while(count < loop_count):
        id = core.random_pull(group)
        if id in element_ids:
            loop_count += 1 
        else:
            element_ids.add(id)
        count += 1
        
    for id in element_ids:
        print(f"*{core.access_element(group, id)}")
# parses arguments recieved as input
def parser(arguments : list):
    if len(arguments) <= 0:
        raise IndexError # meaning list is of invalid length
    match arguments[0]:
        case "add-group":
            if len(arguments) != 2:
                raise IndexError
            else:
                arg_add_group(arguments[1])
        case "add-elements":
            if len(arguments) < 2:
                raise IndexError
            arg_add_elements(arguments[1:])
        case "show-groups":
            if len(arguments) > 1:
                raise IndexError
            else:
                groups = core.return_groups()
                for item in groups:
                    group, _ =  item.split('.')
                    print(f"--{group}")
        case "show-elements":
            if len(arguments) != 2:
                raise IndexError
            core.show_elements(arguments[1])
        case "delete-group":
            if len(arguments) != 2:
                raise IndexError
            else:
                arg_delete_group(arguments[1])
        case "delete-element":
            pass
        case "pull-random":
            if len(arguments) != 3:
                raise IndexError
            arg_pull_random(arguments[1], int(arguments[2]))
        case _:
            help.help()