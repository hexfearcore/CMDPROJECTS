# GitHub Strength Analyzer

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A beautiful terminal-based tool to analyze and score your GitHub account strength across multiple dimensions.

## ✨ Features

- **Beautiful ASCII Art Interface** - Eye-catching terminal display with colorful output
- **Comprehensive Analysis** - Evaluates profile completeness, repository quality, and activity consistency
- **Visual Progress Bars** - Color-coded strength meters for easy interpretation
- **Detailed Scoring** - 300-point scoring system with breakdowns
- **Actionable Recommendations** - Specific suggestions for improvement
- **GitHub API Integration** - Real-time data fetching with optional token support

## 🚀 Quick Start

### Prerequisites

```bash
pip install requests
```

### Installation

1. Clone or download the script
2. Make it executable (optional):
   ```bash
   chmod +x github_analyzer.py
   ```

### Usage

```bash
python github_analyzer.py
```

Follow the prompts:
1. Enter your GitHub username
2. Optionally provide a GitHub token for higher API limits

## 📊 Analysis Categories

### 👤 Profile Completeness (100 points)
- **Basic Info (40pts)**: Name, bio, location, company
- **Contact Info (30pts)**: Email, website/blog
- **Social (30pts)**: Twitter integration, follower count

### 📚 Repository Quality (100 points)
- **Repository Count (20pts)**: Number of repositories
- **Documentation (25pts)**: Description coverage
- **Language Diversity (20pts)**: Programming language variety
- **Community Engagement (20pts)**: Stars and forks
- **Maintenance (15pts)**: Recent activity on repositories

### ⚡ Activity Consistency (100 points)
- **Recent Activity (50pts)**: Number of recent events
- **Activity Diversity (30pts)**: Variety of event types
- **Consistency (20pts)**: Recency of last activity

## 🎯 Scoring System

| Score Range | Rating | Description |
|-------------|--------|-------------|
| 240-300 | 🏆 Excellent | Outstanding GitHub presence |
| 180-239 | 👍 Good | Solid presence with room for improvement |
| 120-179 | 📈 Developing | Building GitHub presence |
| 0-119 | 🔧 Needs Work | Significant improvements needed |

## 🔧 Configuration

### GitHub Token (Recommended)

To avoid rate limiting, create a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `public_repo` scope
3. Use the token when prompted by the script

### API Rate Limits

- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour

## 🎨 Sample Output

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ┌─┐┬┌┬┐┬ ┬┬ ┬┌┐    ┌─┐┌┬┐┬─┐┌─┐┌┐┌┌─┐┌┬┐┬ ┬               ║
║    │ ┬│ │ ├─┤│ │├┴┐   └─┐ │ ├┬┘├┤ ││││ ┬ │ ├─┤               ║
║    └─┘┴ ┴ ┴ ┴└─┘└─┘   └─┘ ┴ ┴└─└─┘┘└┘└─┘ ┴ ┴ ┴               ║
║                                                               ║
║              ┌─┐┌┐┌┌─┐┬ ┬ ┬┌─┐┌─┐┬─┐                         ║
║              ├─┤│││├─┤│ └┬┘┌─┘├┤ ├┬┘                         ║
║              ┴ ┴┘└┘┴ ┴┴─┘┴ └─┘└─┘┴└─                         ║
║                                                               ║
║                        (HEXFEARCORE)                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🏆 OVERALL GITHUB STRENGTH
[████████████████████████████████░░░░░░░░] 82.3% (247/300)
```

## 💡 Improvement Tips

- **Complete your profile** with all available information
- **Add descriptions** to all repositories
- **Diversify programming languages** in your projects
- **Maintain consistent activity** with regular commits
- **Engage with the community** through issues and pull requests

## 🐛 Troubleshooting

### Common Issues

**Rate limit exceeded**: Use a GitHub token for higher limits

**User not found**: Verify the username spelling

**Network errors**: Check internet connection and GitHub API status

### Error Messages

The script provides colored error messages for easy debugging:
- 🔴 Red: Critical errors
- 🟡 Yellow: Warnings
- 🟢 Green: Success messages

## 📝 License

MIT License - feel free to use and modify as needed.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional analysis metrics
- Export functionality (JSON, CSV)
- Historical tracking
- Team/organization analysis

## 🔗 Links

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Python Requests Library](https://docs.python-requests.org/)

---

**Created by HEXFEARCORE** 🚀