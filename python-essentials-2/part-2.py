class StudentScores:
    def __init__(self, scores):
        self.scores=scores

    def highest_last_two(self):
        try:
            if len(self.scores)<2 :
                raise IndexError
            
            last_two=self.scores[-2:]
            
            if last_two[0]> last_two[1]:
                print("Highest score among last two is: "+ str(last_two[0]))
            else:
                print("Highest score among last two is: "+ str(last_two[1]))

            
        except IndexError:
            print("Not enough scores to find highest value")

scores1 = [90, 85, 45, 86, 98, 15]
student1 = StudentScores(scores1)
student1.highest_last_two()

scores2 = [30]
student2 = StudentScores(scores2)
student2.highest_last_two()