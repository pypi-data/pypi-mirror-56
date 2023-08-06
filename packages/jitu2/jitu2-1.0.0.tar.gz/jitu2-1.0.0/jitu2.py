def fun(the_list) :
    for each_list in the_list :
        if isinstance(each_list,list):
            fun(each_list)
        else :
            print(each_list)

            
            
  
