from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # ✅ ADICIONE ISTO
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
