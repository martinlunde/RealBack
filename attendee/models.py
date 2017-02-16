
from django.db import models
from random import choice


class Course(models.Model):
    """ Course model """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


def generate_pin():
    charset = "ABCDEFGHIJKLMNPQRST123456789"
    pin = [choice(charset) for i in range(6)]
    pin = ''.join(pin)
    # TODO check if exists in db after generating
    return pin


class Lecture(models.Model):
    """ Lecture model """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    pin = models.CharField(max_length=6, default=generate_pin)
    # TODO pin must be unique in db
