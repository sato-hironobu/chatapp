from django.db import models

class FAQ(models.Model):
    question = models.CharField("Question", max_length=500)
    answer = models.CharField("Answer", max_length=500)

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
