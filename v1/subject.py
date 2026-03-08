from constant import gradings_f5_term1
from typing import TypedDict, Tuple, List


class Grading(TypedDict):
    """Grading represents a grading scale"""

    subject: str
    grade: int
    range: Tuple[int, int]


class Subject:
    def __init__(self, id: str):
        self.id = id

    def scoreToGrade(self, score: int, gradings: List[Grading]) -> int:
        for grading in gradings:
            if grading["subject"] != self.id:
                continue
            min, max = grading["range"]
            if score >= min and score <= max:
                return grading["grade"]
        return 0


if __name__ == "__main__":
    bio = Subject("bio")
    print(bio.scoreToGrade(119, gradings_f5_term1))
