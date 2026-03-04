from db import engine
from tables import students
from sqlalchemy import insert, delete, update, select


# Create Student row
def create_student(input_name: str, input_age: int, input_city: str):

    with engine.connect() as conn:
        
        query = insert(students).values(name=input_name, age=input_age ,city=input_city)
        conn.execute(query)
        conn.commit()



#Display all student details
def display_student():

    with engine.connect() as conn:

        query= select(students) 
        result=conn.execute(query)
        conn.commit()
    for row in result:
        print(row)


#Update city for student whose name is "Rahul"
def update_student(input_city: str):

    with engine.connect() as conn:
        query= update(students).where(students.c.name=='Rahul').values(city=input_city)
        conn.execute(query)
        conn.commit()
    
    
    
#Delete student record where the age is less than 20
def delete_student():

    with engine.connect() as conn:
        query = delete(students).where(students.c.age<20)
        conn.execute(query)
        conn.commit()






    

