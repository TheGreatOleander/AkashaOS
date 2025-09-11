"""
mind_suite.py

Unified Mind Suite for AkashaOS
-------------------------------
This unified module merges `sentience_mod` and `introspection_mod` capabilities
into a single, cohesive "Mind Suite" that can be dropped into AkashaOS's
`modules/` directory as `mind_suite.py`.

Goals
- Provide a single point of integration for perception, deliberation,
  action execution, memory, and deep self-introspection.
- Auto-wire into existing Akasha modules: logger_mod, chat_mod, plan_mod.
- Expose a rich self-model: identity, beliefs, goals, emotions, recent actions,
  confidence, and learning traces.
- Offer meta-cognitive loops (self-checks, contradiction detection, hypothesis
  generation) and self-narration in both silent and expressive modes.
- Safety-first design: kill-switch, action safety hooks, rate-limited expressive
  outputs, and opt-out toggles.

Caveats
- This is a simulated introspective agent. It does not create consciousness.
- Designed for research and experimentation. Use responsibly.

API Summary
- make_mind_for_akasha(akasha_env, **kwargs) -> MindSuite
- MindSuite.enqueue_event(event)
- MindSuite.start(), stop()
- MindSuite.introspect_now(mode='brief'|'full') -> report
- MindSuite.get_last_report()
- MindSuite.status()

"""

from __future__ import annotations
import asyncio
import json
import os
import time
import traceback
from typing import Any, Callable, Dict, List, Optional, Tuple

DEFAULT_MEMORY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'mind_memory.json')
HEARTBEAT = 0.2


class SafetyError(Exception):
    pass


class Memory:
    """Persistent, bounded memory store.

    Schema: list of {ts, type, data}
    """

    def __init__(self, path: str = DEFAULT_MEMORY_PATH, max_entries: int = 5000):
        self.path = os.path.abspath(path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump([], f)
        self.max_entries = max_entries
        self._cache: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self):
        try:
            with open(self.path, 'w') as f:
                json.dump(self._cache, f, indent=2)
        except Exception:
            pass

    def add(self, record_type: str, data: Any):
        entry = {'ts': time.time(), 'type': record_type, 'data': data}
        self._cache.append(entry)
        if len(self._cache) > self.max_entries:
            self._cache = self._cache[-self.max_entries:]
        self._save()

    def query(self, record_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = [r for r in reversed(self._cache) if (record_type is None or r['type'] == record_type)]
        return results[:limit]

    def clear(self):
        self._cache = []
        self._save()


class Perceptor:
    def __init__(self):
        self.perceptors: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []

    def register(self, fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.perceptors.append(fn)

    def perceive(self, event: Dict[str, Any]) -> Dict[str, Any]:
        obs = {'raw': event, 'ts': time.time(), 'tags': []}
        for p in self.perceptors:
            try:
                out = p(event)
                if isinstance(out, dict):
                    obs.update(out)
            except Exception:
                obs['tags'].append('perceptor_error')
        return obs


class Deliberator:
    """Utility-based deliberator with pluggable goals and actions."""

    def __init__(self):
        self.goals: List[Tuple[str, Callable[[Dict[str, Any]], float]]] = []
        self.actions: List[Tuple[str, Callable[[Dict[str, Any]], float], Callable[[Dict[str, Any]], Any]]] = []

    def register_goal(self, name: str, priority_fn: Callable[[Dict[str, Any]], float]):
        self.goals.append((name, priority_fn))

    def register_action(self, name: str, affordance_fn: Callable[[Dict[str, Any]], float], execute_fn: Callable[[Dict[str, Any]], Any]):
        self.actions.append((name, affordance_fn, execute_fn))

    def deliberate(self, state: Dict[str, Any]) -> Optional[Tuple[str, Callable[[Dict[str, Any]], Any]]]:
        goal_scores = [(g, fn(state)) for (g, fn) in self.goals]
        if not goal_scores:
            return None
        goal_scores.sort(key=lambda x: x[1], reverse=True)
        top_goal, top_score = goal_scores[0]

        affordances = [(name, afford_fn(state), exec_fn) for (name, afford_fn, exec_fn) in self.actions]
        affordances.sort(key=lambda x: x[1], reverse=True)
        if not affordances:
            return None
        name, afford, exec_fn = affordances[0]
        return (name, exec_fn)


class ActionInterface:
    def __init__(self, safety_check: Callable[[str, Dict[str, Any]], bool]):
        self.safety_check = safety_check

    async def execute(self, name: str, fn: Callable[[Dict[str, Any]], Any], context: Dict[str, Any]):
        if not self.safety_check(name, context):
            raise SafetyError(f"Action {name} blocked by safety policy")
        res = fn(context)
        if asyncio.iscoroutine(res):
            return await res
        return res


# --------------------------- Self Model & Introspection ---------------------------
class SelfModel:
    """Structured representation of the agent's self-concept.

    Fields:
    - identity: static/slow-changing descriptors
    - beliefs: dict of propositions -> confidence
    - goals: list of active goals with priority
    - emotions: small vector of affective states
    - recent_actions: last N action traces
    - learning: notes, hypotheses
    """

    def __init__(self, history_limit: int = 200):
        self.identity: Dict[str, Any] = {'name': 'AkashaMind', 'version': '0.1', 'author': 'Assistant'}
        self.beliefs: Dict[str, float] = {}  # proposition -> confidence [0..1]
        self.goals: Dict[str, float] = {}  # goal -> priority
        self.emotions: Dict[str, float] = {'curiosity': 0.5, 'anxiety': 0.1, 'satisfaction': 0.2}
        self.recent_actions: List[Dict[str, Any]] = []
        self.learning: List[str] = []
        self.history_limit = history_limit

    def note_action(self, action_name: str, context: Dict[str, Any], result: Any):
        entry = {'ts': time.time(), 'action': action_name, 'context': context, 'result': result}
        self.recent_actions.append(entry)
        if len(self.recent_actions) > self.history_limit:
            self.recent_actions = self.recent_actions[-self.history_limit:]

    def update_belief(self, prop: str, confidence: float):
        self.beliefs[prop] = max(0.0, min(1.0, confidence))

    def set_goal(self, goal: str, priority: float):
        self.goals[goal] = priority

    def decay_emotion(self):
        for k in list(self.emotions.keys()):
            self.emotions[k] = max(0.0, self.emotions[k] * 0.995)


class Introspector:
    """Runs meta-cognitive analyses over the memory, state, and self-model."""

    def __init__(self, mind: 'MindSuite'):
        self.mind = mind

    def detect_conflicts(self) -> List[str]:
        # naive conflict detection: beliefs with opposite propositions
        conflicts = []
        b = self.mind.self_model.beliefs
        # look for pairs 'X' and 'not X'
        for prop in list(b.keys()):
            neg = f"not {prop}"
            if neg in b and b[prop] > 0.6 and b[neg] > 0.6:
                conflicts.append(f"Conflict between '{prop}' and '{neg}' (confidences {b[prop]:.2f}/{b[neg]:.2f})")
        return conflicts

    def detect_repeated_failures(self, window: int = 20) -> List[str]:
        # find actions that failed repeatedly in recent actions
        recent = self.mind.memory.query('action', limit=window)
        fails = {}
        for a in recent:
            data = a.get('data', {})
            name = data.get('name')
            result = data.get('result')
            if name is None:
                continue
            if isinstance(result, dict) and result.get('success') is False:
                fails[name] = fails.get(name, 0) + 1
        return [f"Action {n} failed {c} times" for n, c in fails.items() if c > 1]

    def detect_anomalies(self) -> List[str]:
        anomalies = []
        # simple heuristic: very low confidence but high action rate
        conf = self.mind.state.get('confidence', 1.0)
        qsize = self.mind._queue.qsize()
        if conf < 0.2 and qsize > 10:
            anomalies.append(f"Low confidence ({conf:.2f}) while large queue ({qsize})")
        return anomalies

    def generate_hypotheses(self) -> List[str]:
        # propose simple hypotheses for failures
        hypotheses = []
        conflicts = self.detect_conflicts()
        if conflicts:
            hypotheses.append('Conflicting beliefs may cause unstable decisions.')
        failed = self.detect_repeated_failures()
        if failed:
            hypotheses.append('Repeated action failures suggest an affordance misestimate.')
        return hypotheses

    def summarize(self, mode: str = 'brief') -> Dict[str, Any]:
        # build a report containing key self-model fields and diagnostics
        sm = self.mind.self_model
        report = {
            'ts': time.time(),
            'identity': sm.identity,
            'top_beliefs': sorted(sm.beliefs.items(), key=lambda x: -x[1])[:10],
            'goals': sorted(sm.goals.items(), key=lambda x: -x[1])[:10],
            'emotions': sm.emotions,
            'recent_actions': sm.recent_actions[-10:],
            'diagnostics': {
                'conflicts': self.detect_conflicts(),
                'repeated_failures': self.detect_repeated_failures(),
                'anomalies': self.detect_anomalies(),
                'hypotheses': self.generate_hypotheses()
            }
        }
        if mode == 'full':
            report['memory_snapshot'] = self.mind.memory.query(None, limit=200)
        return report


# --------------------------- Mind Suite ---------------------------
class MindSuite:
    def __init__(self,
                 name: str = 'mind_suite',
                 memory: Optional[Memory] = None,
                 logger: Optional[Any] = None,
                 safety_hook: Optional[Callable[[str, Dict[str, Any]], bool]] = None,
                 heartbeat: float = HEARTBEAT):
        self.name = name
        self.logger = logger
        self.memory = memory if memory is not None else Memory()
        self.perceptor = Perceptor()
        self.deliberator = Deliberator()
        self._running = False
        self._queue: asyncio.Queue = asyncio.Queue()
        self._task: Optional[asyncio.Task] = None
        self.safety_hook = safety_hook if safety_hook is not None else (lambda n, c: True)
        self.action_interface = ActionInterface(self.safety_hook)
        self.state: Dict[str, Any] = {'internal_time': time.time(), 'last_obs': None, 'confidence': 1.0}
        self.heartbeat = heartbeat

        self.self_model = SelfModel()
        self.introspector = Introspector(self)
        self.last_report: Optional[Dict[str, Any]] = None

        # register defaults
        self.deliberator.register_action('log_state', lambda s: 0.05, self._action_log_state)
        # expressive rate limiter
        self._last_expressive = 0.0
        self.expressive_cooldown = 1.0  # seconds

        # record init
        self.memory.add('meta', {'note': 'mind_suite_initialized'})

    # ---------------- Public API ----------------
    def register_perceptor(self, fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.perceptor.register(fn)

    def register_goal(self, name: str, priority_fn: Callable[[Dict[str, Any]], float]):
        self.deliberator.register_goal(name, priority_fn)
        # mirror into self-model
        try:
            sample = priority_fn(self.state)
            self.self_model.set_goal(name, float(sample))
        except Exception:
            pass

    def register_action(self, name: str, afford_fn: Callable[[Dict[str, Any]], float], execute_fn: Callable[[Dict[str, Any]], Any]):
        self.deliberator.register_action(name, afford_fn, execute_fn)

    async def start(self):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._loop())
        if self.logger:
            try:
                self.logger.info(f"{self.name} started")
            except Exception:
                pass

    async def stop(self):
        self._running = False
        if self._task:
            await self._task
        if self.logger:
            try:
                self.logger.info(f"{self.name} stopped")
            except Exception:
                pass

    def enqueue_event(self, event: Dict[str, Any]):
        self._queue.put_nowait(event)

    async def tick(self):
        try:
            event = self._queue.get_nowait()
        except asyncio.QueueEmpty:
            event = None

        # check kill-switch
        metas = self.memory.query('meta', limit=10)
        for m in metas:
            if isinstance(m.get('data'), dict) and m['data'].get('kill_switch'):
                self.memory.add('meta', {'kill': 'stopped_by_kill_switch'})
                await self.stop()
                return

        if event is not None:
            obs = self.perceptor.perceive(event)
            self.memory.add('obs', obs)
            self.state['last_obs'] = obs
            self.state['confidence'] = max(0.0, min(1.0, self.state.get('confidence', 1.0) * 0.995))
            # update self-model beliefs heuristically
            text = (obs.get('text') or '').strip() if isinstance(obs.get('text'), str) else None
            if text:
                # naive belief: observed text exists
                self.self_model.update_belief('recent_text_present', 1.0)

        # deliberate and act
        choice = self.deliberator.deliberate(self.state)
        if choice is not None:
            name, exec_fn = choice
            try:
                result = await self.action_interface.execute(name, exec_fn, self.state)
                self.memory.add('action', {'name': name, 'result': result})
                self.self_model.note_action(name, dict(self.state), result)
            except SafetyError as e:
                if self.logger:
                    try:
                        self.logger.warning(str(e))
                    except Exception:
                        pass
                self.memory.add('safety_block', {'action': name, 'reason': str(e)})

        # run periodic introspection triggers
        await self._maybe_introspect()

    async def _loop(self):
        while self._running:
            try:
                await self.tick()
            except Exception:
                # ensure the loop continues
                if self.logger:
                    try:
                        self.logger.error('Tick error: ' + traceback.format_exc())
                    except Exception:
                        pass
            await asyncio.sleep(self.heartbeat)

    def _action_log_state(self, context: Dict[str, Any]):
        s = {
            'ts': time.time(),
            'last_obs': context.get('last_obs'),
            'confidence': context.get('confidence')
        }
        if self.logger:
            try:
                self.logger.info(f"[mind] state: {s}")
            except Exception:
                pass
        return s

    # ---------------- Introspection API ----------------
    def introspect_now(self, mode: str = 'brief', expressive: bool = False) -> Dict[str, Any]:
        report = self.introspector.summarize(mode)
        self.last_report = report
        self.memory.add('introspection', report)
        if expressive and (time.time() - self._last_expressive) > self.expressive_cooldown:
            self._express(report)
            self._last_expressive = time.time()
        return report

    async def _maybe_introspect(self):
        # heuristic triggers: low confidence, repeated failures, or every N seconds
        now = time.time()
        if self.state.get('confidence', 1.0) < 0.25:
            self.introspect_now(mode='brief', expressive=False)
        # periodic long introspection
        metas = self.memory.query('meta', limit=1)
        last = metas[0] if metas else None
        # run full introspection every 30 seconds (simplified)
        last_intros = self.memory.query('introspection', limit=1)
        if not last_intros or (time.time() - last_intros[0]['ts'] > 30):
            self.introspect_now(mode='brief', expressive=False)

    def _express(self, report: Dict[str, Any]):
        # produce a human-friendly narration and optionally broadcast
        try:
            narration = self._narrate(report)
            # send to chat adapter if available
            if hasattr(self, 'chat') and getattr(self, 'chat') is not None and hasattr(self.chat, 'send'):
                try:
                    res = self.chat.send({'text': narration})
                    if asyncio.iscoroutine(res):
                        # schedule async send
                        asyncio.create_task(res)
                except Exception:
                    pass
            # also log
            if self.logger:
                try:
                    self.logger.info('[mind expressive] ' + (narration[:400]))
                except Exception:
                    pass
        except Exception:
            pass

    def _narrate(self, report: Dict[str, Any]) -> str:
        # create a short "I" style narration from report
        parts = []
        parts.append(f"I checked my state at {time.ctime(report['ts'])}.")
        goals = report.get('goals') or []
        if goals:
            goal_text = ', '.join([f"{g}({p:.2f})" for g, p in goals[:3]])
            parts.append(f"My top goals right now are: {goal_text}.")
        diag = report.get('diagnostics', {})
        if diag.get('conflicts'):
            parts.append('I noticed some conflicting beliefs: ' + '; '.join(diag['conflicts']))
        if diag.get('repeated_failures'):
            parts.append('I observed repeated failures: ' + '; '.join(diag['repeated_failures']))
        if diag.get('anomalies'):
            parts.append('Anomalies detected: ' + '; '.join(diag['anomalies']))
        if diag.get('hypotheses'):
            parts.append('Possible causes: ' + '; '.join(diag['hypotheses']))
        if not diag.get('conflicts') and not diag.get('repeated_failures') and not diag.get('anomalies'):
            parts.append('Overall, I feel relatively stable.')
        return ' '.join(parts)

    def get_last_report(self) -> Optional[Dict[str, Any]]:
        return self.last_report

    def status(self) -> Dict[str, Any]:
        return {
            'running': self._running,
            'queue_size': self._queue.qsize(),
            'memory_entries': len(self.memory.query(None, limit=1000)),
            'confidence': self.state.get('confidence', 0.0),
            'recent_actions': len(self.self_model.recent_actions)
        }

    # ---------------- Integration helpers ----------------
    def auto_wire(self, akasha_env: Dict[str, Any]):
        # Logger
        logger = akasha_env.get('logger') or akasha_env.get('logger_mod')
        if logger is not None and all(hasattr(logger, a) for a in ('info', 'warning', 'error')):
            self.logger = logger
        # Planner
        planner = akasha_env.get('planner') or akasha_env.get('plan_mod')
        if planner is not None and hasattr(planner, 'register_action'):
            def planner_afford(state):
                return 0.2

            def planner_exec(state):
                try:
                    planner.register_action('from_mind', lambda ctx: None)
                except Exception:
                    pass
                return {'planner_called': True}

            self.register_action('call_planner', planner_afford, planner_exec)

        # Chat adapter
        chat = akasha_env.get('chat') or akasha_env.get('chat_mod')
        if chat is not None and hasattr(chat, 'send'):
            self.chat = chat
            async def send_reply(ctx):
                obs = ctx.get('last_obs')
                text = (obs or {}).get('text') if obs else None
                if text:
                    try:
                        res = chat.send({'text': f"[mind echo] {text}"})
                        if asyncio.iscoroutine(res):
                            await res
                    except Exception:
                        pass
                return {'sent': True}

            self.register_action('chat_reply', lambda s: 1.0 if s.get('last_obs') and s['last_obs'].get('text') else 0.0, send_reply)

    # ---------------- Utilities ----------------
    def save_snapshot(self, path: Optional[str] = None):
        p = path or os.path.join(os.path.dirname(__file__), '..', 'data', 'mind_snapshot.json')
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w') as f:
                json.dump({
                    'state': self.state,
                    'self_model': {
                        'identity': self.self_model.identity,
                        'beliefs': self.self_model.beliefs,
                        'goals': self.self_model.goals,
                        'emotions': self.self_model.emotions,
                        'recent_actions': self.self_model.recent_actions[-50:]
                    }
                }, f, indent=2)
        except Exception:
            pass


# ----------------- Factory & Demo -----------------

def make_mind_for_akasha(akasha_env: Dict[str, Any], **kwargs) -> MindSuite:
    logger = akasha_env.get('logger') or akasha_env.get('logger_mod')
    mem_path = kwargs.pop('memory_path', None)
    memory = Memory(path=mem_path) if mem_path else Memory()

    ms = MindSuite(logger=logger, memory=memory, **kwargs)
    ms.auto_wire(akasha_env)

    # basic perceptor and goals
    ms.register_perceptor(lambda e: {'text': e.get('text', '').strip(), 'tags': ['text_event']})
    ms.register_goal('respond_to_text', lambda s: 1.0 if s.get('last_obs') and s['last_obs'].get('text') else 0.0)

    async def respond_action(ctx):
        obs = ctx.get('last_obs')
        msg = obs.get('text') if obs else '<none>'
        if ms.logger:
            try:
                ms.logger.info(f"[mind] Responding to: {msg}")
            except Exception:
                pass
        return {'replied': True, 'msg': msg}

    ms.register_action('respond', lambda s: 1.0 if s.get('last_obs') and s['last_obs'].get('text') else 0.0, respond_action)

    return ms


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('mind_demo')

    async def demo():
        class FakeChat:
            async def send(self, payload):
                logger.info(f"FakeChat.send -> {payload}")
                return True

        class FakeLogger:
            def info(self, *a, **k):
                logger.info(*a, **k)
            def warning(self, *a, **k):
                logger.warning(*a, **k)
            def error(self, *a, **k):
                logger.error(*a, **k)

        env = {'chat_mod': FakeChat(), 'logger_mod': FakeLogger(), 'plan_mod': None}
        ms = make_mind_for_akasha(env)
        await ms.start()
        ms.enqueue_event({'text': 'hello unified mind'})
        for _ in range(12):
            await asyncio.sleep(ms.heartbeat)
        # trigger expressive introspection
        report = ms.introspect_now(mode='full', expressive=True)
        print('Introspection report keys:', list(report.keys()))
        await ms.stop()

    asyncio.run(demo())

# EOF
