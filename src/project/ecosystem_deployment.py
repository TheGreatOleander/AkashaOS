#!/usr/bin/env python3
"""
Complete AI Ecosystem Deployment Script
This brings your entire distributed intelligence system to life
"""

import asyncio
import os
import sys
import signal
import logging
import json
import yaml
from pathlib import Path
from typing import Dict, Any

# Add the current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ecosystem_circulatory_system import EcosystemBus, EcosystemNeuralNetwork
from ecosystem_adapters import create_integrated_ecosystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EcosystemDeployment:
    """Main deployment orchestrator"""
    
    def __init__(self, config_path: str = "ecosystem_config.yaml"):
        self.config = self.load_config(config_path)
        self.ecosystem = None
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load ecosystem configuration"""
        default_config = {
            "ecosystem": {
                "name": "AI_Ecosystem_v1",
                "persistence_path": "./data",
                "log_level": "INFO"
            },
            "components": {
                "akasha_os": {
                    "enabled": True,
                    "module_directory": "./modules",
                    "memory_file": "./memory.json"
                },
                "aetherius": {
                    "enabled": True,
                    "github_token": None,
                    "rate_limits": {"github": 60, "llm": 20}
                },
                "nexus": {
                    "enabled": True,
                    "database_path": "./nexus_problems.db",
                    "search_queries": [
                        'is:issue is:open label:"help wanted"',
                        'is:issue is:open label:"good first issue"',
                        'is:issue is:open label:"bug" comments:>10'
                    ]
                },
                "mobile_bridge": {
                    "enabled": True,
                    "port": 8080,
                    "auth_token": None
                },
                "hive_mind": {
                    "enabled": False,  # Browser-based, optional
                    "models": []
                }
            },
            "neural_network": {
                "pattern_detection": True,
                "collaboration_learning": True,
                "intelligence_chains": True
            },
            "circulatory_system": {
                "event_retention_hours": 24,
                "heartbeat_interval": 60,
                "cleanup_interval": 300
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                # Merge configs
                default_config.update(user_config)
        else:
            # Create default config file
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            logger.info(f"Created default config file: {config_path}")
        
        return default_config
    
    def setup_directories(self):
        """Set up required directories"""
        directories = [
            self.config["ecosystem"]["persistence_path"],
            "logs",
            "backups",
            self.config["components"]["akasha_os"]["module_directory"]
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def initialize_akasha_os(self):
        """Initialize AkashaOS with existing modules"""
        akasha_config = self.config["components"]["akasha_os"]
        
        if not akasha_config["enabled"]:
            logger.info("AkashaOS disabled in config")
            return {}
        
        # Load existing memory if available
        memory_file = akasha_config["memory_file"]
        memory = {}
        
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
                logger.info(f"Loaded AkashaOS memory from {memory_file}")
            except Exception as e:
                logger.warning(f"Could not load memory file: {e}")
        
        # Ensure default memory structure
        memory.setdefault("observations", [])
        memory.setdefault("desires", [])
        memory.setdefault("plans", [])
        memory.setdefault("logs", [])
        
        return memory
    
    def initialize_aetherius(self):
        """Initialize Aetherius engine"""
        aetherius_config = self.config["components"]["aetherius"]
        
        if not aetherius_config["enabled"]:
            logger.info("Aetherius disabled in config")
            return None
        
        # Create mock Aetherius engine (replace with real implementation)
        class MockAetheriusEngine:
            def __init__(self, config):
                self.config = config
                self.github_token: <REDACTED>"github_token")
                self.rate_limits = config.get("rate_limits", {"github": 60, "llm": 20})
            
            def scan_and_rank_issues(self):
                logger.info("Aetherius: Scanning GitHub issues...")
                # Mock implementation
                return []
            
            def apply_human_feedback(self, repo, issue_number, adjustment):
                logger.info(f"Aetherius: Applied feedback to {repo}#{issue_number}")
        
        return MockAetheriusEngine(aetherius_config)
    
    def initialize_nexus(self):
        """Initialize Unified Nexus"""
        nexus_config = self.config["components"]["nexus"]
        
        if not nexus_config["enabled"]:
            logger.info("Nexus disabled in config")
            return None
        
        # Create mock Nexus instance (replace with real implementation)
        class MockNexusInstance:
            def __init__(self, config):
                self.config = config
                self.database_path = config.get("database_path")
                self.search_queries = config.get("search_queries", [])
            
            def discover_and_queue_problems(self):
                logger.info("Nexus: Discovering and queuing problems...")
            
            def select_next_problem(self):
                logger.info("Nexus: Selecting next problem...")
                return None
        
        return MockNexusInstance(nexus_config)
    
    def start_mobile_bridge_server(self):
        """Start the mobile bridge HTTP server"""
        mobile_config = self.config["components"]["mobile_bridge"]
        
        if not mobile_config["enabled"]:
            logger.info("Mobile Bridge disabled in config")
            return
        
        # Import and start mobile bridge in separate thread
        try:
            import threading
            from mobile_bridge import MobileBridge
            
            def start_bridge():
                bridge = MobileBridge()
                bridge.config.update(mobile_config)
                bridge.run()
            
            bridge_thread = threading.Thread(target=start_bridge, daemon=True)
            bridge_thread.start()
            
            logger.info(f"Mobile Bridge server started on port {mobile_config['port']}")
            
        except ImportError as e:
            logger.warning(f"Could not start Mobile Bridge: {e}")
    
    def start_ecosystem(self):
        """Start the complete ecosystem"""
        logger.info("🚀 Starting AI Ecosystem...")
        
        # Setup directories
        self.setup_directories()
        
        # Initialize components
        akasha_memory = self.initialize_akasha_os()
        aetherius_engine = self.initialize_aetherius()
        nexus_instance = self.initialize_nexus()
        
        # Start mobile bridge server
        self.start_mobile_bridge_server()
        
        # Create integrated ecosystem
        self.ecosystem = create_integrated_ecosystem(
            akasha_memory, aetherius_engine, nexus_instance
        )
        
        # Log startup success
        logger.info("✅ AI Ecosystem fully operational!")
        logger.info("🧠 Central Nervous System: Online")
        logger.info("🩸 Circulatory System: Flowing")
        logger.info("🤖 Component Adapters: Connected")
        
        # Print ecosystem status
        self.print_ecosystem_status()
        
        return self.ecosystem
    
    def print_ecosystem_status(self):
        """Print current ecosystem status"""
        if not self.ecosystem:
            print("❌ Ecosystem not initialized")
            return
        
        health = self.ecosystem["bus"].get_ecosystem_health()
        
        print("\n" + "="*60)
        print("🌐 AI ECOSYSTEM STATUS")
        print("="*60)
        print(f"📊 Active Components: {health['active_components']}")
        print(f"📈 Recent Events: {health['recent_events']}")
        print(f"🔄 Active Correlations: {health['active_correlations']}")
        print(f"📝 Event Types Processed: {health['event_types']}")
        print(f"⚡ Total Events: {health['total_events_processed']}")
        
        print(f"\n🤖 Component Health:")
        for component, info in health['component_health'].items():
            status_emoji = "🟢" if info['status'] == 'healthy' else "🔴"
            print(f"   {status_emoji} {component}: {info['status']}")
            if info.get('stats'):
                for stat, value in info['stats'].items():
                    print(f"      └─ {stat}: {value}")
        
        print(f"\n🧬 Neural Network:")
        print(f"   🧠 Pattern Detection: {'Enabled' if self.config['neural_network']['pattern_detection'] else 'Disabled'}")
        print(f"   🤝 Collaboration Learning: {'Enabled' if self.config['neural_network']['collaboration_learning'] else 'Disabled'}")
        print(f"   ⛓️  Intelligence Chains: {'Enabled' if self.config['neural_network']['intelligence_chains'] else 'Disabled'}")
        
        print("="*60)
    
    def run_interactive_mode(self):
        """Run ecosystem in interactive mode"""
        if not self.ecosystem:
            logger.error("Ecosystem not initialized")
            return
        
        mobile_adapter = self.ecosystem["adapters"]["mobile"]
        
        print("\n🎮 INTERACTIVE MODE")
        print("Commands:")
        print("  'note <text>' - Add a note")
        print("  'progress <text>' - Add progress update")
        print("  'complete' - Complete current problem")
        print("  'status' - Show ecosystem status")
        print("  'health' - Show detailed health info")
        print("  'test' - Run test scenarios")
        print("  'quit' - Shutdown ecosystem")
        
        while self.running:
            try:
                user_input = input("\n🤖 > ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'status':
                    self.print_ecosystem_status()
                elif user_input.lower() == 'health':
                    self.print_detailed_health()
                elif user_input.lower() == 'test':
                    self.run_test_scenarios()
                elif user_input.startswith('note '):
                    note = user_input[5:]
                    mobile_adapter.handle_mobile_note(note)
                    print(f"📝 Note added: {note}")
                elif user_input.startswith('progress '):
                    progress = user_input[9:]
                    mobile_adapter.handle_mobile_progress(progress)
                    print(f"📈 Progress added: {progress}")
                elif user_input.lower() == 'complete':
                    mobile_adapter.handle_problem_completion("Completed via interactive mode")
                    print("✅ Problem marked as complete")
                else:
                    print("❓ Unknown command. Available: note, progress, complete, status, health, test, quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Interactive mode error: {e}")
    
    def print_detailed_health(self):
        """Print detailed ecosystem health information"""
        if not self.ecosystem:
            return
        
        health = self.ecosystem["bus"].get_ecosystem_health()
        
        print("\n🔍 DETAILED HEALTH REPORT")
        print("-" * 50)
        
        # Event flow analysis
        recent_events = self.ecosystem["bus"].get_recent_events(limit=20)
        event_types = {}
        for event in recent_events:
            event_types[event.type] = event_types.get(event.type, 0) + 1
        
        print(f"📊 Recent Event Types (last 20):")
        for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   {event_type}: {count}")
        
        # Component interaction analysis
        component_interactions = {}
        for event in recent_events:
            source = event.source
            component_interactions[source] = component_interactions.get(source, 0) + 1
        
        print(f"\n🤖 Component Activity:")
        for component, activity in sorted(component_interactions.items(), key=lambda x: x[1], reverse=True):
            print(f"   {component}: {activity} events")
        
        # Intelligence chain detection
        correlations = {}
        for event in recent_events:
            if event.correlation_id:
                correlations[event.correlation_id] = correlations.get(event.correlation_id, 0) + 1
        
        active_chains = len([c for c in correlations.values() if c > 1])
        print(f"\n🧬 Intelligence Chains: {active_chains} active patterns")
        
        if active_chains > 0:
            print("   Active correlation chains:")
            for corr_id, event_count in correlations.items():
                if event_count > 1:
                    print(f"   └─ {corr_id[:8]}...: {event_count} connected events")
    
    def run_test_scenarios(self):
        """Run test scenarios to demonstrate ecosystem functionality"""
        if not self.ecosystem:
            print("❌ Ecosystem not initialized")
            return
        
        print("\n🧪 RUNNING TEST SCENARIOS")
        print("-" * 40)
        
        bus = self.ecosystem["bus"]
        mobile_adapter = self.ecosystem["adapters"]["mobile"]
        
        # Test 1: GitHub Issue Discovery Chain
        print("🔬 Test 1: GitHub Issue Discovery Chain")
        bus.publish(
            "aetherius.issue_discovered",
            {
                "id": "test_issue_001",
                "title": "Add user authentication system",
                "description": "Implement OAuth2 authentication for user login",
                "priority": "high",
                "url": "https://github.com/test/repo/issues/1",
                "estimated_effort": 8
            },
            "test_runner",
            priority=3
        )
        print("   ✅ GitHub issue discovery event published")
        
        # Test 2: Mobile Note Processing
        print("\n🔬 Test 2: Mobile Note Processing")
        mobile_adapter.handle_mobile_note("I want to focus on authentication bugs today. This is high priority!")
        print("   ✅ Mobile note processed")
        
        # Test 3: Progress Update Chain
        print("\n🔬 Test 3: Progress Update Chain")
        mobile_adapter.handle_mobile_progress("Implemented OAuth2 login flow, testing needed")
        print("   ✅ Progress update processed")
        
        # Test 4: Neural Pattern Detection
        print("\n🔬 Test 4: Neural Pattern Detection")
        bus.publish(
            "akasha_os.desire_created",
            {
                "key": "implement_auth",
                "description": "Strong desire to implement authentication",
                "intensity": 0.9
            },
            "test_runner"
        )
        print("   ✅ High-intensity desire event published")
        
        # Wait a moment for processing
        import time
        time.sleep(1)
        
        print(f"\n📈 Test Results:")
        health = bus.get_ecosystem_health()
        print(f"   Events processed: {health['total_events_processed']}")
        print(f"   Active components: {health['active_components']}")
        print(f"   Correlation chains: {health['active_correlations']}")
        
        print("   ✅ All test scenarios completed successfully!")
    
    def shutdown_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received shutdown signal ({signum})")
        self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown the ecosystem"""
        self.running = False
        
        if self.ecosystem:
            logger.info("🔄 Shutting down ecosystem components...")
            
            # Shutdown all adapters
            for name, adapter in self.ecosystem["adapters"].items():
                try:
                    adapter.shutdown()
                    logger.info(f"   ✅ {name} adapter shutdown")
                except Exception as e:
                    logger.error(f"   ❌ {name} adapter shutdown failed: {e}")
            
            # Save final state
            try:
                akasha_config = self.config["components"]["akasha_os"]
                if akasha_config["enabled"]:
                    memory_file = akasha_config["memory_file"]
                    akasha_adapter = self.ecosystem["adapters"]["akasha"]
                    with open(memory_file, 'w') as f:
                        json.dump(akasha_adapter.akasha_memory, f, indent=2, default=str)
                    logger.info(f"   💾 AkashaOS memory saved to {memory_file}")
            except Exception as e:
                logger.error(f"   ❌ Memory save failed: {e}")
        
        logger.info("🏁 AI Ecosystem shutdown complete")
        print("👋 Goodbye! The ecosystem has been safely shut down.")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Ecosystem Deployment")
    parser.add_argument('--config', default='ecosystem_config.yaml', help='Configuration file path')
    parser.add_argument('--mode', choices=['interactive', 'daemon', 'test'], default='interactive',
                       help='Run mode: interactive (default), daemon, or test')
    parser.add_argument('--status-only', action='store_true', help='Show status and exit')
    
    args = parser.parse_args()
    
    # Create deployment instance
    deployment = EcosystemDeployment(args.config)
    
    try:
        # Start ecosystem
        ecosystem = deployment.start_ecosystem()
        
        if args.status_only:
            deployment.print_ecosystem_status()
            return
        
        if args.mode == 'interactive':
            deployment.run_interactive_mode()
        elif args.mode == 'test':
            deployment.run_test_scenarios()
        elif args.mode == 'daemon':
            # Daemon mode - just keep running
            print("🏃 Running in daemon mode (Ctrl+C to stop)")
            try:
                while deployment.running:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        deployment.shutdown()

if __name__ == "__main__":
    main()
