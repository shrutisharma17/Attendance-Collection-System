from django.db import models
types = [('Student','Student'),('Faculty','Faculty')]

# it is the schema of the user profile used to upload it to database.
class  Student_profile(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    #date = models.DateField()
    phone = models.BigIntegerField()
    email = models.EmailField()
    roll_number = models.IntegerField()
    profession = models.CharField(choices=types,max_length=20,null=True,blank=False,)
    class_name = models.CharField(max_length=70)
    subject_code = models.CharField(max_length=70)
    present = models.BooleanField(default=False)
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name +' '+self.last_name


class LastFace(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.last_face

