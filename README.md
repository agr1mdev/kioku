# Kioku (記憶)

A spaced repetition learning app with a knowledge graph that tracks concept dependencies.

## Features
- SM-2 algorithm for intelligent review scheduling
- Knowledge graph that propagates risk when a concept is forgotten
- Works as a topic tracker or full flashcard app
- Subjects → Concepts → Flashcards hierarchy

## How it works
Concepts are connected in a dependency graph — if you fail a foundational concept, 
all dependent concepts are flagged as at risk.

In topic tracker mode, SM-2 runs at the concept level.
In flashcard mode, SM-2 runs at the flashcard level and concept health is 
derived from flashcard performance.

## Project Structure
```
kioku/
  ├── core/
  │     ├── models.py   # Subject, Concept, Flashcard classes
  │     ├── sm2.py      # SM2 scheduling algorithm
  │     └── graph.py    # Knowledge graph + risk propagation
  |     |__ db.py       # initalize db & session    
  └── app.py            # Flask app (coming soon)
```

## Roadmap
- [x] SM-2 algorithm
- [x] Knowledge graph with risk propagation
- [x] Data model (Subject, Concept, Flashcard)
- [x] SQLite database for persistence
- [ ] Flask web interface
- [ ] Drag and drop canvas UI
- [ ] ML layer for personalized scheduling
