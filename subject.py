from constant import gradings_f5_term1


class Subject:
    def __init__(self, id):
        self.id = id

    def scoreToGrade(self, score, gradings):
        for grading in gradings:
            if grading["subject"] != self.id:
                continue
            min, max = grading["range"]
            if score >= min and score <= max:
                return grading["grade"]


if __name__ == "__main__":
    bio = Subject("bio")
    print(bio.scoreToGrade(119, gradings_f5_term1))
