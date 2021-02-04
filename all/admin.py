from django.contrib import admin
from .models import *

class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    list_display = ['resource_identifier', 'resource_type', 'resource_title', 'resource_status']
    
class CourseDetailAdmin(admin.ModelAdmin):
    model = CourseDetail
    list_display = ['course_title', 'department', 'professor_1', 'professor_2', 'course_credits']
    
class FDPDetailAdmin(admin.ModelAdmin):
    model = FDPDetail
    list_display = ['FDP_title', 'department', 'tutor', 'co_tutor', 'student_assigned']
    
class SeminarDetailAdmin(admin.ModelAdmin):
    model = SeminarDetail
    list_display = ['seminar_title', 'coordinator', 'speaker', 'date', 'max_seats']
    
class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['person_identifier', 'person_type', 'person_name']
    
class StudentDetailAdmin(admin.ModelAdmin):
    model = StudentDetail
    list_display = ['student_name', 'department']
    
class ProfessorDetailAdmin(admin.ModelAdmin):
    model = ProfessorDetail
    list_display = ['professor_name', 'department']
    
class PersonPasswordAdmin(admin.ModelAdmin):
    model = PersonPassword
    list_display = ['user', 'password_open']
    
class PersonTokenAdmin(admin.ModelAdmin):
    model = PersonToken
    list_display = ['user', 'token']
    
admin.site.register(Resource, ResourceAdmin)
admin.site.register(CourseDetail, CourseDetailAdmin)
admin.site.register(FDPDetail, FDPDetailAdmin)
admin.site.register(SeminarDetail, SeminarDetailAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(StudentDetail, StudentDetailAdmin)
admin.site.register(ProfessorDetail, ProfessorDetailAdmin)
admin.site.register(PersonPassword, PersonPasswordAdmin)
admin.site.register(PersonToken, PersonTokenAdmin)