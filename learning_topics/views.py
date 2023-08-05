from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Topic


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def topics(request):
    topics = Topic.objects.order_by('added_date')
    template = loader.get_template('topics.html')
    context = {
        'topics': topics
    }
    return HttpResponse(template.render(context, request))


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    template =loader.get_template('topic.html')
    entries = topic.entry_set.order_by('-added_date')
    context = {
        'topic': topic,
        'entries': entries
    }
    return HttpResponse(template.render(context, request))

def new_topic(request):

    print("kon")