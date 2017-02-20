from django.db import models, IntegrityError, transaction
from random import choice


class Course(models.Model):
    """ Course model """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


def _generate_pin():
    """ Generate a 6 character pin for attendee login """
    charset = "ABCDEFGHIJKLMNPQRSTUVWXYZ123456789"
    pin = [choice(charset) for i in range(6)]
    pin = ''.join(pin)
    # TODO check if exists in db after generating (or maybe not. exception is handled)
    return pin


class Lecture(models.Model):
    """ Lecture model """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    pin = models.CharField(max_length=6, default=_generate_pin, unique=True)
    # TODO free old pins that are not used anymore

    def save(self, *args, **kwargs):
        done = False
        while not done:
            try:
                with transaction.atomic():
                    super(Lecture, self).save(*args, **kwargs)
                done = True
            except IntegrityError as err:
                # TODO maybe log?
                self.pin = _generate_pin()
