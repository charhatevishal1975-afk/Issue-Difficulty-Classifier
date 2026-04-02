# Q2: Repository Issue Difficulty Classifier

– scraper.py is in `backend/scripts`
<br>
– classifier.py is in `backend/scripts`

This project provides an automated Workflow and interactive dashboard to fetch, classify, and visualize GitHub issues from any public repository. It is designed to help open-source contributors easily find issues matching their skill level.

## 🧠 Classification Logic

The difficulty classification engine (`scripts/classifier.py`) evaluates issues using a multi-layered heuristic approach rather than relying solely on raw text length.

1. **Absolute Overrides (Strongest Signal):** The algorithm first checks for standard GitHub community labels. If an issue is tagged with `good first issue` or `beginner`, it bypasses all other logic and is immediately classified as **Easy**. Labels like `architecture` or `complex` force a **Hard** classification.
2. **Keyword Scoring:** The engine scans the title and description for specific technical markers.
   - Words like `race condition`, `memory leak`, or `segfault` add heavy weight toward a **Hard** rating.
   - Words like `refactor` or `dependency` push the score toward **Medium**.
   - Words like `typo` or `docs` reduce the difficulty score, leaning toward **Easy**.
3. **Engagement Metrics:** Issues with a high comment count (e.g., >15) indicate a contested or deeply technical problem. The algorithm adds difficulty weight based on the volume of discussion.
4. **Length Analysis:** Descriptions exceeding 1500 characters often contain complex stack traces and system context, which marginally increases the difficulty score.

The final cumulative score maps the issue to its respective difficulty tier.

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js and npm
- A GitHub Personal Access Token (Classic)

### 1. Data Workflow & Backend Setup

Navigate to the `Q2` directory and set up the Python environment:

#Activate your virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#Install dependencies

```
pip install -r requirements.txt
```

#Create your environment file

```
echo "GITHUB_TOKEN=your_token_here" > .env
```

**Environment Setup** : Create a `.env` file.

- Paste your own GitHub Personal Access Token into the `GITHUB_TOKEN` variable.
- _Note: A token is required to bypass GitHub's strict 60-request/hour rate limit for unauthenticated users._

Run the data extraction and classification Workflow:

```Bash
python scripts/scraper.py
python scripts/classifier.py
```

Initialize the Django database and start the API:

```Bash
cd backend
python manage.py makemigrations
python manage.py migrate
python import_csv.py
python manage.py runserver
```

2. Frontend Dashboard Setup
   Open a new terminal, navigate to the Q2/frontend directory, and start the Vite server:

```Bash
npm install
npm run dev
The dashboard will be available at http://localhost:5173/.
```

📸 Dashboard Screenshots
(Add your screenshots here before final submission)

![Dashboard Overview](/Screenshot%202026-04-02%20122638.png)
![Dashboard Overview](/Screenshot%202026-04-02%20123457.png)

![Skill Matcher in Action](/Screenshot%202026-04-02%20123610.png)
