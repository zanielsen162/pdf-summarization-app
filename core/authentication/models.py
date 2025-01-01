from django.db import models
from django.contrib.auth.models import User


# # Create your models here.
# class ToDoList(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True) # <--- added
#     name = models.CharField(max_length=200)

#     def __str__(self):
# 	return self.name


# class Item(models.Model):
#     todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
#     text = models.CharField(max_length=300)
#     complete = models.BooleanField()

#     def __str__(self):
# 	return self.text

class PromptModel(models.Model):
    field = models.CharField(max_length=255)
    topics = models.CharField(max_length=255)
    file = models.FileField()

class PrevResponses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="previous_responses", null=True, blank=True) # <--- added


class Response(models.Model):
    previous_responses = models.ForeignKey(
        PrevResponses,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=500)
    content = models.TextField()