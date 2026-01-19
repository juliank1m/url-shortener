from django.db import models
from .utils import generate_code

# Create your models here.

class Link(models.Model):
    code = models.CharField(max_length=16, unique=True, db_index=True, blank=True)
    target_url = models.URLField(max_length=2048)

    created_at = models.DateField(auto_now_add=True)

    clicks = models.PositiveIntegerField(default=0)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.code:
            # collision-safe generation
            for _ in range(5):
                self.code = generate_code()
                try:
                    return super().save(*args, **kwargs)
                except IntegrityError:
                    self.code = ""
            raise IntegrityError("Could not generate unique code")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} -> {self.target_url}"


    