#!/usr/bin/env python3
"""
GitHub Account Strength Analyzer
Beautiful terminal-based analysis of GitHub profile strength
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os

# Color codes for beautiful terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print beautiful ASCII banner"""
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
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
{Colors.ENDC}"""
    print(banner)

def get_github_data(username: str, token: Optional[str] = None) -> Dict:
    """Fetch GitHub user data and repositories"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        # Get user profile
        user_response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        # Get repositories
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100', headers=headers)
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        
        # Get events (activity)
        events_response = requests.get(f'https://api.github.com/users/{username}/events?per_page=100', headers=headers)
        events_response.raise_for_status()
        events_data = events_response.json()
        
        return {
            'user': user_data,
            'repos': repos_data,
            'events': events_data
        }
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}Error fetching data: {e}{Colors.ENDC}")
        return None

def analyze_profile_completeness(user_data: Dict) -> Dict:
    """Analyze profile completeness"""
    score = 0
    max_score = 100
    details = []
    
    # Basic info (40 points)
    if user_data.get('name'):
        score += 10
        details.append(f"{Colors.OKGREEN}✓ Name provided{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Name missing{Colors.ENDC}")
    
    if user_data.get('bio'):
        score += 10
        details.append(f"{Colors.OKGREEN}✓ Bio provided{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Bio missing{Colors.ENDC}")
    
    if user_data.get('location'):
        score += 10
        details.append(f"{Colors.OKGREEN}✓ Location provided{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Location missing{Colors.ENDC}")
    
    if user_data.get('company'):
        score += 10
        details.append(f"{Colors.OKGREEN}✓ Company provided{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Company missing{Colors.ENDC}")
    
    # Contact info (30 points)
    if user_data.get('email'):
        score += 15
        details.append(f"{Colors.OKGREEN}✓ Email provided{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Email missing{Colors.ENDC}")
    
    if user_data.get('blog'):
        score += 15
        details.append(f"{Colors.OKGREEN}✓ Website/blog provided{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Website/blog missing{Colors.ENDC}")
    
    # Social (30 points)
    if user_data.get('twitter_username'):
        score += 15
        details.append(f"{Colors.OKGREEN}✓ Twitter linked{Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ Twitter not linked{Colors.ENDC}")
    
    if user_data.get('followers', 0) > 0:
        score += 15
        details.append(f"{Colors.OKGREEN}✓ Has followers ({user_data['followers']}){Colors.ENDC}")
    else:
        details.append(f"{Colors.WARNING}✗ No followers{Colors.ENDC}")
    
    return {'score': score, 'details': details}

def analyze_repository_quality(repos_data: List[Dict]) -> Dict:
    """Analyze repository quality and diversity"""
    if not repos_data:
        return {'score': 0, 'details': [f"{Colors.FAIL}✗ No repositories{Colors.ENDC}"]}
    
    score = 0
    details = []
    
    # Repository count (20 points)
    repo_count = len(repos_data)
    if repo_count >= 10:
        score += 20
        details.append(f"{Colors.OKGREEN}✓ Good repository count ({repo_count}){Colors.ENDC}")
    elif repo_count >= 5:
        score += 15
        details.append(f"{Colors.OKCYAN}○ Moderate repository count ({repo_count}){Colors.ENDC}")
    else:
        score += 10
        details.append(f"{Colors.WARNING}△ Few repositories ({repo_count}){Colors.ENDC}")
    
    # Documentation (25 points)
    documented_repos = sum(1 for repo in repos_data if repo.get('description'))
    doc_percentage = (documented_repos / repo_count) * 100
    
    if doc_percentage >= 80:
        score += 25
        details.append(f"{Colors.OKGREEN}✓ Excellent documentation ({doc_percentage:.1f}%){Colors.ENDC}")
    elif doc_percentage >= 60:
        score += 20
        details.append(f"{Colors.OKCYAN}○ Good documentation ({doc_percentage:.1f}%){Colors.ENDC}")
    else:
        score += 10
        details.append(f"{Colors.WARNING}△ Poor documentation ({doc_percentage:.1f}%){Colors.ENDC}")
    
    # Language diversity (20 points)
    languages = set()
    for repo in repos_data:
        if repo.get('language'):
            languages.add(repo['language'])
    
    lang_count = len(languages)
    if lang_count >= 5:
        score += 20
        details.append(f"{Colors.OKGREEN}✓ Great language diversity ({lang_count} languages){Colors.ENDC}")
    elif lang_count >= 3:
        score += 15
        details.append(f"{Colors.OKCYAN}○ Good language diversity ({lang_count} languages){Colors.ENDC}")
    else:
        score += 10
        details.append(f"{Colors.WARNING}△ Limited language diversity ({lang_count} languages){Colors.ENDC}")
    
    # Stars and forks (20 points)
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
    
    if total_stars >= 50:
        score += 15
        details.append(f"{Colors.OKGREEN}✓ Great community engagement ({total_stars} stars){Colors.ENDC}")
    elif total_stars >= 10:
        score += 10
        details.append(f"{Colors.OKCYAN}○ Good community engagement ({total_stars} stars){Colors.ENDC}")
    else:
        score += 5
        details.append(f"{Colors.WARNING}△ Limited community engagement ({total_stars} stars){Colors.ENDC}")
    
    # Recent activity (15 points)
    recent_repos = sum(1 for repo in repos_data 
                      if datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ') > 
                      datetime.now() - timedelta(days=90))
    
    if recent_repos >= repo_count * 0.5:
        score += 15
        details.append(f"{Colors.OKGREEN}✓ Active maintenance ({recent_repos} recently updated){Colors.ENDC}")
    elif recent_repos >= repo_count * 0.3:
        score += 10
        details.append(f"{Colors.OKCYAN}○ Moderate maintenance ({recent_repos} recently updated){Colors.ENDC}")
    else:
        score += 5
        details.append(f"{Colors.WARNING}△ Limited maintenance ({recent_repos} recently updated){Colors.ENDC}")
    
    return {'score': score, 'details': details}

def analyze_activity_consistency(events_data: List[Dict]) -> Dict:
    """Analyze activity consistency"""
    if not events_data:
        return {'score': 0, 'details': [f"{Colors.FAIL}✗ No recent activity{Colors.ENDC}"]}
    
    score = 0
    details = []
    
    # Recent activity (50 points)
    recent_events = len(events_data)
    if recent_events >= 50:
        score += 50
        details.append(f"{Colors.OKGREEN}✓ Very active ({recent_events} recent events){Colors.ENDC}")
    elif recent_events >= 20:
        score += 40
        details.append(f"{Colors.OKCYAN}○ Active ({recent_events} recent events){Colors.ENDC}")
    else:
        score += 25
        details.append(f"{Colors.WARNING}△ Limited activity ({recent_events} recent events){Colors.ENDC}")
    
    # Activity diversity (30 points)
    event_types = set(event.get('type', '') for event in events_data)
    type_count = len(event_types)
    
    if type_count >= 5:
        score += 30
        details.append(f"{Colors.OKGREEN}✓ Diverse activity types ({type_count} types){Colors.ENDC}")
    elif type_count >= 3:
        score += 20
        details.append(f"{Colors.OKCYAN}○ Good activity diversity ({type_count} types){Colors.ENDC}")
    else:
        score += 15
        details.append(f"{Colors.WARNING}△ Limited activity diversity ({type_count} types){Colors.ENDC}")
    
    # Consistency (20 points)
    if events_data:
        latest_event = datetime.strptime(events_data[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_since_last = (datetime.now() - latest_event).days
        
        if days_since_last <= 7:
            score += 20
            details.append(f"{Colors.OKGREEN}✓ Very recent activity ({days_since_last} days ago){Colors.ENDC}")
        elif days_since_last <= 30:
            score += 15
            details.append(f"{Colors.OKCYAN}○ Recent activity ({days_since_last} days ago){Colors.ENDC}")
        else:
            score += 10
            details.append(f"{Colors.WARNING}△ Activity not recent ({days_since_last} days ago){Colors.ENDC}")
    
    return {'score': score, 'details': details}

def display_strength_meter(score: int, max_score: int, title: str):
    """Display a beautiful strength meter"""
    percentage = (score / max_score) * 100
    bar_length = 40
    filled_length = int(bar_length * percentage / 100)
    
    # Color based on score
    if percentage >= 80:
        color = Colors.OKGREEN
    elif percentage >= 60:
        color = Colors.OKCYAN
    elif percentage >= 40:
        color = Colors.WARNING
    else:
        color = Colors.FAIL
    
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    print(f"\n{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{color}[{bar}] {percentage:.1f}% ({score}/{max_score}){Colors.ENDC}")

def main():
    """Main function"""
    print_banner()
    
    # Get username
    username = input(f"{Colors.OKBLUE}Enter GitHub username: {Colors.ENDC}").strip()
    if not username:
        print(f"{Colors.FAIL}Username is required!{Colors.ENDC}")
        return
    
    # Optional token for higher rate limits
    token = input(f"{Colors.OKBLUE}Enter GitHub token (optional, press Enter to skip): {Colors.ENDC}").strip()
    if not token:
        token = None
    
    print(f"\n{Colors.OKCYAN}Analyzing GitHub account: {username}...{Colors.ENDC}")
    
    # Fetch data
    data = get_github_data(username, token)
    if not data:
        return
    
    # Analyze different aspects
    profile_analysis = analyze_profile_completeness(data['user'])
    repo_analysis = analyze_repository_quality(data['repos'])
    activity_analysis = analyze_activity_consistency(data['events'])
    
    # Calculate overall score
    total_score = profile_analysis['score'] + repo_analysis['score'] + activity_analysis['score']
    max_total = 300
    
    # Display results
    print(f"\n{Colors.HEADER}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}                    GITHUB STRENGTH ANALYSIS                    {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}")
    
    # Overall score
    display_strength_meter(total_score, max_total, "🏆 OVERALL GITHUB STRENGTH")
    
    # Individual categories
    display_strength_meter(profile_analysis['score'], 100, "👤 PROFILE COMPLETENESS")
    for detail in profile_analysis['details']:
        print(f"    {detail}")
    
    display_strength_meter(repo_analysis['score'], 100, "📚 REPOSITORY QUALITY")
    for detail in repo_analysis['details']:
        print(f"    {detail}")
    
    display_strength_meter(activity_analysis['score'], 100, "⚡ ACTIVITY CONSISTENCY")
    for detail in activity_analysis['details']:
        print(f"    {detail}")
    
    # Recommendations
    print(f"\n{Colors.HEADER}{Colors.BOLD}💡 RECOMMENDATIONS:{Colors.ENDC}")
    
    if profile_analysis['score'] < 80:
        print(f"    {Colors.WARNING}• Complete your profile with missing information{Colors.ENDC}")
    if repo_analysis['score'] < 80:
        print(f"    {Colors.WARNING}• Add descriptions to your repositories{Colors.ENDC}")
        print(f"    {Colors.WARNING}• Diversify your programming languages{Colors.ENDC}")
    if activity_analysis['score'] < 80:
        print(f"    {Colors.WARNING}• Increase your GitHub activity and consistency{Colors.ENDC}")
    
    if total_score >= 240:
        print(f"    {Colors.OKGREEN}🎉 Excellent GitHub presence! Keep up the great work!{Colors.ENDC}")
    elif total_score >= 180:
        print(f"    {Colors.OKCYAN}👍 Good GitHub presence with room for improvement{Colors.ENDC}")
    else:
        print(f"    {Colors.WARNING}📈 Focus on building a stronger GitHub presence{Colors.ENDC}")
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Analysis interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
