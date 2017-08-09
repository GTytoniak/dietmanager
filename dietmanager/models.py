from django.db import models
from django.contrib.auth.models import User


CATEGORY = (
    (1, "breakfast"), 
    (2, "brunch"), 
    (3, "dinner"), 
    (4, "supper"), 
)

SEX = (
    (1.0, "Man"),
    (0.9, "Woman"),    
    )

ACTIVITY = (
    (1.0, "Small activity, sitting job"),
    (1.1, "Sporadic activity(once a week), sitting job"),
    (1.2, "Activity 1-2 times a week, sitting job"),
    (1.3, "Intense activity (eg. fitness) 2-3 times a week, sitting job"),
    (1.4, "Activity everyday (eg. fitness, joggin), job requires movement"),
    (1.5, "Doing a lot of movement all the time, physical job"),
)
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)
    kcal =  models.IntegerField(null=True)
    food_category = models.IntegerField(choices=CATEGORY)
    protein = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    carbohydrate = models.FloatField(null=True)
    roughage = models.FloatField(null=True)
    sugar = models.FloatField(null=True)
    
    def __str__(self):
        return str(self.name, self.kcal)
    
class UserData(models.Model):
    user = models.OneToOneField(User)
    height = models.FloatField(null=False)
    weight = models.IntegerField(null=False)
    
class Bmi(models.Model):
    user = models.OneToOneField(User)
    bmi = models.FloatField()
    
    def __str__(self):
        return str(self.bmi)
    
class UserMoreData(models.Model):
    user = models.OneToOneField(User) 
    weight = models.IntegerField(null=False)
    sex = models.FloatField(choices=SEX)
    activity = models.FloatField(choices=ACTIVITY)
    
class Gda(models.Model):
    user = models.OneToOneField(User)
    gda = models.FloatField()
    
    def __str__(self):
        return str(self.gda)
    

    
