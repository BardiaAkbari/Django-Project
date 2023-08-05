from django.db import models


class Topic(models.Model):
    text = models.CharField(max_length=50)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text


class Entry(models.Model):
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    added_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."
