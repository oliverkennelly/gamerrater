from django.db import models

class GameCategory(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.category.label