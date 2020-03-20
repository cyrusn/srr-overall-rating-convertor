# School Reference Report

This repository generates the **Percentile Report** and **Overall Rating Report** of academic performance in **School Reference Report** session for JUPAS' application.

## Preparation

### Reports files and other JSON files

- Report files

  - `./data/private/f5_term1_report.json`
  - `./data/private/f5_term2_report.json`
  - `./data/private/f6_report.json`

User needs to prepare the above 3 JSON files, filename is matter, schema of the JSON file is listed at [schema session](#schema).

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

## Percentile Report Scale

The percentile report will be generated with the following scale.

| Indicator | Range      |
| --------- | ---------- |
| P1        | Top 10%    |
| P2        | 11% - 25%  |
| P3        | 26% - 50%  |
| P4        | 51% - 75%  |
| P5        | Bottom 25% |

## Overall Rating Report Scale

### Ratio

The following ratio will be used to calculate the overall rating of each subjects.

| F5 First Term | F5 Second Term | F6 Mock |
| ------------- | -------------- | ------- |
| 25%           | 25%            | 50%     |

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

The above method twill be compared with the previous method which simple using the following percentile to determine the overall rating. Better result will go to student.

| Excellent | Very Good | Good      | Average   | Below Average |
| --------- | --------- | --------- | --------- | ------------- |
| Top 5%    | 5% – 10%  | 10% – 20% | 20% – 50% | Bottom 50%    |

## TODO

- Directly parse the excel files that are exported from WEBSAM. So files below should prepare.

  - F5 term 1 report with related grading scale
  - F5 term 2 report with related grading scale
  - F6 Mock report with related grading scale
  - Students' information
  - Subject information (includes the subject code and short name)
