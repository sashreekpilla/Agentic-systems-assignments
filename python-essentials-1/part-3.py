try:
    name= input()
    age= int(input())

    print("Hello "+name)

    while age<=0:
        raise ValueError("Age cannot be negative")

    if age<13:
        print("You are a Child")
    elif 13<=age and age<=17:
        print("You are a Teenager")
    elif 18<=age and age<=59:
        print("You are an Adult")
    else:
        print("You are a Senior Citizen")

    if age>=18:
        print("You are eligible to vote")
    else:
        print("You are not eligible to vote")

except ValueError:
    print("Invalid age input")
