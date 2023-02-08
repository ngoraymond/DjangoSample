from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

default_img = './quizsite/static/quizsite/sample_quiz.png'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    # points earned by user, done by taking quizzes

    played = models.ManyToManyField('Quiz', related_name='played')
    favorited = models.ManyToManyField('Quiz', related_name='favorited')
    liked = models.ManyToManyField('Quiz', related_name='liked')
    disliked = models.ManyToManyField('Quiz', related_name='disliked')


class Quiz(models.Model):
    name = models.CharField(max_length=100) 
    description = models.CharField(max_length=1000) 
    image = models.FileField(upload_to='quiz_images', default=default_img)
    content_type = models.CharField(blank=True, max_length=255, default='image/png')
    publish_date = models.DateTimeField(default=now)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, related_name='created')

    is_assessment = models.BooleanField(default=True) #false = buzzfeed style, true = assessment style

'''
Buzzfeed style questions where each answer corresponds to a certain personality result
'''


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_number = models.IntegerField(default=0)
    prompt = models.CharField(max_length=500, default=None)
    image = models.FileField(upload_to='quiz_images', default=None)
    content_type = models.CharField(blank=True, max_length=255) #Question image content type

    weight = models.IntegerField(default=1)


class Choice(models.Model):
    choice = models.CharField(max_length=200) # text label of the choice
    choice_number = models.IntegerField(default=0) # choice index (begins with 1)
    result = models.CharField(max_length=200, blank=True) # For Buzzfeed style, this is the result
    is_correct = models.BooleanField(default=False) # For Assessment style, true if correct

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    answerers = models.IntegerField(default=0) # number of people who gave this answer
