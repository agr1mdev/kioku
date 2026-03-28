# from core.models import Subject, Concept, Flashcard
# from core.sm2 import SM2
# from core.graph import get_at_risk, get_concept_health

# s = Subject("Machine Learning")
# print(s)


# c1 = Concept("Calculus", subject_id=1)
# c2 = Concept("Cost Function", subject_id=1)
# c3 = Concept("Gradient Descent", subject_id=1)
# print(c1)
# print(c2)
# print(c3)

# f = Flashcard("What is gradient descent?", "An optimization algorithm", concept_id=3)
# print(f)

# sm2 = SM2()
# f = sm2.review(f, 5)
# print(f)

# graph = {
#     "Calculus": [],
#     "Cost Function": ["Calculus"],
#     "Gradient Descent": ["Calculus", "Cost Function"],
#     "Linear Regression": ["Gradient Descent"]
# }

# at_risk = get_at_risk(graph, "Cost Function")
# print("At risk:", at_risk)

# from core.models import Subject, Concept, Flashcard
# from core.db import Session, init_db
# from core.sm2 import SM2
# from core.graph import get_at_risk, get_concept_health



# # create tables
# init_db()

# # open a session
# session = Session()

# create a subject and save it

# clear tables before testing
# session.query(Flashcard).delete()
# session.query(Concept).delete()
# session.query(Subject).delete()
# session.commit()

# now add fresh data
# con1 = Concept(name="Calculus", subject_id=1)
# fc1 = Flashcard(front="What is gradient descent?", back="An optimization algorithm", concept_id=3)
# session.add(con1)
# session.add(fc1)
# session.commit()

# # read it back
# result = session.query(Concept).all()
# for r in result:
#     print(r.id, r.name,r.subject_id)

# result = session.query(Flashcard).all()
# for r in result:
#     print(r.id, r.front, r.back, r.concept_id)

# # test SM2 + database persistence
# fc = session.query(Flashcard).first()
# print("Before:", fc.id, fc.ease_factor, fc.interval, fc.next_review)

# sm2 = SM2()
# fc = sm2.review(fc, 5)
# session.commit()

# fc2 = session.query(Flashcard).first()
# print("After:", fc2.id, fc2.ease_factor, fc2.interval, fc2.next_review)

# from datetime import date

# session = Session()
# flashcard = session.query(Flashcard).first()
# # flashcard.next_review = date.today()
# # session.commit()
# print(flashcard.front, flashcard.next_review)

from core.models import Flashcard
from core.db import Session
from datetime import date

session = Session()
flashcard = session.query(Flashcard).all()
for f in flashcard:
    f.next_review = date.today()
session.commit()
print("done")