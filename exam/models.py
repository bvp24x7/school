from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):

    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    standard        = models.CharField(max_length=50)
    email           = models.EmailField(max_length=254, null=True)
    enrollment      = models.CharField(max_length=15, unique=True)
    date_created    = models.DateTimeField( auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

class Quiz(models.Model):

    
    name            = models.CharField(max_length=250)
    standard        = models.CharField(max_length=50)
    subject         = models.CharField(max_length=150)
    marks           = models.IntegerField(default=0)
    time            = models.TimeField( auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Question(models.Model):

    # number          = models.IntegerField(default=1, unique=True)
    content         = models.CharField(max_length=350)
    quiz            = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Options(models.Model):

    # number          = models.IntegerField(default=1, unique=True)
    content         = models.CharField(max_length=250, null=True)
    correct         = models.BooleanField(default=False)
    explanation     = models.CharField(max_length=250)
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        order_with_respect_to = 'question'

class QuizRecords(models.Model):
    student         = models.ForeignKey(Student, on_delete=models.CASCADE)
    completed       = models.BooleanField(default=False)
    quiz            = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    marks           = models.IntegerField(default=0) 
    start_time      = models.DateTimeField(auto_add_now=True)
    # end_time        = models.DateTimeField(null=True) 

    def __str__(self):
        return self.student.enrollment

    


class Question_Records(models.Model):

    quiz_record     = models.ForeignKey(QuizRecords, on_delete=models.CASCADE)
    question        = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    answer          = models.CharField(max_length=250, null=True)
    answered        = models.BooleanField(default=False)
    correct         = models.BooleanField(default=False)
    def __str__(self):
        return self.quiz_record.student.id

    

