from django.db import models

class CodeSnippet(models.Model):
    code = models.TextField()
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)