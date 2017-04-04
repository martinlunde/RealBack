
from django.db import models, IntegrityError, transaction
from django.utils import timezone
from django.core import validators
from random import choice
from RealBack import settings
from . import logger


class Course(models.Model):
    """ Course model """
    title = models.CharField(max_length=50, validators=[validators.MinLengthValidator(3)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'course_id': self.id,
            'course_title': self.title,
        }


def _generate_pin():
    """ Generate a 6 character pin for attendee login """
    charset = "ABCDEFGHIJKLMNPQRSTUVWXYZ123456789"
    pin = [choice(charset) for i in range(6)]
    pin = ''.join(pin)
    return pin


class Lecture(models.Model):
    """ Lecture model """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, validators=[validators.MinLengthValidator(3)])
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)
    timer_active = models.BooleanField(default=False)
    pin = models.CharField(max_length=6, default=_generate_pin, unique=True)
    paceup = models.IntegerField(default=0)
    pacedown = models.IntegerField(default=0)
    volumeup = models.IntegerField(default=0)
    volumedown = models.IntegerField(default=0)
    attendee_counter = models.IntegerField(default=0)
    lecture_activity = models.IntegerField(default=0)
    volume_reset_timestamp = models.DateTimeField(default=timezone.now)
    pace_reset_timestamp = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=1.0)
    rating_amount = models.IntegerField(default=0)
    rating_active = models.BooleanField(default=False)
    active_topic_index = models.IntegerField(default=0)
    # TODO free old pins that are not used anymore

    def save(self, *args, **kwargs):
        done = False
        while not done:
            try:
                with transaction.atomic():
                    super(Lecture, self).save(*args, **kwargs)
                    done = True
            except IntegrityError as err:
                logger.info("Generated PIN already existed")
                self.pin = _generate_pin()

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'lecture_pin': self.pin,
            'lecture_title': self.title,
            'lecture_start_time': self.start_datetime,
            'lecture_end_time': self.end_datetime,
            'lecture_pace_up': self.paceup,
            'lecture_pace_down': self.pacedown,
            'lecture_volume_up': self.volumeup,
            'lecture_volume_down': self.volumedown,
            'attendee_counter': self.attendee_counter,
            'lecture_activity': self.lecture_activity,
            'pace_reset_timestamp': self.pace_reset_timestamp,
            'volume_reset_timestamp': self.volume_reset_timestamp,
            'rating': self.rating,
            'rating_active': self.rating_active,
            'rating_amount': self.rating_amount,
        }

    def reset_pace(self):
        self.paceup = 0
        self.pacedown = 0
        self.pace_reset_timestamp = timezone.now()
        self.save()

    def reset_volume(self):
        self.volumeup = 0
        self.volumedown = 0
        self.volume_reset_timestamp = timezone.now()
        self.save()


class LectureTopic(models.Model):
    """ Lecture topic model """
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, validators=[validators.MinLengthValidator(3)])
    understanding = models.IntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    def as_dict(self):
        return {
            'topic_id': self.id,
            'topic_title': self.title,
            'topic_understanding': self.understanding,
            'topic_order': self.order,
        }


class Question(models.Model):
    """ Lecture questions model """
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    text = models.CharField(max_length=160)
    votes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            'question_text': self.text,
            'question_votes': self.votes,
            'question_id': self.id,
        }
