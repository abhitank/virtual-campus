import os
import random
import datetime
import hashlib

from datetime import timedelta
from django.db import models

class Resource(models.Model):
    resource_identifier = models.CharField(blank = True, null = True, max_length = 7)
    RESOURCE_TYPE = (
            ('Course' , 'Course'),
            ('FDP' , 'FDP'),
            ('Seminar' , 'Seminar')
            )
            
    RESOURCE_STATUS = (
            ('Created' , 'Created'),
            ('In Progress' , 'In Progress'),
            ('Completed' , 'Completed')
            )
    resource_type = models.CharField(max_length = 100, choices = RESOURCE_TYPE)
    resource_title = models.CharField(blank = True, null = True, max_length = 100)
    resource_status = models.CharField(max_length = 100, choices = RESOURCE_STATUS)
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.resource_title)
    
    class Meta:
        verbose_name_plural = 'Resource'
        
class CourseDetail(models.Model):
    course_title = models.ForeignKey('Resource', related_name = 'course_detail', on_delete=models.CASCADE, null = True)
    DEPARTMENT = (
            ('CS' , 'CS'),
            ('Civil' , 'Civil'),
            ('Electrical' , 'Electrical'),
            ('Mechanical' , 'Mechanical')
            )
    department =  models.CharField(max_length = 100, choices = DEPARTMENT) 
    professor_1 = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'professor_1')
    professor_2 = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'professor_2')
    COURSE_CREDITS = (
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7)
            )
    course_credits = models.IntegerField(choices = COURSE_CREDITS)
    student_enrolled = models.ManyToManyField('Person')
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.course_title)
    
    class Meta:
        verbose_name_plural = 'CourseDetail'
        
class FDPDetail(models.Model):
    FDP_title = models.ForeignKey('Resource', on_delete=models.CASCADE, related_name = 'FDP_detail', null = True)
    DEPARTMENT = (
            ('CS' , 'CS'),
            ('Civil' , 'Civil'),
            ('Electrical' , 'Electrical'),
            ('Mechanical' , 'Mechanical')
            )
    department = models.CharField(max_length = 100, choices = DEPARTMENT)
    tutor = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'tutor')
    co_tutor = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'co_tutor')
    student_assigned = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'student_assigned')
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.FDP_title)
    
    class Meta:
        verbose_name_plural = 'FDPDetail'
        
class SeminarDetail(models.Model):
    seminar_title = models.ForeignKey('Resource', on_delete=models.CASCADE, related_name = 'seminar_detail', null = True)
    coordinator = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'coordinator')
    speaker = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'speaker')
    date = models.DateField()
    max_seats = models.IntegerField()
    student_enrolled = models.ManyToManyField('Person')
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.seminar_title)
    
    class Meta:
        verbose_name_plural = 'SeminarDetail'
        
class Person(models.Model):
    person_identifier = models.CharField(blank = True, null = True, max_length = 7)
    PERSON_TYPE = (
            ('Student', 'Student'),
            ('Professor', 'Professor'),
            ('Administrator', 'Administrator')
            )
    person_type = models.CharField(max_length = 100, choices = PERSON_TYPE)
    person_name = models.CharField(blank = True, null = True, max_length = 100)
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    def __str__(self):
        return str(self.person_name)
    
    class Meta:
        verbose_name_plural = 'Person'
        
class StudentDetail(models.Model):
    student_name = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'student_detail', null = True)
    DEPARTMENT = (
            ('CS' , 'CS'),
            ('Civil' , 'Civil'),
            ('Electrical' , 'Electrical'),
            ('Mechanical' , 'Mechanical')
            )
    department = models.CharField(max_length = 100, choices = DEPARTMENT)
    resource_taken = models.ManyToManyField('Resource')
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.student_name)
    
    class Meta:
        verbose_name_plural = 'StudentDetail'
        
class ProfessorDetail(models.Model):
    professor_name = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'professor_detail', null = True)
    DEPARTMENT = (
            ('Civil', 'Civil'),
            ('Computer Science','Computer Science'), 
            ('Electrical','Electrical'), 
            ('Mechanical', 'Mechanical'),
            ('Metallurgy', 'Metallurgy')
            )
    department =  models.CharField(max_length = 100, choices = DEPARTMENT)
    resource_undertaken = models.ManyToManyField('Resource')
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(blank = True, null = True, default = datetime.datetime.now)
    
    def __str__(self):
        return str(self.professor_name)
    
    class Meta:
        verbose_name_plural = 'ProfessorDetail'

class PersonPassword(models.Model):
    user = models.ForeignKey('Person', on_delete=models.CASCADE, related_name = 'user')
    password = models.CharField(blank = True, max_length = 100)
    password_open = models.CharField(blank = False, max_length = 100)
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(null = True, blank = True, default = datetime.datetime.now)
    def save(self, *args, **kwargs):
        self.password = hashlib.md5(self.password_open.encode()).hexdigest()
        super(PersonPassword, self).save(*args, **kwargs)
        
class PersonToken(models.Model):
    user = models.ForeignKey('Person', on_delete=models.CASCADE,)
    token  = models.CharField(blank = True, max_length = 100)
    created_at = models.DateTimeField(null=True, blank = True, default = datetime.datetime.now)
    
    def save(self, *args, **kwargs):
        self.token = "".join([random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for i in range(32)])
        super(PersonToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.token

    class Meta:
        verbose_name_plural = "PersonToken"