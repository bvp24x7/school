from django.shortcuts import render, redirect

from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
# import datetime
# from datetime import timezone
from .models import *
from .forms import *

# Create your views here.


def home(request):
    return render(request, 'exam/home.html')

def register(request):

    form1 = CreateUserForm()
    form2 = StudentForm()
    if request.method == 'POST':
        form1 = CreateUserForm(request.POST)
        form2 = StudentForm(request.POST)
        print(request.POST)
        print('form1', form1.is_valid())
        print('form2', form2.is_valid())

        if form1.is_valid() and form2.is_valid():
            
            user=form1.save()
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()
            
            return redirect('login')

    context = {'form1': form1, 'form2':form2}

    return render(request, 'exam/register.html', context)


def logIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')


        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'exam/login.html')

    context = {}
   
    return render(request, 'exam/login.html',context)

def logOut(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')  
def createQuiz(request):
    form = QuizForm(request.POST)
    if request.method == 'POST':
        form.save()
    context = {'form' : form }

    return render(request, 'exam/createe.html' , context)
@login_required(login_url='login')
def createQuestion(request):
    form = QuestionForm(request.POST)
    
    if request.method == 'POST':
        if form.is_valid():
            
            form.save()
    

    context = {'form' : form }
    return render(request, 'exam/createe.html', context )
@login_required(login_url='login')
def createOptions(request):
    form = OptionsForm(request.POST)
    if request.method == 'POST':
        form.save()
    context = {'form' : form }

    return render(request, 'exam/createe.html' , context)
@login_required(login_url='login')
def dashboard(request):
    
    uuu= Student.objects.filter(user_id=request.user.id).values() 
    std = uuu.values('standard')[0]['standard']   
    quizs = Quiz.objects.filter(standard=std)
    # QuizRecords.objects.filter(student = )
    
    context={'quizs':quizs}
    return render(request,'exam/loggedin.html',context)


@login_required(login_url='login')
def questionView(request,pk):
    
    quiz = Quiz.objects.get(id=pk)
    uid = request.user.id
    stud = Student.objects.get(user_id=uid)

    qzr = QuizRecords()
    qzr.student = stud
    qzr.quiz = quiz
    qzr.start_time = timezone.now()
    qzr.save()
    all_questions = Question.objects.filter(quiz_id=quiz.id)

    for each_questions in all_questions:
        qurc = Question_Records()
        qurc.quiz_record = qzr
        qurc.question = each_questions
        qurc.save()

    context={'quiz':quiz,'stud':stud}
    return render(request, 'exam/startquiz.html',context)


@login_required(login_url='login')
def nextquestion(request,stud,quiz):



    if request.method=='POST':
        print('hellllllllllllllllllo',request.POST)
        question_id  = int(request.POST['question_id'])        
        quizrec = int(request.POST['quzrec'])
        opted = Options.objects.get(id=request.POST['ansed'])
        exp = opted.explanation
        question = Question.objects.get(id=question_id)
        option = Options.objects.filter(question_id=question.id)
        dso = opted.correct
        Question_Records.objects.filter(quiz_record_id=quizrec,question_id=question_id).update(answer=opted.content,answered=True,correct=dso)
        context = {'dso': dso, 'exp':exp,'submitted':True,'quiz':quiz,'stud':stud, 'question' : question,'option' : option,'finished':False}
    else:
        quzrec = QuizRecords.objects.get(student=stud,quiz=quiz)
        qstrec = Question_Records.objects.filter(quiz_record=quzrec,answered=False)
        if qstrec:
            question = Question.objects.get(id=qstrec[0].question.id)
            option = Options.objects.filter(question_id=question.id)
            context={'question' : question, 'option' : option,'quiz':quiz,'stud':stud,'quzrec':quzrec.id,'finished':False}
        else:
            quzrec.completed = True
            total_questions = Question_Records.objects.filter(quiz_record=quzrec).count()
            correct_answer = Question_Records.objects.filter(quiz_record=quzrec,correct=True).count()
            quzrec.marks = correct_answer 
            stime = quzrec.start_time

            time_taken = timezone.now() - stime
            # print((time_taken,2))
            # print(time_taken[0:4])
            

            if total_questions/2 <=correct_answer:
                result = "pass"
            else:
                result = "fail"
            context={'finished':True,"total_question":total_questions,"correct_answered":correct_answer,"result":result,'time_taken':time_taken}    
            print(context)            
    return render(request, 'exam/questioned.html', context)

