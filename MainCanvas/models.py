from django.db import models

# Create your models here.

class Drawing(models.Model):
    drawingJSONText = models.TextField(null = True)
    image = models.ImageField(upload_to='drawing')