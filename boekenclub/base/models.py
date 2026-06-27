from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Profile(models.Model):
    FavoriteGenre = models.CharField(max_length=100)
    DateOfBirth = models.DateField(null=True, blank=True)
    City = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    Name = models.CharField(max_length=30, blank=False, unique=True)
    PublicationYear = models.IntegerField(blank=False)
    Genre = models.CharField(max_length=30, blank=True)
    Approved = models.BooleanField()
    ApprovedBy = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='ApprovedBy', null=True, blank=True)
    def __str__(self):
        return self.Name


class ReadingSession(models.Model):
    Book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False)
    Date = models.DateField(blank=False,)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False)
    
    class Meta:
        unique_together = ('Book', 'User', 'Date')
        
    def __str__(self):
        return f"Book: {Book.Name}, Score: {self.Score}, Read by: {self.User.get_username()}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)