def print_lol(this_list, indent=False, level=0):
    for each_item in this_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
#python3语法                print("\t", end='')
                    print " ",
            print(each_item)
