from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile_number=mobile_number
        )
        user.is_active = True  
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_number']

    def __str__(self):
        return self.email

class Expense(models.Model):
    SPLIT_METHODS = (
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    )
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.FloatField()
    split_details = models.JSONField()
    split_method = models.CharField(max_length=10, choices=SPLIT_METHODS)
    participants = models.ManyToManyField(User, related_name='participating_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
