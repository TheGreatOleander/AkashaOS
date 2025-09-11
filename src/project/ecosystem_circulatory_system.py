#!/usr/bin/env python3
"""
AI Ecosystem Central Nervous & Circulatory System
The missing piece that makes your distributed intelligence actually distributed
"""

import asyncio
import json
import logging
import threading
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Set
from pathlib import Path
import sqlite3
import weakref

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EcosystemEvent:
    """Standard event format for ecosystem communication"""
    id: str
    type: str
    data: Dict[str, Any]
    source: str
    timestamp: datetime
    priority: int = 5  # 1=critical, 10=low
    correlation_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    ttl_seconds: int = 3600  # Event expires after 1 hour
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'data': self.data,
            'source': self.source,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority,
            'correlation_id': self.correlation_id,
            'tags': self.tags,
            'ttl_seconds': self.ttl_seconds
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            type=data['type'],
            data=data['data'],
            source=data['source'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            priority=data.get('priority', 5),
            correlation_id=data.get('correlation_id'),
            tags=data.get('tags', []),
            ttl_seconds=data.get('ttl_seconds', 3600)
        )
    
    def is_expired(self):
        return datetime.now() > self.timestamp + timedelta(seconds=self.ttl_seconds)

class EcosystemBus:
    """Central message bus - the circulatory system"""
    
    def __init__(self, persistence_path: str = "ecosystem_events.db"):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_history: deque = deque(maxlen=10000)
        self.active_correlations: Dict[str, List[EcosystemEvent]] = defaultdict(list)
        self.persistence_path = persistence_path
        self.running = True
        
        # Component health tracking
        self.component_heartbeats: Dict[str, datetime] = {}
        self.component_metadata: Dict[str, Dict] = {}
        
        # Event statistics
        self.event_stats = defaultdict(int)
        self.component_stats = defaultdict(lambda: defaultdict(int))
        
        # Initialize persistence
        self._init_persistence()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _init_persistence(self):
        """Initialize SQLite database for event persistence"""
        with sqlite3.connect(self.persistence_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    source TEXT,
                    timestamp TEXT,
                    priority INTEGER,
                    correlation_id TEXT,
                    data TEXT,
                    tags TEXT,
                    processed INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_type_timestamp ON events(type, timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_correlation ON events(correlation_id)
            """)
    
    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        def cleanup_task():
            while self.running:
                try:
                    self._cleanup_expired_events()
                    self._detect_stale_components()
                    time.sleep(30)
                except Exception as e:
                    logger.error(f"Cleanup task error: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        cleanup_thread.start()
    
    def publish(self, event_type: str, data: Dict[str, Any], source: str, 
                priority: int = 5, correlation_id: str = None, tags: List[str] = None):
        """Publish an event to the ecosystem"""
        event = EcosystemEvent(
            id=str(uuid.uuid4()),
            type=event_type,
            data=data,
            source=source,
            timestamp=datetime.now(),
            priority=priority,
            correlation_id=correlation_id or str(uuid.uuid4()),
            tags=tags or []
        )
        
        # Store in history
        self.event_history.append(event)
        
        # Store correlation
        if event.correlation_id:
            self.active_correlations[event.correlation_id].append(event)
        
        # Persist to database
        self._persist_event(event)
        
        # Update statistics
        self.event_stats[event_type] += 1
        self.component_stats[source]['events_published'] += 1
        
        # Notify subscribers
        self._notify_subscribers(event)
        
        # Update component heartbeat
        self.component_heartbeats[source] = datetime.now()
        
        logger.info(f"📡 Event published: {event_type} from {source}")
        return event.id
    
    def subscribe(self, event_pattern: str, callback: Callable, component: str):
        """Subscribe to events matching pattern"""
        self.subscribers[event_pattern].append(callback)
        self.component_stats[component]['subscriptions'] += 1
        logger.info(f"📻 {component} subscribed to {event_pattern}")
    
    def subscribe_multiple(self, patterns: List[str], callback: Callable, component: str):
        """Subscribe to multiple event patterns with one callback"""
        for pattern in patterns:
            self.subscribe(pattern, callback, component)
    
    def _notify_subscribers(self, event: EcosystemEvent):
        """Notify all matching subscribers of an event"""
        notified_count = 0
        
        # Exact match subscribers
        for callback in self.subscribers.get(event.type, []):
            try:
                callback(event)
                notified_count += 1
            except Exception as e:
                logger.error(f"Subscriber callback failed: {e}")
        
        # Wildcard subscribers (* matches all)
        for callback in self.subscribers.get('*', []):
            try:
                callback(event)
                notified_count += 1
            except Exception as e:
                logger.error(f"Wildcard subscriber failed: {e}")
        
        # Pattern matching (simple prefix matching for now)
        for pattern, callbacks in self.subscribers.items():
            if pattern.endswith('*') and event.type.startswith(pattern[:-1]):
                for callback in callbacks:
                    try:
                        callback(event)
                        notified_count += 1
                    except Exception as e:
                        logger.error(f"Pattern subscriber failed: {e}")
        
        self.event_stats[f"{event.type}_notifications"] = notified_count
    
    def _persist_event(self, event: EcosystemEvent):
        """Persist event to database"""
        try:
            with sqlite3.connect(self.persistence_path) as conn:
                conn.execute("""
                    INSERT INTO events 
                    (id, type, source, timestamp, priority, correlation_id, data, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.id, event.type, event.source, event.timestamp.isoformat(),
                    event.priority, event.correlation_id, 
                    json.dumps(event.data), json.dumps(event.tags)
                ))
        except Exception as e:
            logger.error(f"Failed to persist event: {e}")
    
    def get_correlation_chain(self, correlation_id: str) -> List[EcosystemEvent]:
        """Get all events in a correlation chain"""
        return self.active_correlations.get(correlation_id, [])
    
    def get_recent_events(self, event_type: str = None, limit: int = 100) -> List[EcosystemEvent]:
        """Get recent events, optionally filtered by type"""
        if event_type:
            return [e for e in list(self.event_history)[-limit:] if e.type == event_type]
        return list(self.event_history)[-limit:]
    
    def _cleanup_expired_events(self):
        """Remove expired events from memory"""
        current_time = datetime.now()
        
        # Clean event history
        self.event_history = deque(
            [e for e in self.event_history if not e.is_expired()],
            maxlen=self.event_history.maxlen
        )
        
        # Clean correlations
        for correlation_id in list(self.active_correlations.keys()):
            events = self.active_correlations[correlation_id]
            active_events = [e for e in events if not e.is_expired()]
            if active_events:
                self.active_correlations[correlation_id] = active_events
            else:
                del self.active_correlations[correlation_id]
    
    def _detect_stale_components(self):
        """Detect components that haven't sent heartbeats recently"""
        stale_threshold = datetime.now() - timedelta(minutes=5)
        stale_components = []
        
        for component, last_seen in self.component_heartbeats.items():
            if last_seen < stale_threshold:
                stale_components.append(component)
        
        if stale_components:
            self.publish(
                "ecosystem.components_stale",
                {"stale_components": stale_components},
                "ecosystem_bus",
                priority=3
            )
    
    def get_ecosystem_health(self) -> Dict[str, Any]:
        """Get overall ecosystem health metrics"""
        return {
            "active_components": len(self.component_heartbeats),
            "recent_events": len(self.event_history),
            "active_correlations": len(self.active_correlations),
            "event_types": len(self.event_stats),
            "total_events_processed": sum(self.event_stats.values()),
            "component_health": {
                comp: {
                    "last_seen": heartbeat.isoformat(),
                    "status": "healthy" if datetime.now() - heartbeat < timedelta(minutes=5) else "stale",
                    "stats": dict(self.component_stats[comp])
                }
                for comp, heartbeat in self.component_heartbeats.items()
            }
        }

class EcosystemNeuralNetwork:
    """Central nervous system - pattern detection and intelligence coordination"""
    
    def __init__(self, bus: EcosystemBus):
        self.bus = bus
        self.pattern_memory = {}
        self.success_patterns = defaultdict(list)
        self.failure_patterns = defaultdict(list)
        self.component_capabilities = {}
        self.collaboration_history = []
        self.intelligence_chains = []
        
        # Subscribe to all events for pattern detection
        self.bus.subscribe('*', self._process_event_for_patterns, 'neural_network')
        
        # Start neural processing
        self._start_neural_processing()
    
    def register_component_capabilities(self, component: str, capabilities: Dict[str, Any]):
        """Register what a component can do"""
        self.component_capabilities[component] = capabilities
        self.bus.publish(
            "neural.component_registered",
            {"component": component, "capabilities": capabilities},
            "neural_network"
        )
    
    def request_help(self, requesting_component: str, task_type: str, 
                    context: Dict[str, Any]) -> List[str]:
        """Find components that can help with a specific task"""
        capable_components = []
        
        for component, capabilities in self.component_capabilities.items():
            if component == requesting_component:
                continue
                
            # Check if component has relevant capabilities
            if task_type in capabilities.get('task_types', []):
                capable_components.append(component)
            
            # Check for semantic matches in capabilities
            for capability in capabilities.get('capabilities', []):
                if task_type.lower() in capability.lower():
                    capable_components.append(component)
        
        # Publish help request
        self.bus.publish(
            "neural.help_requested",
            {
                "requesting_component": requesting_component,
                "task_type": task_type,
                "context": context,
                "suggested_helpers": capable_components
            },
            "neural_network",
            correlation_id=context.get('correlation_id')
        )
        
        return capable_components
    
    def learn_collaboration_outcome(self, components: List[str], task: str, 
                                  success: bool, metrics: Dict[str, Any]):
        """Learn from collaboration outcomes"""
        collaboration = {
            "components": sorted(components),
            "task": task,
            "success": success,
            "metrics": metrics,
            "timestamp": datetime.now()
        }
        
        self.collaboration_history.append(collaboration)
        
        if success:
            self.success_patterns[task].append(collaboration)
        else:
            self.failure_patterns[task].append(collaboration)
        
        # Publish learning
        self.bus.publish(
            "neural.collaboration_learned",
            collaboration,
            "neural_network"
        )
    
    def suggest_collaboration(self, task: str, context: Dict[str, Any]) -> List[str]:
        """Suggest best component combination for a task"""
        # Look for successful patterns
        if task in self.success_patterns:
            # Find most recent successful collaboration
            recent_successes = sorted(
                self.success_patterns[task],
                key=lambda x: x['timestamp'],
                reverse=True
            )
            
            if recent_successes:
                return recent_successes[0]['components']
        
        # Fallback to capability matching
        return self.request_help("neural_network", task, context)
    
    def _process_event_for_patterns(self, event: EcosystemEvent):
        """Process events to detect patterns and opportunities"""
        # Pattern: GitHub issue → AkashaOS insight opportunity
        if event.type == "aetherius.issue_discovered":
            relevant_modules = self._find_relevant_akasha_modules(event.data)
            if relevant_modules:
                self.bus.publish(
                    "neural.suggest_module_activation",
                    {
                        "issue": event.data,
                        "suggested_modules": relevant_modules,
                        "reasoning": "GitHub issue matches module capabilities"
                    },
                    "neural_network",
                    correlation_id=event.correlation_id
                )
        
        # Pattern: Mobile note → Problem context
        if event.type == "mobile.note_added":
            current_problem = self._get_current_problem_context()
            if current_problem:
                self.bus.publish(
                    "neural.context_enrichment",
                    {
                        "note": event.data,
                        "problem": current_problem,
                        "suggestion": "Apply note to current problem context"
                    },
                    "neural_network",
                    correlation_id=event.correlation_id
                )
        
        # Pattern: AI response → Knowledge extraction
        if event.type == "hive_mind.response_generated":
            knowledge = self._extract_knowledge_from_response(event.data)
            if knowledge:
                self.bus.publish(
                    "neural.knowledge_extracted",
                    knowledge,
                    "neural_network",
                    correlation_id=event.correlation_id
                )
    
    def _find_relevant_akasha_modules(self, issue_data: Dict) -> List[str]:
        """Find AkashaOS modules relevant to a GitHub issue"""
        issue_text = f"{issue_data.get('title', '')} {issue_data.get('description', '')}"
        relevant_modules = []
        
        # Simple keyword matching (could be enhanced with embeddings)
        module_keywords = {
            'awareness_mod': ['observe', 'monitor', 'track', 'detect'],
            'longing_mod': ['goal', 'desire', 'want', 'need'],
            'plan_mod': ['plan', 'strategy', 'approach', 'solve'],
            'endearment_mod': ['user', 'interaction', 'relationship']
        }
        
        for module, keywords in module_keywords.items():
            if any(keyword in issue_text.lower() for keyword in keywords):
                relevant_modules.append(module)
        
        return relevant_modules
    
    def _get_current_problem_context(self) -> Optional[Dict]:
        """Get current problem being worked on"""
        recent_events = self.bus.get_recent_events("nexus.problem_started", limit=1)
        if recent_events:
            return recent_events[0].data
        return None
    
    def _extract_knowledge_from_response(self, response_data: Dict) -> Optional[Dict]:
        """Extract reusable knowledge from AI responses"""
        # Simple pattern: look for code snippets, solutions, insights
        response_text = response_data.get('response', '')
        
        knowledge = {}
        if 'def ' in response_text or 'class ' in response_text:
            knowledge['type'] = 'code_solution'
            knowledge['content'] = response_text
            knowledge['tags'] = ['code', 'solution']
        elif 'error' in response_text.lower() and 'fix' in response_text.lower():
            knowledge['type'] = 'error_solution'
            knowledge['content'] = response_text
            knowledge['tags'] = ['error', 'fix', 'debugging']
        
        return knowledge if knowledge else None
    
    def _start_neural_processing(self):
        """Start background neural processing"""
        def neural_processing_loop():
            while True:
                try:
                    self._detect_intelligence_opportunities()
                    self._optimize_collaboration_patterns()
                    time.sleep(60)  # Process every minute
                except Exception as e:
                    logger.error(f"Neural processing error: {e}")
        
        neural_thread = threading.Thread(target=neural_processing_loop, daemon=True)
        neural_thread.start()
    
    def _detect_intelligence_opportunities(self):
        """Detect opportunities for cross-component intelligence"""
        # Look for events that could trigger intelligence chains
        recent_events = self.bus.get_recent_events(limit=50)
        
        # Group events by correlation ID
        correlations = defaultdict(list)
        for event in recent_events:
            if event.correlation_id:
                correlations[event.correlation_id].append(event)
        
        # Detect potential intelligence chains
        for correlation_id, events in correlations.items():
            if len(events) > 1:
                chain_opportunity = self._analyze_intelligence_chain(events)
                if chain_opportunity:
                    self.bus.publish(
                        "neural.intelligence_chain_detected",
                        chain_opportunity,
                        "neural_network"
                    )
    
    def _analyze_intelligence_chain(self, events: List[EcosystemEvent]) -> Optional[Dict]:
        """Analyze if events form a productive intelligence chain"""
        event_types = [e.type for e in events]
        
        # Example pattern: discovery → analysis → action → feedback
        productive_patterns = [
            ['aetherius.issue_discovered', 'akasha.insight_generated', 'nexus.problem_queued'],
            ['mobile.note_added', 'neural.context_enrichment', 'akasha.memory_updated'],
            ['hive_mind.query_sent', 'hive_mind.response_generated', 'neural.knowledge_extracted']
        ]
        
        for pattern in productive_patterns:
            if all(event_type in event_types for event_type in pattern):
                return {
                    "pattern_matched": pattern,
                    "events": [e.to_dict() for e in events],
                    "intelligence_chain": True,
                    "suggestion": "This chain shows productive cross-component intelligence"
                }
        
        return None
    
    def _optimize_collaboration_patterns(self):
        """Optimize collaboration patterns based on success history"""
        # Analyze recent collaboration outcomes
        recent_collaborations = [
            c for c in self.collaboration_history
            if datetime.now() - c['timestamp'] < timedelta(days=7)
        ]
        
        if len(recent_collaborations) >= 5:
            # Find most successful patterns
            successful_patterns = defaultdict(list)
            for collab in recent_collaborations:
                if collab['success']:
                    pattern = tuple(sorted(collab['components']))
                    successful_patterns[pattern].append(collab)
            
            # Publish optimization insights
            if successful_patterns:
                self.bus.publish(
                    "neural.collaboration_optimization",
                    {
                        "successful_patterns": {
                            str(pattern): len(collabs)
                            for pattern, collabs in successful_patterns.items()
                        },
                        "recommendation": "Prioritize these component combinations"
                    },
                    "neural_network"
                )

class EcosystemComponent:
    """Base class for ecosystem components with built-in bus integration"""
    
    def __init__(self, component_name: str, bus: EcosystemBus, neural: EcosystemNeuralNetwork):
        self.name = component_name
        self.bus = bus
        self.neural = neural
        self.capabilities = {}
        self.running = True
        
        # Register with neural network
        self.neural.register_component_capabilities(self.name, self.capabilities)
        
        # Subscribe to relevant events
        self.bus.subscribe(f"{self.name}.*", self._handle_direct_event, self.name)
        self.bus.subscribe("neural.*", self._handle_neural_event, self.name)
        self.bus.subscribe("ecosystem.*", self._handle_ecosystem_event, self.name)
        
        # Start heartbeat
        self._start_heartbeat()
    
    def _start_heartbeat(self):
        """Send regular heartbeats to show component is alive"""
        def heartbeat_loop():
            while self.running:
                self.bus.publish(
                    f"{self.name}.heartbeat",
                    {"status": "alive", "capabilities": self.capabilities},
                    self.name,
                    priority=10  # Low priority
                )
                time.sleep(60)
        
        heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        heartbeat_thread.start()
    
    def _handle_direct_event(self, event: EcosystemEvent):
        """Handle events directed at this component"""
        pass
    
    def _handle_neural_event(self, event: EcosystemEvent):
        """Handle neural network events"""
        pass
    
    def _handle_ecosystem_event(self, event: EcosystemEvent):
        """Handle ecosystem-wide events"""
        pass
    
    def publish_event(self, event_type: str, data: Dict[str, Any], 
                     priority: int = 5, correlation_id: str = None):
        """Publish an event from this component"""
        return self.bus.publish(
            f"{self.name}.{event_type}",
            data,
            self.name,
            priority=priority,
            correlation_id=correlation_id
        )
    
    def request_help(self, task_type: str, context: Dict[str, Any]) -> List[str]:
        """Request help from other components"""
        return self.neural.request_help(self.name, task_type, context)
    
    def shutdown(self):
        """Gracefully shutdown the component"""
        self.running = False
        self.publish_event("shutdown", {"reason": "graceful_shutdown"})

def main():
    """Demo of the ecosystem running"""
    # Initialize the circulatory system
    bus = EcosystemBus()
    neural = EcosystemNeuralNetwork(bus)
    
    # Create some demo components
    class DemoAkashaOS(EcosystemComponent):
        def __init__(self, bus, neural):
            super().__init__("akasha_os", bus, neural)
            self.capabilities = {
                "task_types": ["introspection", "memory_management", "pattern_detection"],
                "capabilities": ["observe", "remember", "analyze", "introspect"]
            }
            neural.register_component_capabilities(self.name, self.capabilities)
        
        def _handle_neural_event(self, event: EcosystemEvent):
            if event.type == "neural.suggest_module_activation":
                self.publish_event(
                    "modules_activated",
                    {"modules": event.data["suggested_modules"], "reason": event.data["reasoning"]},
                    correlation_id=event.correlation_id
                )
    
    class DemoAetherius(EcosystemComponent):
        def __init__(self, bus, neural):
            super().__init__("aetherius", bus, neural)
            self.capabilities = {
                "task_types": ["github_scanning", "issue_analysis", "automation"],
                "capabilities": ["scan", "analyze", "automate", "prioritize"]
            }
            neural.register_component_capabilities(self.name, self.capabilities)
        
        def discover_issue(self):
            self.publish_event(
                "issue_discovered",
                {
                    "title": "Implement user authentication",
                    "description": "Need to add OAuth2 authentication system",
                    "priority": "high",
                    "url": "https://github.com/example/repo/issues/123"
                },
                priority=3
            )
    
    # Start demo components
    akasha = DemoAkashaOS(bus, neural)
    aetherius = DemoAetherius(bus, neural)
    
    print("🧠 Ecosystem Central Nervous System Started")
    print("🩸 Circulatory System Online")
    print("\nDemo: Discovering a GitHub issue...")
    
    # Simulate ecosystem activity
    aetherius.discover_issue()
    
    # Let the system process for a bit
    time.sleep(2)
    
    # Show ecosystem health
    health = bus.get_ecosystem_health()
    print(f"\n📊 Ecosystem Health: {json.dumps(health, indent=2)}")
    
    print("\n✅ The triops are alive and the ecosystem is circulating!")

if __name__ == "__main__":
    main()
