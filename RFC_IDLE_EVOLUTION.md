# RFC: Built-in Idle Evolution & Self-Learning System

> **Status**: Draft
> **Author**: [Your Name]
> **Date**: 2026-04-29
> **Reference**: [Pask DD-MM-PAS](https://arxiv.org/abs/2604.08000)

---

## Summary

Propose integrating a built-in **Idle Evolution System** into QwenPaw, enabling the AI to automatically learn new skills and report findings when the user is idle. This transforms QwenPaw from a passive assistant into a proactive learning companion.

---

## Motivation

### Current State

QwenPaw is an excellent personal AI assistant with:
- ✅ Multi-channel support (WeChat, DingTalk, QQ, etc.)
- ✅ Extensible Skills system
- ✅ Built-in memory manager (reme_light)
- ✅ Scheduled tasks (cron)

### Problem

**All features are reactive** — the AI only responds when the user initiates. When the user is idle:
- No proactive behavior
- No continuous learning
- No value generation during idle time

### Inspiration

Reference: **[Pask DD-MM-PAS](https://github.com/xzf-thu/Pask)** — "Toward Intent-Aware Proactive Agents with Long-Term Memory"

```
┌─────────────────────────────────────────────────────┐
│  DD-MM-PAS = Demand Detection + Memory + Proactive   │
│                                                     │
│  1. Detection → Detect latent user needs             │
│  2. Memory → Hierarchical memory system              │
│  3. Proactive → Act without explicit requests       │
└─────────────────────────────────────────────────────┘
```

Pask demonstrates that proactive AI requires:
- Real-time intent detection
- Long-term user modeling
- Proactive action capabilities

---

## Proposed Solution

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  Idle Evolution System                               │
│                                                     │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────┐ │
│  │ Idle Monitor│───▶│Demand Detection│───▶│ Evolution│ │
│  └─────────────┘    └──────────────┘    └─────────┘ │
│         │                   │                   │   │
│         ▼                   ▼                   ▼   │
│  ┌─────────────────────────────────────────────────┐ │
│  │              Hierarchical Memory                │ │
│  │  User Profile │ Working Memory │ Long-term     │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Components

#### 1. Idle Monitor Service

```python
# Background service running alongside QwenPaw
# - Monitors user idle time (OS-level)
# - Triggers evolution when idle > threshold (default: 60 min)
# - Respects user's active hours
```

#### 2. Demand Detection

Based on Pask's IntentFlow, detect user needs from:
- Recent conversation history
- Working memory (current session)
- Long-term memory (past interactions)

#### 3. Proactive Learning

When idle is detected:
1. Analyze user's domain and recent activities
2. Search for relevant new skills/tools/papers
3. Evaluate value and feasibility
4. Report findings to user

#### 4. Hierarchical Memory (Enhanced reme_light)

| Layer | Content | Update Frequency |
|-------|---------|------------------|
| User Profile | Background, expertise, preferences | Low |
| Working Memory | Current session state | High |
| Long-term Store | Cross-session knowledge | Medium |

---

## Implementation

### Existing Work

We have implemented a prototype:

**File**: `idle_evolution_service.py`
```python
# Monitors idle time, triggers evolution
# - OS-level idle detection (Windows/macOS/Linux)
# - Configurable threshold (default: 60 min)
# - Daily evolution limit
```

**File**: `skills/autonomous-learner/SKILL.md`
```markdown
# Skill for proactive learning
# - Demand Detection (W/L/D taxonomy)
# - Memory Modeling (Pask's 3-layer)
# - IntentFlow simulation (3 decisions)
```

### Proposed Integration

```json
{
  "idle_evolution": {
    "enabled": true,
    "idle_threshold_minutes": 60,
    "max_evolutions_per_day": 1,
    "active_hours": {
      "start": "08:00",
      "end": "22:00"
    },
    "learning_scope": ["skills", "papers", "tools"],
    "report_channel": "console"
  },
  "memory_manager_backend": "remelight",
  "reme_light_memory_config": {
    "dream_cron": "0 23 * * *",
    "auto_memory_search": true,
    "hierarchical_memory": true
  }
}
```

---

## User Experience

### Before (Current State)

```
User: [uses QwenPaw for tasks]
User: [goes idle for 1 hour]
[No activity - no value generated]

User returns → QwenPaw: "Hi, how can I help?"
```

### After (With Idle Evolution)

```
User: [uses QwenPaw for tasks]
User: [goes idle for 1 hour]

QwenPaw (in background):
  → Detects idle
  → Analyzes user's domain (adaptive optics simulation)
  → Searches for new HCIPy plugins
  → Finds "pyprismatic" (10x faster simulation)
  → Reports finding

User returns → QwenPaw: "Hi! While you were away, I found a faster 
simulation library that might help with your AO work. Want me to set it up?"
```

---

## Benefits

1. **User Productivity** — More value per session
2. **Continuous Improvement** — AI gets smarter over time
3. **Personalization** — Learns user's domain and preferences
4. **Proactive Assistance** — Anticipates needs before explicit requests

---

## Concerns & Mitigations

| Concern | Mitigation |
|---------|------------|
| Privacy | All processing is local, no external calls |
| Resource Usage | Runs only during idle, lightweight |
| Annoying Reports | Respects active hours, configurable frequency |
| False Positives | Daily limits, user can disable |

---

## Adoption Path

### Phase 1: Optional Feature
- Disabled by default
- Users can enable via config or `qwenpaw evolution enable`

### Phase 2: Opt-in Default
- New users get prompted to enable
- Existing users unchanged

### Phase 3: Built-in
- Memory + evolution become core QwenPaw features
- Full integration with Skills Hub

---

## References

- [Pask: DD-MM-PAS Framework](https://arxiv.org/abs/2604.08000)
- [Pask GitHub](https://github.com/xzf-thu/Pask)
- [Our Prototype Implementation](https://github.com/your-repo/copaw-awesome-starter)

---

## Open Questions

1. Should evolution run in background process or as scheduled task?
2. How to handle conflicting learning topics?
3. Should users be able to teach the AI what to learn?
4. Integration with Skills Hub for automatic skill discovery?

---

**We believe this feature would significantly differentiate QwenPaw as a truly proactive personal AI assistant.**
