from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


PROFILE_ROLE_CHOICES = [
    (0, "Student"),
    (1, "Parent"),
    (2, "Teacher"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.IntegerField(choices=PROFILE_ROLE_CHOICES, default=0)
    temp_password = models.CharField(max_length=32)
    phone = models.CharField(max_length=12, default='')

    def __str__(self):
        return f'{self.user.first_name}, {self.user.last_name} Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Messages(models.Model):
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    send_to = models.ForeignKey(User, on_delete=models.SET("Deleted"), related_name="user_to")
    send_from = models.ForeignKey(User, on_delete=models.SET("Deleted"), related_name="user_from")
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.send_from} - {self.send_to} >>> {self.content[0:30]}"
