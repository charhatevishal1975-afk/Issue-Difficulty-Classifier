import { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import './App.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [issues, setIssues] = useState([]);
  const [stats, setStats] = useState(null);
  const [search, setSearch] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [skills, setSkills] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch Visualisation Stats
    axios.get('http://127.0.0.1:8000/api/stats/')
      .then(res => setStats(res.data))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    const fetchIssues = async () => {
      setLoading(true);
      try {
        let url = 'http://127.0.0.1:8000/api/issues/?';
        if (search) url += `search=${search}&`;
        if (difficulty) url += `difficulty=${difficulty}`;

        const response = await axios.get(url);
        setIssues(response.data);
      } catch (error) {
        console.error("Error fetching issues:", error);
      }
      setLoading(false);
    };

    const delayDebounceFn = setTimeout(() => {
      fetchIssues();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [search, difficulty]);

  // Skill Matcher Logic
  const userSkills = skills.toLowerCase().split(',').map(s => s.trim()).filter(s => s);
  
  const isRecommended = (issue) => {
    if (userSkills.length === 0) return false;
    const content = `${issue.title} ${issue.description} ${issue.labels}`.toLowerCase();
    return userSkills.some(skill => content.includes(skill));
  };

  const difficultyRank = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };

  // Create a sorted copy of the issues array
  const sortedIssues = [...issues].sort((a, b) => {
    const aRec = isRecommended(a);
    const bRec = isRecommended(b);

    // 1. Sort by Recommendation (Recommended comes first)
    if (aRec && !bRec) return -1;
    if (!aRec && bRec) return 1;

    // 2. Sort by Difficulty (Easy -> Medium -> Hard)
    return difficultyRank[a.difficulty] - difficultyRank[b.difficulty];
  });

  // Pie Chart Config
  const pieData = stats ? {
    labels: ['Easy', 'Medium', 'Hard'],
    datasets: [{
      data: [stats.distribution.Easy, stats.distribution.Medium, stats.distribution.Hard],
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
      borderWidth: 0,
    }]
  } : null;

  // Filter out useless repo-specific words from the cloud
  const ignoreWords = ['github', 'https', 'com', 'scikit', 'learn', 'sklearn', 'issue', 'issues'];

  return (
    <div className="dashboard-container">
      <header>
        <h1>WnCC Issue Dashboard</h1>
        <p>Advanced metrics and personalized repository recommendations.</p>
      </header>

      {/* Visualizations Section */}
      {stats && (
        <div className="stats-panel">
          <div className="chart-container">
            <h3>Issue Distribution</h3>
            <div className="pie-wrapper">
              <Pie data={pieData} options={{ maintainAspectRatio: false }} />
            </div>
          </div>
          <div className="wordcloud-container">
            <h3>Top Keywords by Difficulty</h3>
            <div className="clouds-flex">
              {['Easy', 'Medium', 'Hard'].map(diff => (
                <div key={diff} className="cloud-box">
                  <h4 className={diff.toLowerCase()}>{diff}</h4>
                  <div className="cloud-words">
                    {stats.word_clouds[diff]
                      .filter(word => !ignoreWords.includes(word.text))
                      .slice(0, 5) // Keep it to the top 15 words to prevent clutter
                      .map((word, idx) => {
                        // Logarithmic math: keeps highly frequent words from exploding the layout
                        const fontSize = Math.min(2.5, Math.max(0.8, Math.log(word.value + 1) * 0.7));
                        return (
                          <span 
                            key={idx} 
                            style={{ 
                              fontSize: `${fontSize}rem`, 
                              opacity: Math.min(1, 0.4 + (fontSize * 0.2)),
                              fontWeight: fontSize > 1.5 ? '700' : '500'
                            }}
                          >
                            {word.text}
                          </span>
                        );
                      })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Controls Section */}
      <div className="controls">
        <input
          type="text"
          placeholder="Declare skills (e.g. python, css, api)..."
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          className="search-bar skill-input"
        />
        <input
          type="text"
          placeholder="Search issues..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-bar"
        />
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="difficulty-filter"
        >
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>
      </div>

      {/* Issues Grid */}
     {loading ? (
        <div className="loading">Loading issues...</div>
      ) : (
        <div className="issues-grid">
          {/* Change issues.map to sortedIssues.map right here 👇 */}
          {sortedIssues.map((issue) => {
            const recommended = isRecommended(issue);
            return (
              <div key={issue.id} className={`issue-card ${issue.difficulty.toLowerCase()} ${recommended ? 'recommended' : ''}`}>
                <div className="card-header">
                  <span className="issue-id">#{issue.issue_id}</span>
                  <div className="badges">
                    {recommended && <span className="badge rec-badge">⭐ Recommended</span>}
                    <span className={`badge ${issue.difficulty.toLowerCase()}`}>
                      {issue.difficulty}
                    </span>
                  </div>
                </div>
                <h2>{issue.title}</h2>
                <div className="card-footer">
                  <span>💬 {issue.comment_count} comments</span>
                  <a href={`https://github.com/scikit-learn/scikit-learn/issues/${issue.issue_id}`} target="_blank" rel="noopener noreferrer" className="view-btn">View</a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default App;