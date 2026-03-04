from tables import create_tables, students
from crud_operations import create_student, display_student, update_student, delete_student
from sqlalchemy import Delete, Select


# creating students table
create_tables()

# Inserting 3 students records to the table
create_student('Abhishek',32, 'Hyderabad')
create_student('Rahul',27, 'Chennai')
create_student('Chirag',18, 'Bangalore')

# Fetch all students records
display_student()

# # Update city of student whone name='Rahul'
update_student('Delhi')

#Delete student whose age is less than 20
delete_student()

