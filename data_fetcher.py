import csv

# Note :

# Type
# E (Extraversion) vs I (Introversion)
# S (Sensing) vs N (iNtuition)
# T (Thinking) vs F (Feeling)
# J (Judging) vs P (Perceiving)

# Score
# score1: ketika user menjawab 1 (Strongly Disagree)
# score2: ketika user menjawab 2 (Disagree)
# score3: ketika user menjawab 3 (Neutral)
# score4: ketika user menjawab 4 (Agree)
# score5: ketika user menjawab 5 (Strongly Agree)

class DataFetcher:
    def __init__(self, file_path: str) -> None:
        # Declare Data type
        self.data: list[tuple[str, dict[int, dict[str, float]]]] = []
        # Open CSV
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            # Read the CSV
            reader = csv.DictReader(f)
            # Looping per data Row
            for row in reader:
                trait_type = row['type']
                question = row['question']
                scores = {}
                # Update Score based pipe split
                for level in range(1, 6):
                    key = f'score{level}'
                    trait1_score, trait2_score = map(float, row[key].split('|'))
                    scores[level] = {trait_type[0]: trait1_score, trait_type[1]: trait2_score}
                self.data.append((question, scores))