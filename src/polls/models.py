from django.db import models
from django.utils.timezone import datetime


class Poll(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=1024)


class Question(models.Model):
    class Type:
        """
        Описывает типы вопроса
        """
        TEXT = 1
        CHOICE = 2
        MULTICHOICE = 3

        choices = (
            (TEXT, 'Текст'),
            (CHOICE, 'Выбор'),
            (MULTICHOICE, 'Множественный выбор'),
        )

    poll = models.ForeignKey(
        Poll, related_name='questions', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=256)
    type = models.SmallIntegerField(choices=Type.choices, default=Type.TEXT)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=128, default='Enter value')


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.IntegerField()
    date = models.DateField(default=datetime.today, editable=False)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.CharField(max_length=128, blank=True, null=True)
