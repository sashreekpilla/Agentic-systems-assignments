class StudentPerformance:
    def __init__(self,scores):
        self.scores=scores

    def score_difference(self):
        try:
            if len(self.scores)<1:
                raise IndexError()
            
            first=self.scores[0]
            print(first)
            last=self.scores[-1]
            print(last)

            if first >= last:
                diff=first-last
                print("Difference between last and first score is: "+ str(diff))
            else:
                diff=last-first
                print("Difference between last and first score is: "+ str(diff))

        except IndexError:
            print("No scores available to calculate difference")

scores1 = [15, 85, 45, 86, 98, 15, 90]
student1 = StudentPerformance(scores1)
student1.score_difference()

scores2 = []
student2 = StudentPerformance(scores2)
student2.score_difference()