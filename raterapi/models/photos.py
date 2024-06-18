from django.db import models

class Photo(models.Model):
    upload = models.ImageField(upload_to ='uploads/')