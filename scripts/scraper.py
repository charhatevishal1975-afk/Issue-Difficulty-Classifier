import os
import csv
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_repo_issues(repo_name, output_file='raw_issues.csv', max_issues=100):
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not found in .env file.")
        return

    print(f"Connecting to GitHub to fetch issues from '{repo_name}'...")
    g = Github(token)
    
    try:
        repo = g.get_repo(repo_name)
        # Fetch open issues, sorted by newest
        issues = repo.get_issues(state='open', sort='updated', direction='desc')
        
        extracted_issues = []
        count = 0
        
        for issue in issues:
            if count >= max_issues:
                break
                
            # CRITICAL: The GitHub API treats Pull Requests as issues. 
            # We must skip them to only analyze actual bugs/feature requests.
            if issue.pull_request is not None:
                continue
                
            # Extract the exactly requested data points
            issue_data = {
                'IssueID': issue.number,
                'Title': issue.title.strip(),
                'Description': issue.body.strip() if issue.body else "",
                'Labels': ", ".join([label.name for label in issue.labels]),
                'LastUpdated': issue.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'CommentCount': issue.comments
            }
            
            extracted_issues.append(issue_data)
            count += 1
            
            if count % 10 == 0:
                print(f"Fetched {count} issues...")

        # Export to CSV for our classifier to consume
        keys = ['IssueID', 'Title', 'Description', 'Labels', 'LastUpdated', 'CommentCount']
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(extracted_issues)
            
        print(f"\nSuccess! {len(extracted_issues)} actual issues saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # We will test on scikit-learn as it has excellent issue tagging
    target_repo = "scikit-learn/scikit-learn" 
    fetch_repo_issues(target_repo, output_file='raw_issues.csv', max_issues=100)