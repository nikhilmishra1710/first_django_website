from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

def gotopolls(request):
    return HttpResponseRedirect("mysite:polls")