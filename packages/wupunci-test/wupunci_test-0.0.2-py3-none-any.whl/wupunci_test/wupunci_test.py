def print_lol(the_list,level):
    """这个函数有两个参数，一个是任何python列表
    一个是参数level，用来遇到嵌套列表时插入制表符"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
            #这又是注释
