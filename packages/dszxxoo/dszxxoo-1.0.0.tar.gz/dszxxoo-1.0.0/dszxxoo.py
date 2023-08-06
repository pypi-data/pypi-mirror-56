

def print_list(l):
    
    for i in l:
        if isinstance(i,list):
            print_list(i)
        else:
            print(i)

