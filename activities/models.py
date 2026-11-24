from django.conf import settings
from django.db import models


class Run(models.Model):
    # Who ran it. If the user deletes their account, their runs go too (CASCADE).
    # related_name='runs' lets us write user.runs.all()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='runs')
    title = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # in miles, e.g. 3.10
    # Time it took, the same three boxes the form uses
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)
    seconds = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']  # newest runs first

    def __str__(self):
        return f'{self.user.username} - {self.distance} mi on {self.date}'
