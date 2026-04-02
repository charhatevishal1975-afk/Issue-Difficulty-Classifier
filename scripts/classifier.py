import pandas as pd
import os

def classify_difficulty(row):
    """
    Applies heuristic rules to classify GitHub issue difficulty.
    """
    # Safely extract and normalize text fields
    title = str(row.get('Title', '')).lower()
    desc = str(row.get('Description', '')).lower()
    labels = str(row.get('Labels', '')).lower()
    
    # Safely parse comment count
    try:
        comments = int(row.get('CommentCount', 0))
    except ValueError:
        comments = 0

    # 1. Absolute Overrides based on GitHub's standard label conventions
    easy_labels = ['good first issue', 'easy', 'beginner', 'first timers only', 'good-first-issue']
    hard_labels = ['hard', 'complex', 'architecture', 'expert']

    for el in easy_labels:
        if el in labels:
            return 'Easy'
    for hl in hard_labels:
        if hl in labels:
            return 'Hard'

    # 2. Heuristic Scoring System
    score = 0
    full_text = title + " " + desc

    # Keyword analysis
    hard_keywords = ['race condition', 'memory leak', 'segfault', 'concurrency', 
                     'optimization', 'performance', 'vulnerability', 'cve', 'thread', 'deadlock']
    medium_keywords = ['refactor', 'enhancement', 'feature', 'integration', 'dependency', 'api']
    easy_keywords = ['typo', 'docs', 'documentation', 'readme', 'spelling', 'format', 'lint']

    if any(word in full_text for word in hard_keywords):
        score += 3
    if any(word in full_text for word in medium_keywords):
        score += 1
    if any(word in full_text for word in easy_keywords):
        score -= 1  # Trivial fixes lower the difficulty

    # Engagement analysis
    if comments > 15:
        score += 2
    elif comments > 5:
        score += 1

    # Length analysis
    if len(desc) > 1500:
        score += 1

    # 3. Final Decision Mapping
    if score <= 0:
        return 'Easy'
    elif score <= 2:
        return 'Medium'
    else:
        return 'Hard'

def run_classifier(input_file='raw_issues.csv', output_file='classified_issues.csv'):
    # Locate the files safely
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, input_file)
    output_path = os.path.join(base_dir, output_file)

    if not os.path.exists(input_path):
        print(f"Error: {input_file} not found. Run scraper.py first.")
        return

    print(f"Loading {input_file} for classification...")
    df = pd.read_csv(input_path)
    
    # Apply the classification function to each row
    print("Applying heuristic grading algorithms...")
    df['Difficulty'] = df.apply(classify_difficulty, axis=1)
    
    # Save the results
    df.to_csv(output_path, index=False)
    
    # Print a quick summary of the distribution
    distribution = df['Difficulty'].value_counts()
    print(f"\nClassification complete! Data saved to {output_file}")
    print("\nDifficulty Distribution:")
    print(distribution.to_string())

if __name__ == "__main__":
    run_classifier()