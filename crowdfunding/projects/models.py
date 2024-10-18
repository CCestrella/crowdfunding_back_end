from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)

class Pledge(models.Model):
    amount = models.IntegerField() # The amount of money the donor is pledging
    comment = models.CharField(max_length=200) # An optional comment from the donor
    anonymous = models.BooleanField() # Whether the donor wants to stay anonymous
    project = models.ForeignKey(
        'Project', # This links the pledge to a specific project (athlete)
        on_delete=models.CASCADE, # If the project (athlete) is deleted, all pledges will also be deleted
        related_name='pledges' # This allows you to access all pledges linked to a specific project 
    )
