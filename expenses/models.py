from django.db import models
from authenticate.models import NewUser
from django.utils import timezone

# Create your models here.
class Expenses(models.Model):

    CATEGORY_OPTIONS = [
        ("ONLINE_SERVICE", "ONLINE_SERVICE"),
        ("TRAVEL", "TRAVEL"),
        ("FOOD", "FOOD"),
        ("RENT", "RENT"),
        ("OTHERS", "OTHERS"),
    ]

    category    = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner       = models.ForeignKey(to=NewUser, on_delete=models.CASCADE)
    date        = models.DateField(null=False, blank=False)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at",]

    def __str__(self):
        return "%s's expenses" % (self.owner)
