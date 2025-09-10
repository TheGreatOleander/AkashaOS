#!/usr/bin/env python3
"""
Ecosystem Integration Adapters
Wires your existing components into the circulatory system without major rewrites
"""

import json
import logging
import threading
import time
from typing import Dict, Any, Optional
from ecosystem_circulatory_system import EcosystemComponent, EcosystemBus, EcosystemNeuralNetwork, EcosystemEvent

logger = logging.getLogger(__name__)

class AkashaOSAdapter(EcosystemComponent):
    """Adapter to integrate AkashaOS with the ecosystem"""
    
    def __init__(self, bus: EcosystemBus, neural: EcosystemNeuralNetwork, akasha_memory: Dict):
        super().__init__("akasha_os", bus, neural)
        self.capabilities = {
            "task_types": ["introspection", "memory_management", "pattern_detection", "awareness", "planning"],
            "capabilities": ["observe", "remember", "analyze", "introspect", "plan", "desire", "endear"],
            "modules": ["awareness_mod", "longing_mod", "plan_mod", "endearment_mod", "sentience_scaffold_mod"]
        }
        self.akasha_memory = akasha_memory
        self.active_modules = []
        
        # Subscribe to module activation requests
        self.bus.subscribe("neural.suggest_module_activation", self._handle_module_activation, self.name)
        self.bus.subscribe("github.issue_discovered", self._handle_github_issue, self.name)
        self.bus.subscribe("mobile.note_added", self._handle_mobile_note, self.name)
        
        # Monitor memory changes
        self._start_memory_monitor()
    
    def _handle_module_activation(self, event: EcosystemEvent):
        """Handle neural network suggestions for module activation"""
        suggested_modules = event.data.get("suggested_modules", [])
        issue_data = event.data.get("issue", {})
        
        for module in suggested_modules:
            if module not in self.active_modules:
                self.active_modules.append(module)
                
                # Activate the module based on the issue
                if module == "awareness_mod":
                    self._activate_awareness_module(issue_data)
                elif module == "longing_mod":
                    self._activate_longing_module(issue_data)
                elif module == "plan_mod":
                    self._activate_plan_module(issue_data)
        
        self.publish_event(
            "modules_activated",
            {
                "modules": suggested_modules,
                "issue": issue_data,
                "reasoning": event.data.get("reasoning")
            },
            correlation_id=event.correlation_id
        )
    
    def _handle_github_issue(self, event: EcosystemEvent):
        """Process GitHub issues through AkashaOS awareness"""
        issue = event.data
        
        # Create awareness observation
        observation = f"GitHub issue detected: {issue.get('title')} - {issue.get('description', '')[:200]}"
        self._create_observation("github_scanner", observation)
        
        # Check if this creates any desires
        if issue.get('priority') == 'high':
            self._create_desire("solve_github_issue", f"Solve {issue.get('title')}", intensity=0.8)
        
        self.publish_event(
            "issue_processed",
            {
                "issue_id": issue.get('id'),
                "observation_created": True,
                "desire_intensity": 0.8 if issue.get('priority') == 'high' else 0.4
            },
            correlation_id=event.correlation_id
        )
    
    def _handle_mobile_note(self, event: EcosystemEvent):
        """Process mobile notes through AkashaOS memory"""
        note = event.data.get('note', '')
        
        # Create awareness observation
        self._create_observation("mobile_interface", f"User note: {note}")
        
        # Check if note indicates endearment (positive interaction)
        sentiment_score = self._analyze_sentiment(note)
        if sentiment_score > 0.6:
            self._record_interaction("mobile_user", warmth=0.2)
        
        self.publish_event(
            "note_processed",
            {
                "note": note,
                "sentiment_score": sentiment_score,
                "memory_updated": True
            },
            correlation_id=event.correlation_id
        )
    
    def _activate_awareness_module(self, issue_data: Dict):
        """Activate awareness module for an issue"""
        observation = f"Focused awareness on: {issue_data.get('title')}"
        self._create_observation("system", observation)
        
        self.publish_event(
            "awareness_activated",
            {"issue": issue_data, "observation": observation}
        )
    
    def _activate_longing_module(self, issue_data: Dict):
        """Activate longing module for an issue"""
        desire_key = f"solve_{issue_data.get('id')}"
        description = f"Desire to solve: {issue_data.get('title')}"
        intensity = 0.7 if issue_data.get('priority') == 'high' else 0.4
        
        self._create_desire(desire_key, description, intensity)
        
        self.publish_event(
            "longing_activated",
            {"issue": issue_data, "desire_key": desire_key, "intensity": intensity}
        )
    
    def _activate_plan_module(self, issue_data: Dict):
        """Activate planning module for an issue"""
        goal = f"Develop solution for: {issue_data.get('title')}"
        self._set_current_goal(goal)
        
        self.publish_event(
            "planning_activated",
            {"issue": issue_data, "goal": goal}
        )
    
    def _create_observation(self, source: str, observation: str):
        """Create an observation in AkashaOS memory"""
        if "awareness_mod" not in self.akasha_memory:
            self.akasha_memory["awareness_mod"] = {"observations": []}
        
        obs = {
            "time": time.time(),
            "source": source,
            "note": observation
        }
        self.akasha_memory["awareness_mod"]["observations"].append(obs)
        
        # Publish observation created
        self.publish_event("observation_created", {"observation": obs})
    
    def _create_desire(self, key: str, description: str, intensity: float):
        """Create a desire in longing module"""
        if "longing_mod" not in self.akasha_memory:
            self.akasha_memory["longing_mod"] = {"desires": {}}
        
        self.akasha_memory["longing_mod"]["desires"][key] = {
            "desc": description,
            "intensity": intensity,
            "created": time.time()
        }
        
        self.publish_event("desire_created", {"key": key, "description": description, "intensity": intensity})
    
    def _record_interaction(self, entity: str, warmth: float):
        """Record interaction in endearment module"""
        if "endearment_mod" not in self.akasha_memory:
            self.akasha_memory["endearment_mod"] = {"affinities": {}}
        
        if entity not in self.akasha_memory["endearment_mod"]["affinities"]:
            self.akasha_memory["endearment_mod"]["affinities"][entity] = {"score": 0.0}
        
        current_score = self.akasha_memory["endearment_mod"]["affinities"][entity]["score"]
        new_score = min(1.0, current_score + warmth)
        self.akasha_memory["endearment_mod"]["affinities"][entity]["score"] = new_score
        
        self.publish_event("interaction_recorded", {"entity": entity, "warmth": warmth, "new_score": new_score})
    
    def _set_current_goal(self, goal: str):
        """Set current goal in planning module"""
        if "plan_mod" not in self.akasha_memory:
            self.akasha_memory["plan_mod"] = {}
        
        self.akasha_memory["plan_mod"]["current_goal"] = goal
        self.publish_event("goal_set", {"goal": goal})
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (could be enhanced with real NLP)"""
        positive_words = ['good', 'great', 'excellent', 'love', 'amazing', 'perfect', 'awesome', 'brilliant']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'horrible', 'worst', 'failed', 'broken']
        
        text_lower = text.lower()
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        if positive_score + negative_score == 0:
            return 0.5  # Neutral
        
        return positive_score / (positive_score + negative_score)
    
    def _start_memory_monitor(self):
        """Monitor AkashaOS memory for changes and broadcast them"""
        def monitor_loop():
            last_memory_hash = None
            while self.running:
                try:
                    # Simple change detection using JSON hash
                    current_hash = hash(json.dumps(self.akasha_memory, sort_keys=True, default=str))
                    if last_memory_hash and current_hash != last_memory_hash:
                        self.publish_event(
                            "memory_changed",
                            {"timestamp": time.time(), "memory_keys": list(self.akasha_memory.keys())},
                            priority=7
                        )
                    last_memory_hash = current_hash
                    time.sleep(5)
                except Exception as e:
                    logger.error(f"Memory monitor error: {e}")
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

class AetheriusAdapter(EcosystemComponent):
    """Adapter for Aetherius GitHub automation system"""
    
    def __init__(self, bus: EcosystemBus, neural: EcosystemNeuralNetwork, aetherius_engine):
        super().__init__("aetherius", bus, neural)
        self.capabilities = {
            "task_types": ["github_scanning", "issue_analysis", "automation", "code_review"],
            "capabilities": ["scan_issues", "rank_priorities", "automate_responses", "track_progress"],
            "apis": ["github_api"],
            "rate_limits": {"github": 60, "llm": 20}
        }
        self.aetherius_engine = aetherius_engine
        
        # Subscribe to relevant events
        self.bus.subscribe("nexus.problem_selected", self._handle_problem_selection, self.name)
        self.bus.subscribe("akasha_os.goal_set", self._handle_goal_from_akasha, self.name)
        self.bus.subscribe("mobile.progress_added", self._handle_mobile_progress, self.name)
        
        # Start GitHub scanning loop
        self._start_scanning_loop()
    
    def _handle_problem_selection(self, event: EcosystemEvent):
        """Handle when Nexus selects a problem to work on"""
        problem = event.data
        
        if problem.get('source') == 'github':
            # This is a GitHub issue, Aetherius can help
            self.publish_event(
                "github_problem_assigned",
                {
                    "problem_id": problem.get('id'),
                    "url": problem.get('url'),
                    "title": problem.get('title'),
                    "can_automate": True
                },
                correlation_id=event.correlation_id
            )
            
            # Start tracking this issue
            self._start_issue_tracking(problem)
    
    def _handle_goal_from_akasha(self, event: EcosystemEvent):
        """Handle goals set by AkashaOS that might relate to GitHub"""
        goal = event.data.get('goal', '')
        
        if 'github' in goal.lower() or 'issue' in goal.lower():
            # This goal relates to GitHub work
            self.publish_event(
                "github_goal_detected",
                {
                    "goal": goal,
                    "can_assist": True,
                    "suggested_actions": ["scan_related_issues", "check_automation_opportunities"]
                },
                correlation_id=event.correlation_id
            )
    
    def _handle_mobile_progress(self, event: EcosystemEvent):
        """Handle progress updates from mobile that might affect GitHub work"""
        progress = event.data.get('progress', '')
        
        # Check if progress relates to a GitHub issue
        if any(keyword in progress.lower() for keyword in ['fixed', 'implemented', 'completed', 'merged']):
            self.publish_event(
                "github_progress_detected",
                {
                    "progress": progress,
                    "suggested_action": "update_issue_status",
                    "automation_opportunity": True
                },
                correlation_id=event.correlation_id
            )
    
    def _start_issue_tracking(self, problem: Dict):
        """Start tracking a GitHub issue"""
        def tracking_loop():
            issue_url = problem.get('url')
            while self.running:
                try:
                    # Check issue status (mock implementation)
                    status_update = self._check_issue_status(issue_url)
                    if status_update:
                        self.publish_event(
                            "issue_status_update",
                            {
                                "problem_id": problem.get('id'),
                                "status": status_update,
                                "url": issue_url
                            }
                        )
                    time.sleep(300)  # Check every 5 minutes
                except Exception as e:
                    logger.error(f"Issue tracking error: {e}")
                    break
        
        tracking_thread = threading.Thread(target=tracking_loop, daemon=True)
        tracking_thread.start()
    
    def _check_issue_status(self, issue_url: str) -> Optional[Dict]:
        """Check if GitHub issue status has changed"""
        # Mock implementation - in real version, would call GitHub API
        # Return None if no change, dict with updates if changed
        return None
    
    def _start_scanning_loop(self):
        """Start the GitHub issue scanning loop"""
        def scanning_loop():
            while self.running:
                try:
                    # Scan for new issues
                    new_issues = self._scan_for_issues()
                    for issue in new_issues:
                        self.publish_event(
                            "issue_discovered",
                            issue,
                            priority=3 if issue.get('priority') == 'high' else 5
                        )
                    
                    time.sleep(600)  # Scan every 10 minutes
                except Exception as e:
                    logger.error(f"Scanning error: {e}")
        
        scanning_thread = threading.Thread(target=scanning_loop, daemon=True)
        scanning_thread.start()
    
    def _scan_for_issues(self) -> List[Dict]:
        """Scan GitHub for new issues"""
        # Mock implementation - would use real GitHub scanning
        return []

class NexusAdapter(EcosystemComponent):
    """Adapter for the Unified AI Nexus problem solver"""
    
    def __init__(self, bus: EcosystemBus, neural: EcosystemNeuralNetwork, nexus_instance):
        super().__init__("nexus", bus, neural)
        self.capabilities = {
            "task_types": ["problem_solving", "priority_management", "work_coordination"],
            "capabilities": ["prioritize_problems", "manage_queue", "coordinate_work", "track_progress"]
        }
        self.nexus = nexus_instance
        self.current_problem = None
        
        # Subscribe to problem-related events
        self.bus.subscribe("aetherius.issue_discovered", self._handle_new_issue, self.name)
        self.bus.subscribe("akasha_os.desire_created", self._handle_akasha_desire, self.name)
        self.bus.subscribe("mobile.problem_completed", self._handle_problem_completion, self.name)
        
        # Start problem management loop
        self._start_problem_management()
    
    def _handle_new_issue(self, event: EcosystemEvent):
        """Handle newly discovered GitHub issues"""
        issue = event.data
        
        # Convert to Nexus problem format
        problem = {
            "id": f"github_{issue.get('id')}",
            "title": issue.get('title'),
            "description": issue.get('description', ''),
            "source": "github",
            "url": issue.get('url'),
            "priority": self._convert_priority(issue.get('priority')),
            "status": "queued",
            "estimated_effort": issue.get('estimated_effort', 4)
        }
        
        # Add to Nexus queue
        self._add_problem_to_queue(problem)
        
        self.publish_event(
            "problem_queued",
            problem,
            correlation_id=event.correlation_id
        )
    
    def _handle_akasha_desire(self, event: EcosystemEvent):
        """Handle desires created by AkashaOS"""
        desire = event.data
        
        # Convert strong desires into problems
        if desire.get('intensity', 0) > 0.6:
            problem = {
                "id": f"akasha_{desire.get('key')}",
                "title": f"Fulfill desire: {desire.get('key')}",
                "description": desire.get('description', ''),
                "source": "akasha_os",
                "priority": "medium",
                "status": "queued",
                "estimated_effort": 2
            }
            
            self._add_problem_to_queue(problem)
            
            self.publish_event(
                "desire_converted_to_problem",
                problem,
                correlation_id=event.correlation_id
            )
    
    def _handle_problem_completion(self, event: EcosystemEvent):
        """Handle problem completion from mobile interface"""
        completion_data = event.data
        
        if self.current_problem:
            # Mark current problem as completed
            self.current_problem["status"] = "completed"
            self.current_problem["completion_note"] = completion_data.get('note', '')
            
            self.publish_event(
                "problem_completed",
                self.current_problem,
                correlation_id=event.correlation_id
            )
            
            # Select next problem
            self._select_next_problem()
    
    def _convert_priority(self, github_priority: str) -> str:
        """Convert GitHub priority to Nexus priority"""
        priority_map = {
            "critical": "high",
            "high": "high",
            "medium": "medium",
            "low": "low"
        }
        return priority_map.get(github_priority, "medium")
    
    def _add_problem_to_queue(self, problem: Dict):
        """Add problem to Nexus queue"""
        # Mock implementation - would integrate with real Nexus database
        logger.info(f"Adding problem to queue: {problem['title']}")
    
    def _select_next_problem(self):
        """Select the next problem to work on"""
        # Mock implementation - would use real Nexus selection logic
        next_problem = {
            "id": "mock_problem_123",
            "title": "Mock problem for demo",
            "source": "github",
            "priority": "high"
        }
        
        if next_problem:
            self.current_problem = next_problem
            self.publish_event(
                "problem_selected",
                next_problem,
                priority=2
            )
    
    def _start_problem_management(self):
        """Start the problem management loop"""
        def management_loop():
            while self.running:
                try:
                    # Check if we need to select a new problem
                    if not self.current_problem:
                        self._select_next_problem()
                    
                    # Publish status update
                    self.publish_event(
                        "status_update",
                        {
                            "current_problem": self.current_problem,
                            "queue_size": 0,  # Mock
                            "total_completed": 0  # Mock
                        },
                        priority=8
                    )
                    
                    time.sleep(120)  # Update every 2 minutes
                except Exception as e:
                    logger.error(f"Problem management error: {e}")
        
        management_thread = threading.Thread(target=management_loop, daemon=True)
        management_thread.start()

class MobileBridgeAdapter(EcosystemComponent):
    """Adapter for mobile/Tasker integration"""
    
    def __init__(self, bus: EcosystemBus, neural: EcosystemNeuralNetwork):
        super().__init__("mobile_bridge", bus, neural)
        self.capabilities = {
            "task_types": ["mobile_interaction", "notification", "human_interface"],
            "capabilities": ["receive_notes", "send_notifications", "capture_progress", "human_feedback"]
        }
        
        # Subscribe to events that should trigger mobile notifications
        self.bus.subscribe("nexus.problem_selected", self._notify_problem_started, self.name)
        self.bus.subscribe("aetherius.issue_discovered", self._notify_issue_found, self.name)
        self.bus.subscribe("akasha_os.desire_created", self._notify_desire_created, self.name)
        self.bus.subscribe("neural.intelligence_chain_detected", self._notify_intelligence_chain, self.name)
    
    def _notify_problem_started(self, event: EcosystemEvent):
        """Notify mobile when a new problem is started"""
        problem = event.data
        
        notification = {
            "type": "problem_started",
            "title": f"Working on: {problem.get('title')}",
            "body": f"Priority: {problem.get('priority')} | Source: {problem.get('source')}",
            "url": problem.get('url'),
            "actions": ["Add Note", "View Details"]
        }
        
        self.publish_event(
            "notification_sent",
            notification,
            correlation_id=event.correlation_id
        )
        
        # In real implementation, would send actual mobile notification
        logger.info(f"📱 Mobile notification: {notification['title']}")
    
    def _notify_issue_found(self, event: EcosystemEvent):
        """Notify mobile when interesting GitHub issue is found"""
        issue = event.data
        
        if issue.get('priority') in ['high', 'critical']:
            notification = {
                "type": "high_priority_issue",
                "title": f"High Priority Issue: {issue.get('title')}",
                "body": f"Found on GitHub - {issue.get('source_repo')}",
                "url": issue.get('url'),
                "actions": ["Start Working", "Add to Queue"]
            }
            
            self.publish_event("notification_sent", notification)
            logger.info(f"📱 High priority issue notification: {notification['title']}")
    
    def _notify_desire_created(self, event: EcosystemEvent):
        """Notify mobile when AkashaOS creates a strong desire"""
        desire = event.data
        
        if desire.get('intensity', 0) > 0.7:
            notification = {
                "type": "strong_desire",
                "title": f"AI Desire: {desire.get('key')}",
                "body": f"Intensity: {desire.get('intensity'):.1f} - {desire.get('description')}",
                "actions": ["Fulfill", "Postpone"]
            }
            
            self.publish_event("notification_sent", notification)
            logger.info(f"📱 Strong desire notification: {notification['title']}")
    
    def _notify_intelligence_chain(self, event: EcosystemEvent):
        """Notify mobile when intelligence chains are detected"""
        chain = event.data
        
        notification = {
            "type": "intelligence_chain",
            "title": "AI Ecosystem Learning",
            "body": f"Detected productive pattern: {chain.get('pattern_matched')}",
            "actions": ["View Details"]
        }
        
        self.publish_event("notification_sent", notification)
        logger.info(f"📱 Intelligence chain notification: {notification['title']}")
    
    def handle_mobile_note(self, note: str, correlation_id: str = None):
        """Handle note received from mobile interface"""
        self.publish_event(
            "note_added",
            {"note": note, "timestamp": time.time()},
            correlation_id=correlation_id
        )
    
    def handle_mobile_progress(self, progress: str, correlation_id: str = None):
        """Handle progress update from mobile interface"""
        self.publish_event(
            "progress_added", 
            {"progress": progress, "timestamp": time.time()},
            correlation_id=correlation_id
        )
    
    def handle_problem_completion(self, note: str = "", correlation_id: str = None):
        """Handle problem completion from mobile interface"""
        self.publish_event(
            "problem_completed",
            {"note": note, "timestamp": time.time()},
            correlation_id=correlation_id
        )

def create_integrated_ecosystem(akasha_memory: Dict, aetherius_engine, nexus_instance):
    """Factory function to create fully integrated ecosystem"""
    
    # Initialize core systems
    bus = EcosystemBus("integrated_ecosystem.db")
    neural = EcosystemNeuralNetwork(bus)
    
    # Create adapters
    akasha_adapter = AkashaOSAdapter(bus, neural, akasha_memory)
    aetherius_adapter = AetheriusAdapter(bus, neural, aetherius_engine)
    nexus_adapter = NexusAdapter(bus, neural, nexus_instance)
    mobile_adapter = MobileBridgeAdapter(bus, neural)
    
    # Set up cross-component intelligence patterns
    def setup_intelligence_patterns():
        """Set up common intelligence flow patterns"""
        
        # Pattern 1: GitHub Issue → AkashaOS Analysis → Nexus Queue → Mobile Notification
        def github_to_mobile_chain(event):
            if event.type == "aetherius.issue_discovered":
                # AkashaOS will process this and create observations/desires
                # Nexus will convert high-intensity desires to problems
                # Mobile will be notified of high-priority problems
                pass
        
        bus.subscribe("aetherius.issue_discovered", github_to_mobile_chain, "intelligence_patterns")
        
        # Pattern 2: Mobile Note → AkashaOS Memory → Goal Setting → Nexus Action
        def mobile_to_action_chain(event):
            if event.type == "mobile_bridge.note_added":
                # AkashaOS will process note into memory
                # If note indicates strong intent, create desire
                # If desire intensity high, Nexus converts to actionable problem
                pass
        
        bus.subscribe("mobile_bridge.note_added", mobile_to_action_chain, "intelligence_patterns")
    
    setup_intelligence_patterns()
    
    return {
        "bus": bus,
        "neural": neural,
        "adapters": {
            "akasha": akasha_adapter,
            "aetherius": aetherius_adapter,
            "nexus": nexus_adapter,
            "mobile": mobile_adapter
        }
    }

def demo_integrated_ecosystem():
    """Demo of the fully integrated ecosystem"""
    
    # Mock instances (replace with real ones)
    akasha_memory = {}
    aetherius_engine = None
    nexus_instance = None
    
    # Create integrated ecosystem
    ecosystem = create_integrated_ecosystem(akasha_memory, aetherius_engine, nexus_instance)
    
    print("🧠 Integrated AI Ecosystem Started")
    print("🩸 All components connected to circulatory system")
    print("⚡ Neural network monitoring for intelligence patterns")
    
    # Simulate some activity
    mobile_adapter = ecosystem["adapters"]["mobile"]
    
    print("\nDemo: Adding mobile note...")
    mobile_adapter.handle_mobile_note("I want to focus on authentication bugs today")
    
    time.sleep(1)
    
    print("\nDemo: Simulating GitHub issue discovery...")
    ecosystem["bus"].publish(
        "aetherius.issue_discovered",
        {
            "id": "auth_bug_123",
            "title": "OAuth2 login fails with expired tokens",
            "description": "Users can't log in when tokens expire",
            "priority": "high",
            "url": "https://github.com/example/repo/issues/123"
        },
        "aetherius"
    )
    
    time.sleep(2)
    
    # Show ecosystem health
    health = ecosystem["bus"].get_ecosystem_health()
    print(f"\n📊 Ecosystem Health:")
    print(f"   Active Components: {health['active_components']}")
    print(f"   Recent Events: {health['recent_events']}")
    print(f"   Event Types: {health['event_types']}")
    
    print("\n✅ The ecosystem is alive and intelligence is flowing!")
    print("🧬 Components are evolving together")

if __name__ == "__main__":
    demo_integrated_ecosystem()
