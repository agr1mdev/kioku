from datetime import date, timedelta

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