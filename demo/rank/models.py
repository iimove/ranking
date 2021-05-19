from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.

class RankUser(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=16, null=True, unique=True)
    password = models.CharField(verbose_name='密码', max_length=16, null=True)
    userNumber = models.CharField(verbose_name='客户端号', max_length=16, null=True, unique=True)
    fraction = models.IntegerField(verbose_name='分数',
                                   default=None,
                                   validators=[
                                       MaxValueValidator(10000000),
                                       MinValueValidator(1)
                                   ])


class Rank(models.Model):
    user = models.OneToOneField(RankUser, on_delete=models.CASCADE, primary_key=True)
    rank = models.IntegerField(verbose_name='名次', validators=[MinValueValidator(1)])
