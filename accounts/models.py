from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
import datetime
class UserManger(BaseUserManager):
    def create_user(self,phone,password=None):
        if not phone:
            raise ValueError("User Must have an Phone")
        if not password:
            raise ValueError('User Must have as Password')

        user = self.model(
            phone = phone
        )
        user.set_password(password)
        user.is_admin = False

        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self,phone,password=None):
        if not phone:
            raise ValueError("User Must have an Phone")
        if not password:
            raise ValueError('User Must have as Password')

        user = self.model(
            phone = phone
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    gender = models.CharField(max_length=10,choices=GenderChoices.choices,default=GenderChoices.MALE)
    country_code = models.CharField(max_length=10)

    # phone = PhoneNumberField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11,unique=True) # validators should be a list
    avatar = models.ImageField(upload_to="user_images/",null=True,blank=True)
    birthdate = models.DateField(default=datetime.date.today)
    email = models.CharField(max_length=255,null=True,blank=True)
    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    objects = UserManger()


    def get_full_name(self):
        # The user is identified by their email address
        return self.phone

    def get_short_name(self):
        # The user is identified by their email address
        return self.phone

    def __str__(self):
        return f"{self.phone}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True





class Status(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.status}"