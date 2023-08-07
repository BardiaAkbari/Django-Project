from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Topic, Entry
from .form import TopicFrom, EntryForm


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

    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))


def new_entry(request, topic_id):
    template = loader.get_template('new_entry.html')

    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            my_entry = form.save(commit=False)
            my_entry.topic = topic
            my_entry.save()
            return redirect('topic', topic_id=topic_id)

    context = {
        'topic': topic,
        'form': form
    }
    return HttpResponse(template.render(context, request))


def edit_entry(request, entry_id):

    template = loader.get_template('edit_entry.html')
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('topic', topic_id=topic.id)
    context = {
        'topic': topic,
        'entry': entry,
        'form': form
    }
    return HttpResponse(template.render(context, request))
