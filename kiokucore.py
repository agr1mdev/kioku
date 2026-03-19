from datetime import date, timedelta

#Concept card
class ConceptCard:
    def __init__(self,name):
        self.name = name
        self.repetitions = 0
        self.ease_factor = 2.5
        self.interval = 0
        self.next_review = None

    def __str__(self):
        return f"{self.name} | Interval: {self.interval}d | EF:{self.ease_factor} | Next: {self.next_review}"
        
# implementation of the sm2 algorithm
class SM2:
    def review(self,card,score):
        
        if score>=3:

            if card.repetitions == 0:
                card.interval = 1
            elif card.repetitions == 1:
                card.interval = 6
            else:
                card.interval = round(card.interval * card.ease_factor)


            card.repetitions += 1

        else:
            card.repetitions = 0
            card.interval = 1

        card.ease_factor += (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
        card.ease_factor = round(card.ease_factor, 2)   
        
        # enforce minimum
        if card.ease_factor < 1.3:
            card.ease_factor = 1.3
        card.ease_factor = round(card.ease_factor, 2)
        # Step 5 - set next review date
        card.next_review = date.today() + timedelta(days=card.interval)

        return card
    


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