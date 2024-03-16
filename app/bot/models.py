from django.db import models


class User(models.Model):
    class Meta:
        db_table = "users"

    user_id = models.IntegerField(primary_key=True)
    chat_id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)


class Schedule(models.Model):
    class Meta:
        db_table = "schedule"

    lesson = models.TextField()
    format = models.TextField()
    date = models.TextField()
    hours = models.TextField()
    minutes = models.TextField()
    users_number = models.IntegerField()
    additional_info = models.TextField()
    id = models.BigAutoField(primary_key=True)


class Practice(models.Model):
    class Meta:
        db_table = "practices"

    user_id = models.IntegerField()
    lessons = models.TextField()
    format = models.TextField()
    date = models.TextField()
    hours = models.TextField()
    minutes = models.TextField()
    id = models.BigAutoField(primary_key=True)


class LessonTitle(models.Model):
    class Meta:
        db_table = "lessons_title"

    title = models.TextField()
    id = models.BigAutoField(primary_key=True)


class QuitedPractice(models.Model):
    class Meta:
        db_table = "quited_practice"

    practice = models.TextField()
    reason = models.TextField()
    id = models.BigAutoField(primary_key=True)


class LastBotMessage(models.Model):
    class Meta:
        db_table = "last_bot_message"

    user_id = models.IntegerField()
    message_number = models.IntegerField()
    id = models.BigAutoField(primary_key=True)


class WorkshopsSchedule(models.Model):
    class Meta:
        db_table = "workshops_schedule"

    title = models.TextField()
    format = models.TextField()
    date = models.TextField()
    hours = models.TextField()
    minutes = models.TextField()
    users_number = models.IntegerField()
    additional_info = models.TextField()
    id = models.BigAutoField(primary_key=True)


class Workshop(models.Model):
    class Meta:
        db_table = "workshops"

    user_id = models.IntegerField()
    title = models.TextField()
    format = models.TextField()
    date = models.TextField()
    hours = models.TextField()
    minutes = models.TextField()
    id = models.BigAutoField(primary_key=True)


class WorkshopTitle(models.Model):
    class Meta:
        db_table = "workshops_title"

    title = models.TextField()
    id = models.BigAutoField(primary_key=True)


class QuitedWorkshop(models.Model):
    class Meta:
        db_table = "quited_workshops"

    workshop = models.TextField()
    reason = models.TextField()
    id = models.BigAutoField(primary_key=True)
