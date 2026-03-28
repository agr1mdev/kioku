from flask import Flask, render_template, request, redirect
from core.db import Session, init_db
from core.models import Subject, Concept, Flashcard, Dependency
from core.graph import get_at_risk, get_concept_health
from core.sm2 import SM2
from datetime import date
from flask import jsonify
import json



app = Flask(__name__)
init_db()


@app.route("/")
def home():
    session = Session()
    subjects = session.query(Subject).all()
    due_count = session.query(Flashcard).filter(Flashcard.next_review <= date.today()).count()
    return render_template("index.html", subjects=subjects, due_count=due_count)

@app.route("/add-subject",methods = ["POST"])
def add_subject():
    name = request.form["name"]
    session = Session() 
    subject = Subject(name = name)
    session.add(subject)
    session.commit()
    return redirect("/")

@app.route("/subject/<int:subject_id>", methods=["GET"])
def subject(subject_id):
    session = Session()
    subject = session.query(Subject).filter_by(id=subject_id).first()
    concepts = session.query(Concept).filter_by(subject_id=subject_id).all()
    concept_ids = [c.id for c in concepts]
    dependencies = session.query(Dependency).filter(
        Dependency.source_id.in_(concept_ids)
    ).all()
    return render_template("subject.html", subject=subject, concepts=concepts, dependencies=dependencies)

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

@app.route("/review/answer", methods=["POST"])
def answer():
    card_id = request.form["card_id"]
    score = request.form["score"]
    session = Session()
    flashcard = session.query(Flashcard).filter_by(id=card_id).first()
    sm2 = SM2()
    sm2.review(flashcard, int(score))

    concept = session.query(Concept).filter_by(id=flashcard.concept_id).first()
    all_concepts = session.query(Concept).filter_by(subject_id=concept.subject_id).all()

    if int(score) < 3:
        graph = {}
        for c in all_concepts:
            deps = session.query(Dependency).filter_by(target_id=c.id).all()
            graph[c.name] = [session.query(Concept).filter_by(id=d.source_id).first().name for d in deps]
        at_risk = get_at_risk(graph, concept.name)
        at_risk.append(concept.name)
        for c in all_concepts:
            c.at_risk = True if c.name in at_risk else False
    else:
        concept.at_risk = False
        for c in all_concepts:
            if c.at_risk and c.id != concept.id:
                deps = session.query(Dependency).filter_by(target_id=c.id).all()
                still_at_risk = any(
                    session.query(Concept).filter_by(id=d.source_id).first().at_risk
                    for d in deps
                )
                if not still_at_risk:
                    c.at_risk = False

    session.commit()
    return redirect("/review")

@app.route("/debug")
def debug():
    session = Session()
    flashcards = session.query(Flashcard).all()
    result = ""
    for f in flashcards:
        result += f"{f.id} | {f.front} | EF: {f.ease_factor} | Interval: {f.interval} | Next: {f.next_review}<br>"
    return result

@app.route("/add-dependency", methods=["POST"])
def add_dependency():
    data = request.get_json()
    source_id = data["source"]
    target_id = data["target"]
    session = Session()
    
    # check if dependency already exists
    existing = session.query(Dependency).filter_by(
        source_id=source_id, 
        target_id=target_id
    ).first()
    
    if not existing:
        dep = Dependency(source_id=source_id, target_id=target_id)
        session.add(dep)
        session.commit()
    
    return jsonify({"status": "ok"})

@app.route("/save-position", methods=["POST"])
def save_position():
    data = request.get_json()
    session = Session()
    concept = session.query(Concept).filter_by(id=data["id"]).first()
    concept.x = data["x"]
    concept.y = data["y"]
    session.commit()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)