from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

CHOICES = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin'),
)


class Review(models.Model):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=CHOICES, default='u')
    bio = models.TextField(max_length=500, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Comments(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='Comments')
    text = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Comments')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)

