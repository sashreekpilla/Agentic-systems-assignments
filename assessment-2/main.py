
from typing import List

# class Student(BaseModel):
#     name: str
#     experience_years: float
#     skills: List[str]
#     has_degree: bool

# students: List[Student]=[]


# def validate_and_score_resumes(students:List[Student]):
#     for i in students:
#         if i.experience_years < 0 or i.skills == None or i.name == None :
#             print ("Not suitable candidate")
#         else:
#             if i.has_degree=="True":
#                 bonus= bonus+ 20

        

def validate_and_score_resumes(Applicant):

    #selected candidates
    candidate=[]

    for i in Applicant:
        name= i.get('name')
        experience= i.get('experience_years')
        skills= i.get('skills')
        degree=i.get('has_degree')
    
        if experience<0 or skills==None:
            continue

        if type(name)!= str or len(name)==0:
            continue


        # score variable to score individual candidate
        score= experience* 10
        score= score + (len(skills)*5)
        if degree ==True:
            score= score + 20
    
        # appending the selected candidate to selected candidate list
        candidate.append((name,score))

    #sorting candidate table in descending order
    candidate.sort(key=lambda x:x[1], reverse=True)
    return candidate




# input
Applicant=[
  {'name': 'Alice', 'experience_years': 5, 'skills': ['Python', 'SQL'], 'has_degree': True},
  {'name': 'Bob', 'experience_years': -1, 'skills': ['Java'], 'has_degree': False},
  {'name': 'Carol', 'experience_years': 3, 'skills': [], 'has_degree': False},
  {'name': 'Dave', 'experience_years': 7, 'skills': ['Python', 'ML', 'SQL'], 'has_degree': False},
]

# function call
result =validate_and_score_resumes(Applicant)
print (result)


    


