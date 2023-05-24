from django.db import models

class Class(models.Model):
    name = models.CharField("class_name", max_length=100)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField("unit_name", max_length=100)
    parent = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField("lesson_name", max_length=100)
    parent = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField("Question", max_length=500)
    answer = models.CharField("Answer", max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default="temp_lesson")

    def __str__(self):
        if len(self.question) < 20: return self.question
        return self.question[:20] + "..."

class History(models.Model):
    message = models.CharField("Message", max_length=500)
    is_from_bot = models.BooleanField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.message) < 20: return self.message
        return self.message[:20] + "..."
