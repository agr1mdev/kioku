from flask import Flask, render_template, request, redirect
from core.db import Session, init_db
from core.models import Subject, Concept, Flashcard
from core.sm2 import SM2
from datetime import date



app = Flask(__name__)
init_db()


@app.route("/")
def home():
    session = Session()
    subjects = session.query(Subject).all()
    print("Subjects found:", subjects)  # add this
    for s in subjects:
        print(s.id, s.name)            # add this
    return render_template("index.html", subjects=subjects)

@app.route("/add-subject",methods = ["POST"])
def add_subject():
    name = request.form["name"]
    session = Session()
    subject = Subject(name = name)
    session.add(subject)
    session.commit()
    return redirect("/")

@app.route("/subject/<int:subject_id>",methods= ["GET"])
def subject(subject_id):
    session = Session()
    subject = session.query(Subject).filter_by(id=subject_id).first()
    concepts = session.query(Concept).filter_by(subject_id = subject_id).all()
    return render_template("subject.html",subject=subject,concepts = concepts)

@app.route("/subject/<int:subject_id>/add-concept", methods = ["POST"])
def add_concept(subject_id):
    name = request.form["name"]
    session = Session()
    concept = Concept(name= name,subject_id = subject_id)
    session.add(concept)
    session.commit()
    return redirect(f"/subject/{subject_id}")

@app.route("/concept/<int:concept_id>", methods = ["GET"])
def show_flashcard(concept_id):
    session = Session()
    concept = session.query(Concept).filter_by(id = concept_id).first()
    flashcards = session.query(Flashcard).filter_by(concept_id = concept_id).all()
    return render_template("concept.html",concept = concept, flashcards = flashcards)

@app.route("/concept/<int:concept_id>/add-flashcard",methods = ["POST"])
def add_flashcard(concept_id):
    front = request.form["front"]
    back = request.form["back"]
    session = Session()
    flashcard = Flashcard(front = front, back = back, concept_id = concept_id)
    session.add(flashcard)
    session.commit()
    return redirect(f"/concept/{concept_id}")

@app.route("/review",methods = ["GET"])
def review_page():
    session = Session()
    due_cards = session.query(Flashcard).filter(Flashcard.next_review <= date.today()).all()
    card = due_cards[0] if due_cards else None
    return render_template("review.html",card= card, show_answer = False)


@app.route("/review/show-answer", methods = ["POST"])
def show_answer():
    card_id = request.form["card_id"]
    session = Session()
    flashcard = session.query(Flashcard).filter_by(id=card_id).first()
    return render_template("review.html",card = flashcard,show_answer=True)

@app.route("/review/answer",methods = ["POST"])
def answer():
    card_id = request.form["card_id"]
    score = request.form["score"] 
    session = Session()
    flashcard = session.query(Flashcard).filter_by(id=card_id).first()
    sm2 = SM2()
    sm2.review(flashcard, int(score))
    session.commit()
    return redirect(f"/review")

@app.route("/debug")
def debug():
    session = Session()
    flashcards = session.query(Flashcard).all()
    result = ""
    for f in flashcards:
        result += f"{f.id} | {f.front} | EF: {f.ease_factor} | Interval: {f.interval} | Next: {f.next_review}<br>"
    return result

if __name__ == "__main__":
    app.run(debug=True)