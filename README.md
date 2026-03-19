# Kioku (記憶)

A spaced repetition learning app with a knowledge graph that tracks concept dependencies.

## Features
- SM-2 algorithm for intelligent review scheduling
- Knowledge graph that propagates risk when a concept is forgotten
- Built with Python

## How it works
Each concept is tracked individually using the SM-2 algorithm. Concepts are connected in a dependency graph — if you fail a foundational concept, all dependent concepts are flagged as at risk.

## Roadmap
- [ ] SQLite database for persistence
- [ ] Flask web interface
- [ ] ML layer for personalized scheduling