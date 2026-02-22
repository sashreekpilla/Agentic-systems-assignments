class StudentMarks:
    def __init__(self, marks):
        self.marks = marks

    def last_three_avg(self):
        try:
            if len(self.marks) < 3:
                raise IndexError()
        

            last_three = self.marks[-3:]
            total = sum(last_three)
            avg = total / 3
            print("The average of the last three marks is: "+str(avg))

        except IndexError:
            print("Not enough marks to calculate average")


marks1 = [90, 85, 45, 86, 98, 15]
student1 = StudentMarks(marks1)
student1.last_three_avg()

marks2 = [50, 60]
student2 = StudentMarks(marks2)
student2.last_three_avg()