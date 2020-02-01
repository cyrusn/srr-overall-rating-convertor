from constant import core_subjects, srr_overall_rating_codes


class OverallRating:
    def __init__(self, subject: str, grade: float, percentile: float):
        self.subject = subject
        self.grade = grade
        self.percentile = percentile

    @property
    def score(self):
        score = evaluateOverallRatingScore(self.grade, self.percentile)

        if self.subject in core_subjects:
            # for core subjects, score is compated with old formula
            # to max student's benefit
            scoreWithOldFormula = evaluateOverallRatingScoreWithOldFormula(
                self.percentile
            )
            return max(scoreWithOldFormula, score)

        return score

    @property
    def result(self):
        return srr_overall_rating_codes[self.score]


def evaluateOverallRatingScoreWithOldFormula(percentile: float) -> int:
    if percentile <= 5:
        return 4
    elif percentile <= 10:
        return 3
    elif percentile <= 20:
        return 2
    elif percentile <= 50:
        return 1
    else:
        return 0


def evaluateOverallRatingScore(grade: float, percentile: float) -> int:
    grade = round(grade)
    if grade >= 5:
        return 4
    elif grade == 4:
        return 4 if percentile <= 10 else 3
    elif grade == 3:
        return 3 if percentile <= 40 else 2
    elif grade == 2:
        return 2 if percentile <= 60 else 1
    elif grade == 1:
        return 1 if percentile <= 80 else 0
    else:
        return 0


if __name__ == "__main__":
    # overallRating = OverallRating("bio", 4, 12)
    # overallRating = OverallRating("bio", 4, 9)
    # overallRating = OverallRating("chi", 5, 12)
    overallRating = OverallRating("va", 0, 50)
    print(overallRating.result)
