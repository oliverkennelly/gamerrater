from django.db import models
import statistics

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    designer = models.CharField(max_length=255)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time = models.IntegerField()
    age_rec = models.IntegerField()

    @property
    def average_score(self):
        """Average score calculated attribute for each game"""
        scores = [review.score for review in self.scores.all()]

        # Calculate the averge and return it.
        if scores == []:
            return "No ratings"
        else:
            return statistics.mean(scores)

        #return the result