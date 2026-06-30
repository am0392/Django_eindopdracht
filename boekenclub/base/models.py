from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Profile(models.Model):
    favorite_genre = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    publication_year = models.IntegerField(blank=False)
    genre = models.CharField(max_length=30, blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='approved_by', null=True, blank=True)
    def __str__(self):
        return self.name


class ReadingSession(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False)
    date = models.DateField(blank=False,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False)
    
    class Meta:
        unique_together = ('book', 'user', 'date')
        
    def __str__(self):
        return f"Book: {self.book.name}, Score: {self.score}, Read by: {self.user.get_username()}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)