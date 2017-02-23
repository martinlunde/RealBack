
from django.db import models, IntegrityError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from random import choice
from RealBack import settings


class Course(models.Model):
    """ Course model """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def _generate_pin():
    """ Generate a 6 character pin for attendee login """
    charset = "ABCDEFGHIJKLMNPQRSTUVWXYZ123456789"
    pin = [choice(charset) for i in range(6)]
    pin = ''.join(pin)
    return pin


class Lecture(models.Model):
    """ Lecture model """
    # class Meta:
    #     permissions = (
    #         ('can_lecture', 'Can access and create lectures'),
    #         ('can_attend', 'Can attend lectures'),
    #     )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    pin = models.CharField(max_length=6, default=_generate_pin, unique=True)
    # pin_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO delete the related user with delete() override or post_delete signal
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

    def __str__(self):
        return self.title


# @receiver(post_save, sender=Lecture)
# def create_pin_user(sender, instance, created, **kwargs):
#     if created:
#         user = get_user_model().objects.create_user(instance.pin, instance.pin + '@realback.com', instance.pin)
#         instance.pin_user = user
#         instance.save()
