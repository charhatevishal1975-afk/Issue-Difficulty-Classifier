from django.db import models

class Issue(models.Model):
    issue_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    labels = models.CharField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField()
    comment_count = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return f"[{self.difficulty}] {self.title}"