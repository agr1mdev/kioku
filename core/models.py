class Subject:
    def __init__(self,name):
        self.id = None
        self.name = name
    
    def __str__(self):
        return f"{self.name} | Id: {self.id}"
    
class Concept:
    def __init__(self, name, subject_id):
        self.id = None
        self.name = name
        self.subject_id = subject_id
        self.repetitions = 0
        self.ease_factor = 2.5
        self.interval = 0
        self.next_review = None


    def __str__(self):
        return f"{self.name} | Id: {self.id} | Subject_Id: {self.subject_id} | Repetitions : {self.repetitions} | Ease factor : {self.ease_factor}| Interval: {self.interval}| next review : {self.next_review}"
    
class Flashcard:
    
    def __init__(self,front,back,concept_id):
        self.id = None
        self.front = front
        self.back = back
        self.concept_id = concept_id
        self.repetitions = 0
        self.ease_factor = 2.5
        self.interval = 0
        self.next_review = None

    def __str__(self):
        return f"Id: {self.id} | Front: {self.front} | Back : {self.back} | Concept_id : {self.concept_id} | Repetitions : {self.repetitions} | Ease factor : {self.ease_factor}| Interval: {self.interval}| next review : {self.next_review} "
    




        