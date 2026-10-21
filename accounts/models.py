from django.contrib.auth.models import AbstractUser # Django's built-in user (username, password, email, etc.)
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        RUNNER = "runner", "Runner"     # Logs runs and joins challenges
        ORGANIZER = "organizer", "Challenge Organizer"      # Can also create and manage challenges
        ADMIN = "admin", "Admin"        # Can also moderate posts and remove suspicious runs


    # New column added on top of the built-in ones.
    # choices: only the three roles above are allowed (shows as a dropdown in admin).
    # default: new users are Runners unless changed.
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RUNNER)

    def __str__(self):
        # How a user appears as text (admin panel, dropdowns).
        # Without this, it would show "User object (1)".
        return self.username