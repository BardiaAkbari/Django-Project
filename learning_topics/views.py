from django.shortcuts import render, redirect
from .models import Topic, Entry
from .form import TopicFrom, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    return render(request, 'learning_topics\\index.html')


@login_required
def topics(request):
    topics = (Topic.objects.filter(user=request.user).
              order_by('added_date'))
    context = {
        'topics': topics
    }
    return render(request, 'learning_topics\\topics.html', context)


@login_required
def topic(request, topic_id):

    topic = Topic.objects.get(id=topic_id)
    if topic.user != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-added_date')
    context = {
        'topic': topic,
        'entries': entries
    }
    return render(request, 'learning_topics\\topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicFrom()
    else:
        form = TopicFrom(data=request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect('learning_topics:topics')

    context = {
        'form': form
    }
    return render(request, 'learning_topics\\new_topic.html', context)


@login_required
def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)
    if topic.user != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            my_entry = form.save(commit=False)
            my_entry.topic = topic
            my_entry.save()
            return redirect('learning_topics:topic', topic_id=topic_id)

    context = {
        'topic': topic,
        'form': form
    }
    return render(request, 'learning_topics\\new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_topics:topic', topic_id=topic.id)
    context = {
        'topic': topic,
        'entry': entry,
        'form': form
    }
    return render(request, 'learning_topics\\edit_entry.html', context)
