from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question,Choice,userdetails

# Create your views here.

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"
    
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model=Question
    template_name="polls/detail.html"
    
class ResultsView(generic.DetailView):
    model =Question
    template_name="polls/results.html"

def index(request):
    return HttpResponse("hello, World.You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s."%question_id)

def results(request, question_id):
    response="You're looking at the results of question %s."
    return HttpResponse(response%question_id)

def vote(request, question_id):
    return HttpResponse("You'revoting on question %s."%question_id)
user=""
def index(request):
    global user
    latest_question_list=Question.objects.order_by("-pub_date")[:5]
    template=loader.get_template("polls/index.html")
    context={
        "latest_question_list": latest_question_list,
        "user":user,
    }
    return HttpResponse(template.render(context,request))

def detail(request,question_id):
    try:
        question= Question.objects.get(pk=question_id)
    except:
        raise Http404("Question does not exist")
    return render(request,"polls/details.html",{"question":question,
                                                "number":question_id})

def vote(request, question_id):
    question= get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,"polls/details.html",
            {
                "question":question,
                "error_message":"You didn't select a choice",
            },
        )
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def addPoll(request):
    return render(request,"polls/newpoll.html")

def add(request):
    
    print("processing started")
    ques=request.POST["ques"]
    print(ques)
    q=Question(question_text=ques,pub_date=timezone.now())
    q.save()
    choices=int(request.POST["total_num"])
    for i in range(1,choices+1):
        temp="choice"+str(i)
        choice=request.POST[temp]
        choice=choice.strip()
        print(choice)
        q.choice_set.create(choice_text=choice,votes=0)
        q.save()
    return HttpResponseRedirect(reverse("polls:index"))
    
    choices=request.POST["choice"]
    choices=choices.split("_")
    for ch in choices:
        q.choice_set.create(choice_text=ch,votes=0)
    q.save()
    return HttpResponseRedirect(reverse("polls:index"))

errormsg=""
def LoginPage(request):
    global errormsg
    return render(request,"mysite/login.html",context={
        "error_msg":errormsg,
    })

def Checkuser(request):
    global errormsg,user
    print("User validation start")
    username=request.POST["username"]
    password=request.POST["pwd"]
    user=authenticate(request,username=username, password=password)
    if user is not None:
        errormsg=""
        login(request,user)
        return HttpResponseRedirect(reverse("polls:index"))
    else:
        errormsg="Invalid Credentials"
        return HttpResponseRedirect(reverse("polls:Login"))
    
def newuser(request):
    print("User creation start")
    uname=request.POST["username"]
    pwd=request.POST["pwd"]
    fname=request.POST["fname"]
    lname=request.POST["lname"]
    mail=request.POST["mail"]
    user=User.objects.create_user(uname,mail,pwd)
    user.first_name=fname
    user.last_name=lname
    user.save()
    login(request,user)
    return HttpResponseRedirect(reverse("polls:index"))

def logoutfunc(request):
    logout(request)
    return HttpResponseRedirect(reverse("polls:Login"))
    