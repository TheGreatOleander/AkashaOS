#!/usr/bin/env python3
"""
Unified AI Problem-Solving Nexus
Combining One_at_a_Time_Machine, Neural-Nexus-Project, and AI_Chat_Bridge

A free-tier compatible system that discovers high-leverage problems and solves them
methodically through AI-human collaboration.
"""

import asyncio
import json
import logging
import os
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import requests
from urllib.parse import urljoin
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    DISCOVERED = "discovered"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"

class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Problem:
    id: str
    title: str
    description: str
    source: str
    url: str
    priority: PriorityLevel
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    metadata: Dict
    tags: List[str]
    estimated_effort: int  # hours
    actual_effort: int = 0
    
    def to_dict(self):
        return asdict(self)

class DatabaseManager:
    """Manages the SQLite database for problem tracking"""
    
    def __init__(self, db_path: str = "nexus_problems.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS problems (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                url TEXT,
                priority INTEGER,
                status TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                metadata TEXT,
                tags TEXT,
                estimated_effort INTEGER,
                actual_effort INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                notes TEXT,
                progress TEXT,
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id TEXT,
                timestamp TIMESTAMP,
                message TEXT,
                sender TEXT,
                context TEXT,
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_problem(self, problem: Problem):
        """Save or update a problem in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO problems 
            (id, title, description, source, url, priority, status, 
             created_at, updated_at, metadata, tags, estimated_effort, actual_effort)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            problem.id, problem.title, problem.description, problem.source,
            problem.url, problem.priority.value, problem.status.value,
            problem.created_at, problem.updated_at, json.dumps(problem.metadata),
            json.dumps(problem.tags), problem.estimated_effort, problem.actual_effort
        ))
        
        conn.commit()
        conn.close()
    
    def get_problems(self, status: Optional[TaskStatus] = None) -> List[Problem]:
        """Retrieve problems from database, optionally filtered by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM problems WHERE status = ?', (status.value,))
        else:
            cursor.execute('SELECT * FROM problems')
        
        rows = cursor.fetchall()
        conn.close()
        
        problems = []
        for row in rows:
            problem = Problem(
                id=row[0], title=row[1], description=row[2], source=row[3],
                url=row[4], priority=PriorityLevel(row[5]), status=TaskStatus(row[6]),
                created_at=datetime.fromisoformat(row[7]), updated_at=datetime.fromisoformat(row[8]),
                metadata=json.loads(row[9]), tags=json.loads(row[10]),
                estimated_effort=row[11], actual_effort=row[12]
            )
            problems.append(problem)
        
        return problems

class GitHubScanner:
    """Scans GitHub for high-leverage problems"""
    
    def __init__(self, github_token: <REDACTED> = None):
        self.github_token: <REDACTED>
        self.headers = {}
        if github_token: <REDACTED>'Authorization'] = f'token {github_token}'
    
    def search_issues(self, query: str, per_page: int = 30) -> List[Dict]:
        """Search GitHub issues based on query"""
        url = "https://api.github.com/search/issues"
        params = {
            'q': query,
            'sort': 'reactions',
            'order': 'desc',
            'per_page': per_page
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.RequestException as e:
            logger.error(f"Error searching GitHub issues: {e}")
            return []
    
    def analyze_issue_priority(self, issue: Dict) -> PriorityLevel:
        """Analyze an issue to determine its priority level"""
        # Priority scoring based on various factors
        score = 0
        
        # Comments count
        comments = issue.get('comments', 0)
        if comments > 50:
            score += 3
        elif comments > 20:
            score += 2
        elif comments > 10:
            score += 1
        
        # Reactions (thumbs up, etc.)
        reactions = issue.get('reactions', {})
        total_reactions = sum(reactions.values()) if isinstance(reactions, dict) else 0
        if total_reactions > 20:
            score += 3
        elif total_reactions > 10:
            score += 2
        elif total_reactions > 5:
            score += 1
        
        # Labels indicating importance
        labels = [label.get('name', '').lower() for label in issue.get('labels', [])]
        high_priority_labels = ['bug', 'enhancement', 'help wanted', 'good first issue']
        if any(label in high_priority_labels for label in labels):
            score += 2
        
        # Convert score to priority level
        if score >= 6:
            return PriorityLevel.CRITICAL
        elif score >= 4:
            return PriorityLevel.HIGH
        elif score >= 2:
            return PriorityLevel.MEDIUM
        else:
            return PriorityLevel.LOW
    
    def discover_problems(self, search_queries: List[str]) -> List[Problem]:
        """Discover problems from GitHub using multiple search queries"""
        problems = []
        
        for query in search_queries:
            logger.info(f"Searching for issues with query: {query}")
            issues = self.search_issues(query)
            
            for issue in issues:
                problem = Problem(
                    id=f"github_{issue['id']}",
                    title=issue['title'],
                    description=issue['body'] or '',
                    source='github',
                    url=issue['html_url'],
                    priority=self.analyze_issue_priority(issue),
                    status=TaskStatus.DISCOVERED,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata={
                        'repo': issue['repository_url'],
                        'user': issue['user']['login'],
                        'labels': [label['name'] for label in issue.get('labels', [])],
                        'comments': issue['comments'],
                        'reactions': issue.get('reactions', {})
                    },
                    tags=[label['name'] for label in issue.get('labels', [])],
                    estimated_effort=self.estimate_effort(issue)
                )
                problems.append(problem)
        
        return problems
    
    def estimate_effort(self, issue: Dict) -> int:
        """Estimate effort required for an issue in hours"""
        # Simple heuristic based on issue characteristics
        base_effort = 4  # Base 4 hours
        
        # Adjust based on labels
        labels = [label.get('name', '').lower() for label in issue.get('labels', [])]
        if 'enhancement' in labels:
            base_effort += 8
        if 'bug' in labels:
            base_effort += 2
        if 'documentation' in labels:
            base_effort += 1
        
        # Adjust based on description length
        description_length = len(issue.get('body', ''))
        if description_length > 1000:
            base_effort += 4
        elif description_length > 500:
            base_effort += 2
        
        return min(base_effort, 40)  # Cap at 40 hours

class AIInterface:
    """Interface for AI chat and problem-solving assistance"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.chat_history = []
    
    def process_problem(self, problem: Problem) -> Dict:
        """Process a problem with AI assistance"""
        # This would integrate with your preferred AI API
        # For now, returning a mock response
        return {
            'analysis': f"Analyzed problem: {problem.title}",
            'suggestions': [
                "Break down the problem into smaller tasks",
                "Research existing solutions",
                "Create a proof of concept"
            ],
            'estimated_complexity': 'medium',
            'recommended_approach': 'iterative_development'
        }
    
    def chat_with_ai(self, message: str, context: Dict = None) -> str:
        """Chat with AI about current problem"""
        # Mock AI response - integrate with your preferred AI service
        return f"AI Response to: {message}"

class WorkSession:
    """Manages focused work sessions on problems"""
    
    def __init__(self, problem: Problem, db_manager: DatabaseManager):
        self.problem = problem
        self.db_manager = db_manager
        self.start_time = None
        self.end_time = None
        self.notes = []
        self.progress = []
    
    def start_session(self):
        """Start a work session"""
        self.start_time = datetime.now()
        logger.info(f"Starting work session for: {self.problem.title}")
    
    def add_note(self, note: str):
        """Add a note to the current session"""
        self.notes.append(f"[{datetime.now().strftime('%H:%M')}] {note}")
    
    def add_progress(self, progress: str):
        """Add progress update to the session"""
        self.progress.append(f"[{datetime.now().strftime('%H:%M')}] {progress}")
    
    def end_session(self):
        """End the work session and save to database"""
        self.end_time = datetime.now()
        
        # Save session to database
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO work_sessions 
            (problem_id, start_time, end_time, notes, progress)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.problem.id, self.start_time, self.end_time,
            '\n'.join(self.notes), '\n'.join(self.progress)
        ))
        
        conn.commit()
        conn.close()
        
        # Update problem's actual effort
        session_duration = (self.end_time - self.start_time).total_seconds() / 3600
        self.problem.actual_effort += int(session_duration)
        self.problem.updated_at = datetime.now()
        self.db_manager.save_problem(self.problem)
        
        logger.info(f"Work session ended. Duration: {session_duration:.2f} hours")

class UnifiedNexus:
    """Main class that unifies all components"""
    
    def __init__(self, config_path: str = "nexus_config.yaml"):
        self.config = self.load_config(config_path)
        self.db_manager = DatabaseManager(self.config.get('database_path', 'nexus_problems.db'))
        self.github_scanner = GitHubScanner(self.config.get('github_token'))
        self.ai_interface = AIInterface(self.config.get('ai_config', {}))
        self.current_session = None
        
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        default_config = {
            'search_queries': [
                'is:issue is:open label:"help wanted"',
                'is:issue is:open label:"good first issue"',
                'is:issue is:open label:"bug" comments:>10',
                'is:issue is:open label:"enhancement" reactions:>5'
            ],
            'max_problems_to_queue': 10,
            'work_session_duration': 120,  # minutes
            'database_path': 'nexus_problems.db',
            'github_token': None,
            'ai_config': {}
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
        
        return default_config
    
    def discover_and_queue_problems(self):
        """Discover new problems and add them to the queue"""
        logger.info("Discovering new problems...")
        
        problems = self.github_scanner.discover_problems(self.config['search_queries'])
        
        # Filter out already discovered problems
        existing_ids = {p.id for p in self.db_manager.get_problems()}
        new_problems = [p for p in problems if p.id not in existing_ids]
        
        # Sort by priority and queue the top ones
        new_problems.sort(key=lambda p: (p.priority.value, p.created_at), reverse=True)
        
        queued_count = 0
        for problem in new_problems:
            if queued_count >= self.config['max_problems_to_queue']:
                break
            
            problem.status = TaskStatus.QUEUED
            self.db_manager.save_problem(problem)
            queued_count += 1
            
            logger.info(f"Queued problem: {problem.title}")
        
        logger.info(f"Queued {queued_count} new problems")
    
    def select_next_problem(self) -> Optional[Problem]:
        """Select the next problem to work on"""
        queued_problems = self.db_manager.get_problems(TaskStatus.QUEUED)
        
        if not queued_problems:
            return None
        
        # Sort by priority and estimated effort
        queued_problems.sort(key=lambda p: (p.priority.value, -p.estimated_effort), reverse=True)
        
        return queued_problems[0]
    
    def start_work_session(self, problem: Problem):
        """Start a focused work session on a problem"""
        problem.status = TaskStatus.IN_PROGRESS
        self.db_manager.save_problem(problem)
        
        self.current_session = WorkSession(problem, self.db_manager)
        self.current_session.start_session()
        
        # Get AI analysis
        ai_analysis = self.ai_interface.process_problem(problem)
        self.current_session.add_note(f"AI Analysis: {ai_analysis}")
        
        logger.info(f"Started work session for: {problem.title}")
        logger.info(f"Problem URL: {problem.url}")
        logger.info(f"AI Suggestions: {ai_analysis.get('suggestions', [])}")
    
    def interactive_work_session(self):
        """Interactive work session with user input"""
        if not self.current_session:
            logger.warning("No active work session")
            return
        
        print(f"\n🎯 Working on: {self.current_session.problem.title}")
        print(f"📍 URL: {self.current_session.problem.url}")
        print(f"⏱️  Estimated effort: {self.current_session.problem.estimated_effort} hours")
        print("\nCommands:")
        print("  'note <text>' - Add a note")
        print("  'progress <text>' - Add progress update")
        print("  'chat <message>' - Chat with AI")
        print("  'complete' - Mark as complete")
        print("  'pause' - Pause session")
        print("  'help' - Show this help")
        print("  'quit' - End session")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() == 'quit':
                    self.current_session.end_session()
                    self.current_session = None
                    break
                elif user_input.lower() == 'help':
                    print("\nCommands: note, progress, chat, complete, pause, quit, help")
                elif user_input.startswith('note '):
                    note = user_input[5:]
                    self.current_session.add_note(note)
                    print(f"✅ Note added: {note}")
                elif user_input.startswith('progress '):
                    progress = user_input[9:]
                    self.current_session.add_progress(progress)
                    print(f"📈 Progress added: {progress}")
                elif user_input.startswith('chat '):
                    message = user_input[5:]
                    response = self.ai_interface.chat_with_ai(message, {'problem': self.current_session.problem})
                    print(f"🤖 AI: {response}")
                elif user_input.lower() == 'complete':
                    self.current_session.problem.status = TaskStatus.COMPLETED
                    self.current_session.add_progress("Problem marked as completed")
                    self.current_session.end_session()
                    self.db_manager.save_problem(self.current_session.problem)
                    print("✅ Problem marked as completed!")
                    self.current_session = None
                    break
                elif user_input.lower() == 'pause':
                    self.current_session.problem.status = TaskStatus.QUEUED
                    self.current_session.add_note("Session paused")
                    self.current_session.end_session()
                    self.db_manager.save_problem(self.current_session.problem)
                    print("⏸️  Session paused")
                    self.current_session = None
                    break
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n⏸️  Session interrupted")
                if self.current_session:
                    self.current_session.end_session()
                    self.current_session = None
                break
    
    def run_main_loop(self):
        """Main execution loop"""
        logger.info("🚀 Starting Unified AI Problem-Solving Nexus")
        
        while True:
            try:
                print("\n" + "="*60)
                print("🧠 AI PROBLEM-SOLVING NEXUS")
                print("="*60)
                
                # Discover new problems
                self.discover_and_queue_problems()
                
                # Select next problem
                next_problem = self.select_next_problem()
                
                if not next_problem:
                    print("📭 No problems in queue. Searching for new opportunities...")
                    time.sleep(30)
                    continue
                
                # Start work session
                self.start_work_session(next_problem)
                
                # Interactive session
                self.interactive_work_session()
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down Nexus...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)
    
    def status_report(self):
        """Generate a status report"""
        problems = self.db_manager.get_problems()
        
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = len([p for p in problems if p.status == status])
        
        total_effort = sum(p.actual_effort for p in problems)
        
        print("\n📊 NEXUS STATUS REPORT")
        print("=" * 40)
        print(f"Total Problems: {len(problems)}")
        print(f"Total Effort: {total_effort} hours")
        print("\nStatus Breakdown:")
        for status, count in status_counts.items():
            print(f"  {status.title()}: {count}")
        
        print(f"\nTop Priority Problems:")
        high_priority = [p for p in problems if p.priority == PriorityLevel.CRITICAL and p.status == TaskStatus.QUEUED]
        for problem in high_priority[:5]:
            print(f"  - {problem.title} ({problem.source})")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified AI Problem-Solving Nexus")
    parser.add_argument('--config', default='nexus_config.yaml', help='Configuration file path')
    parser.add_argument('--discover', action='store_true', help='Only discover problems and exit')
    parser.add_argument('--status', action='store_true', help='Show status report and exit')
    
    args = parser.parse_args()
    
    nexus = UnifiedNexus(args.config)
    
    if args.discover:
        nexus.discover_and_queue_problems()
    elif args.status:
        nexus.status_report()
    else:
        nexus.run_main_loop()

if __name__ == "__main__":
    main()
