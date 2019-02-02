import json

with open("./data/public/subjectLevelCriteria.json") as f:
    criteria = json.load(f)


class Subject:
    def __init__(self, id):
        self.id = id

    def toLevel(self, score):
        for criterion in criteria:
            if criterion["subject"] != self.id:
                continue
            min = criterion["range"][0]
            max = criterion["range"][1]
            if score >= min and score <= max:
                return criterion["level"]


if __name__ == "__main__":
    bio = Subject("bio")
    print(bio.toLevel(119))

