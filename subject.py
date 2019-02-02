import json

from constant import criteria


class Subject:
    def __init__(self, id):
        self.id = id

    def toLevel(self, score):
        for criterion in criteria:
            if criterion["subject"] != self.id:
                continue
            min, max = criterion["range"]
            if score >= min and score <= max:
                return criterion["level"]


if __name__ == "__main__":
    bio = Subject("bio")
    print(bio.toLevel(119))

