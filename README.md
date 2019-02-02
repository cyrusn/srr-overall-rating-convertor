# School Reference Report

This repository generates the percentile report and overall rating performances report of SRR for JUPAS' application.

## Preparation

### Reports files and other json files

- Report files

  - `./data/private/f5_term1_report.json`
  - `./data/private/f5_term2_report.json`
  - `./data/private/f6_report.json`

User needs to prepare the above 3 JSON files, filename is matter, schema of the json file is listed at [schema session](#schema).

`./data/private/students.json` stores all basic information of each students. Please see the schema in [schema session](#schema).

`./data/public/subjectLevelCriteria.json` stores the criteria of the predicted DSE level of each subjects. Please see the schema in [schema session](#schema).

`./data/public/subjectInfo.json` stores all DSE subject codes which is generated from webSams.

### Schema

```javascript
// reports schema
[{
  "regno": Number,
  "chi": Number,
  "eng": Number,
  "math": Number,
  "ls": Number,
  "bafs": Number, // x1 code as key
  "cs": Number, // x2 code as key
  "m2": Number // only if student who take M2
}, ...]
```

```javascript
// students schema
[{
  "regno": Number,  
  "classcode": String,
  "classno": Number,
  "chname": String,
  "enname": String
}, ...]
```

```javascript
// subjectLevelCriteria.json
[{
  // subject subject, please refer to `./data/public/subjectInfo.json`
  "subject": String,
  // DSE level e.g. 4 mean level 4
  "level": Number,
  // range of attain the level, former is min and latter is max
  "range": [Number, Number]
}, ...]
```

## Run

```sh
python3 main.py
```

## Percentile Report

- P1 - Top 10%
- P2 - 11% - 25%
- P3 - 26% - 50%
- P4 - 51% - 75%
- P5 - Bottom 25%

## How to evaluate the SRR overall rating performance

### Ratio

F5 First Term | F5 Second Term | F6 Mock
------------- | -------------- | -------
25%           | 25%            | 50%

### Shorthand

#### Level

Evaluate the average of the predicted DSE level of each semester, result will be rounded to nearest integer.

#### Percentile

Percentile are evaluated from the ranking of students in subject. Weighted mean of subject scores are used to prioritize students. Percentile will be rounded down to nearest integer. e.g. If student's percentile is 5.9%, we will also treat his / her percentile as 5%.

### Criteria

- Excellent (R1):

  - Level 5 or above
  - or (percentile < 10% and Level 4)

- Very Good (R2):

  - Level 4 or above
  - or (percentile < 40% and Level 3)

- Good (R3):

  - Level 3 or above
  - or (percentile < 60% and Level 2)

- Average (R4):

  - Level 2 or above
  - or (percentile < 80% and Level 1)

- Below Average (R5)

  - Others

#### Compare with previous method

The above SRR performances will be compared with the previous percentile method, higher performance will go to student. Student's overall rating is simply retrieved from the percentiles below.

Excellent | Very Good | Good      | Average   | Below Average
--------- | --------- | --------- | --------- | -------------
Top 5%    | 5% – 10%  | 10% – 20% | 20% – 50% | Bottom 50%
