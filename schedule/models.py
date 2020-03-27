from django.db import models


class Groups(models.Model):
    name = models.CharField(max_length=20, unique=True)
    course = models.SmallIntegerField(null=True, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    is_evening = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)

    class Meta:
        verbose_name_plural = 'Group'
        verbose_name = 'group'


class Teacher(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=150, unique=True)
    color = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class LessonType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str('{}: {}'.format(self.id, self.name))


class Lesson(models.Model):
    LESSON_WEEK = (
        (1, 'even'),
        (2, 'odd'),
        (3, 'both')
    )
    DAYS_OF_WEEK = (
        (1, 'monday'),
        (2, 'tuesday'),
        (3, 'wednesday'),
        (4, 'thursday'),
        (5, 'friday'),
        (6, 'saturday'),
        (7, 'sunday'),
    )
    name = models.CharField(max_length=200)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    number = models.IntegerField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    classrooms = models.ManyToManyField(Classroom)
    teachers = models.ManyToManyField(Teacher)
    type = models.ForeignKey(LessonType, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    week = models.IntegerField(choices=LESSON_WEEK)

    def __str__(self):
        return '{} {}'.format(self.name, self.group)


class Notification(models.Model):
    time = models.DateTimeField()
    old_lesson = models.TextField()
    new_lesson = models.TextField()
