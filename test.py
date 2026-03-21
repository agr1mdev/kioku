from core.models import Subject, Concept, Flashcard
from core.sm2 import SM2
from core.graph import get_at_risk, get_concept_health

s = Subject("Machine Learning")
print(s)


c1 = Concept("Calculus", subject_id=1)
c2 = Concept("Cost Function", subject_id=1)
c3 = Concept("Gradient Descent", subject_id=1)
print(c1)
print(c2)
print(c3)

f = Flashcard("What is gradient descent?", "An optimization algorithm", concept_id=3)
print(f)

sm2 = SM2()
f = sm2.review(f, 5)
print(f)

graph = {
    "Calculus": [],
    "Cost Function": ["Calculus"],
    "Gradient Descent": ["Calculus", "Cost Function"],
    "Linear Regression": ["Gradient Descent"]
}

at_risk = get_at_risk(graph, "Cost Function")
print("At risk:", at_risk)