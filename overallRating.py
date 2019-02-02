CORE_SUBJECTS = ["chi", "eng", "math", "ls"]
SRR_OVERALL_RATING_CODES = ["R5", "R4", "R3", "R2", "R1"]


def evaluateOverallRatingScoreWithOldFormula(percentile):
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


def evaluateOverallRatingScore(level, percentile):
    if level >= 5:
        return 4
    elif level == 4:
        return 4 if percentile <= 10 else 3
    elif level == 3:
        return 3 if percentile <= 40 else 2
    elif level == 2:
        return 2 if percentile <= 60 else 1
    elif level == 1:
        return 1 if percentile <= 80 else 0
    else:
        return 0


def compareWithPreviousFormula(percentile, overallRatingScore):
    #  for core subjects, will compare with old formula to max student's benefit
    scoreByPreviousFormula = evaluateOverallRatingScoreWithOldFormula(percentile)
    return max(scoreByPreviousFormula, overallRatingScore)


class OverallRating:
    def __init__(self, subject, level, percentile):
        self.subject = subject
        self.level = level
        self.percentile = percentile

    @property
    def score(self):
        score = evaluateOverallRatingScore(self.level, self.percentile)

        if self.subject in CORE_SUBJECTS:
            return compareWithPreviousFormula(self.percentile, score)

        return score

    @property
    def result(self):
        return SRR_OVERALL_RATING_CODES[self.score]


if __name__ == "__main__":
    # overallRating = OverallRating("bio", 4, 12)
    # overallRating = OverallRating("bio", 4, 9)
    # overallRating = OverallRating("chi", 5, 12)
    overallRating = OverallRating("va", 0, 50)
    print(overallRating.result)
