import os
import csv
import django

# Initialize the Django environment so we can use the models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core_api.models import Issue

def import_data():
    # Locate the CSV file in the parent Q2 directory
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'classified_issues.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        return

    print("Importing issues into the database...")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            # update_or_create prevents duplicate entries if you run this twice
            Issue.objects.update_or_create(
                issue_id=row['IssueID'],
                defaults={
                    'title': row['Title'],
                    'description': row['Description'],
                    'labels': row['Labels'],
                    'last_updated': row['LastUpdated'],
                    'comment_count': int(row['CommentCount']),
                    'difficulty': row['Difficulty']
                }
            )
            count += 1
            
        print(f"Success! {count} issues injected into the database.")

if __name__ == '__main__':
    import_data()