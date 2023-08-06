from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Topic
from .form import TopicFrom


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
    template = loader.get_template('topic.html')
    entries = topic.entry_set.order_by('-added_date')
    context = {
        'topic': topic,
        'entries': entries
    }
    return HttpResponse(template.render(context, request))


def new_topic(request):
    template = loader.get_template('new_topic.html')

    if request.method != 'POST':
        form = TopicFrom()
    else:
        form = TopicFrom(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('topics')

    context = {'form': form}
    return HttpResponse(template.render(context, request))
