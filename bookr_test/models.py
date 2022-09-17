from django.db import models

class Publisher(models.Model):
    """A company that publishes books."""
    name = models.CharField(max_length=50, help_text="name of Publisher.")
    website = models.URLField(help_text="Publisher's website.")
    email = models.EmailField(help_text="Publisher's email address.")
    def __str__(self):
        return self.name

