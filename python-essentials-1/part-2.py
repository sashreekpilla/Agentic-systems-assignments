try:
    first_Name= input()
    last_Name= input()
    cur_age=int(input())
    if cur_age <= 0:
        raise ValueError ("Age cannot be Negative")
    fut_age=  cur_age+1
    print ("Full Name:" + first_Name +" "+ last_Name)
    print ("You will be "+str(fut_age)+" next year")
except ValueError:
    print ("Invalid age input")
