from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, datetime, MINYEAR


# Create your models here.


# Tag model
# Create a model for tag, which will store the tag name and several tag can be applied to a single quote.
class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


# Author model
class Author(models.Model):
    full_name = models.CharField(max_length=255)
    born_date = models.DateField()
    born_location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.full_name}"


# Quote model
class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # there are several tag stored on the list
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"


# User model
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
