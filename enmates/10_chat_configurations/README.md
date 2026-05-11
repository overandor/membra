# Chat Configurations

This directory contains ChatConfig files for different agent roles.

## Purpose

ChatConfig declares which SI + IP components compose each agent. It defines audience, mode, project, purpose, versions, and loading order.

## Agent Roles

- **EnMaTeSArchitect**: Design package architecture, folder tree, graph schema, ChatConfig
- **AgentDeveloper**: Build app.py, exporters, tests, repo ingestion, UI
- **DomainExpert**: Answer from SG + SDA; navigate the knowledge base
- **TesterAI**: Generate tests, RAG checks, ambiguity checks, hallucination checks
- **VerificationFirewall**: Validate README/product claims against code evidence
- **ReleaseManager**: Control deployment, changelog, ZIP export, release gates

## Configuration Format

Each role has a configuration file that specifies:
- System Instruction components to load
- Initiation Package components to load
- Agent role and specialization
- Operating mode
- Profit layer settings

## Status

Configuration files pending implementation.
