from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Post(models.Model):
    chat = models.CharField(max_length=20, help_text=_("Isi pesan anda"))
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.chat)
