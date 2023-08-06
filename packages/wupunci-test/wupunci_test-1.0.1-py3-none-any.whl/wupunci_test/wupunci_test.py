def print_lol2(the_list,level=0):
    """这个函数有两个参数，一个是任何python列表
    一个是参数level，用来遇到嵌套列表时插入制表符"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol2(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
            #这又是注释

