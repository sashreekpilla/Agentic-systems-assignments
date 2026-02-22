try:
    a=int (input())
    b=int (input())
    sum=a+b
    div=a/b
    print(sum)
    print(div)
except ValueError:
    print("Invlaid input")
except ZeroDivisionError:
    print("Cannot divide by zero")