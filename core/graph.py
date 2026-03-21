graph = {
    "Calculus":          [],
    "Linear Algebra":    [],
    "Cost Function":     ["Calculus"],
    "Feature Scaling":   ["Linear Algebra"],
    "Gradient Descent":  ["Calculus", "Cost Function"],
    "Linear Regression": ["Gradient Descent", "Feature Scaling"]
}

#Topics at risk
def get_at_risk(graph, failed_concept):
    queue = [failed_concept]
    at_risk = []

    while len(queue) > 0:
        current = queue.pop(0)
        
        for i in graph:
             for j in graph[i]:
                if j == current:
                    at_risk.append(i)
                    queue.append(i)
        
    return at_risk

def get_concept_health(concept, flashcards):
    if len(flashcards) == 0:
        # topic tracker mode - use concept's own SM2 fields
        return concept.ease_factor
    else:
        # flashcard mode - derive from flashcards
        avg_ef = sum(f.ease_factor for f in flashcards) / len(flashcards)
        return avg_ef