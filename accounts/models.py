from django.db import models
from django.contrib.auth.models import AbstractUser

SEMESTERS = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
]



class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(TimeStamp):
    DEPARTMENTS = [
        ('CSE', 'Computer Science Engineering'),
        ('CE', 'Civil Engineering'),
        ('CHE', 'Chemical Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
    ]
    name = models.CharField(max_length=100, choices=DEPARTMENTS, unique=True)

    def __str__(self):
        return self.get_name_display()


class Subject(TimeStamp):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='subject', on_delete=models.CASCADE)
    # teacher = models.ForeignKey(User, related_name='subject', on_delete=models.CASCADE, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True, choices=SEMESTERS)

    def __str__(self):
        return self.name


class User(AbstractUser, TimeStamp):
    USER_TYPES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    TEACHING_POSITIONS = [
        ('HOD', 'Head of the Department'),
        ('Professor', 'Professor'),
        ('Asscociate Professor', 'Associate Professor'),
        ('Asstistant Professor', 'Assistant Professor'),
        ('Senior Lecturer', 'Senior Lecturer'),
        ('Guest Lecturer', 'Guest Lecturer'),
    ]

    user_type = models.CharField(max_length=7, choices=USER_TYPES, default='student')
    # name = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='users')
    department = models.ForeignKey(Department, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    roll_number = models.CharField(max_length=8, unique=True, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(null=True, blank=True, choices=SEMESTERS)
    year_of_admission = models.PositiveIntegerField(choices=list(zip(range(2014, 2021), range(2014, 2021))),null=True, blank=True)
    position = models.CharField(max_length=30, null=True, blank=True, choices=TEACHING_POSITIONS)
    profile_pic = models.ImageField(null=True, blank=True)

