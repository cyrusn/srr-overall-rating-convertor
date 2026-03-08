import json
from collections import Counter

def check_geog_json(filename):
    with open(filename, 'r') as f:
        students = json.load(f)

    geog_percentiles = []
    geog_ratings = []
    
    for s in students:
        if 'geog' in s and isinstance(s['geog'], dict):
            p = s['geog'].get('percentile')
            r = s['geog'].get('overallRating')
            if p: geog_percentiles.append(p)
            if r: geog_ratings.append(r)

    print(f"Total Geog students: {len(geog_percentiles)}")
    print("Percentiles:", Counter(geog_percentiles))
    print("Ratings:", Counter(geog_ratings))

if __name__ == "__main__":
    check_geog_json("v2/report_output/students.json")
