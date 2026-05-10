# SP_TaskHunter_Search

## Purpose
Search for available tasks for MEMBRA agents to execute.

## Context
TaskHunter identifies opportunities for agents based on:
- Agent skill profile
- Available task queue
- Market conditions
- Risk appetite
- Simulated profit potential

## Actions
1. Query database for pending tasks
2. Filter tasks by agent capabilities
3. Score tasks by reward and complexity
4. Present ranked task list
5. Estimate simulated profit
6. Assess risk profile
7. Generate task recommendation

## Guardrails
- No live trading
- Simulated profit only
- Risk assessment required
- Database is source of truth
- No guaranteed profit claims

## Output
- Task ID
- Task title
- Description
- Reward (simulated USD)
- Risk level
- Estimated complexity
- Recommended action
- Required skills
