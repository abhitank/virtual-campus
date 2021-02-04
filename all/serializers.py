from rest_framework import serializers
from .models import *

class CourseDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.StringRelatedField()
    professor_1 = serializers.StringRelatedField()
    professor_2 = serializers.StringRelatedField()
    student_enrolled = serializers.StringRelatedField(many = True)
    class Meta:
        model = CourseDetail
        fields = ['course_title', 'department', 'professor_1', 'professor_2', 'course_credits', 'created_at', 'student_enrolled']
        
class FDPDetailSerializer(serializers.ModelSerializer):
    FDP_title = serializers.StringRelatedField()
    tutor = serializers.StringRelatedField()
    co_tutor = serializers.StringRelatedField()
    student_assigned = serializers.StringRelatedField()
    class Meta:
        model = FDPDetail
        fields = ['FDP_title', 'department', 'tutor', 'co_tutor', 'student_assigned', 'created_at']
        
class SeminarDetailSerializer(serializers.ModelSerializer):
    seminar_title = serializers.StringRelatedField()
    speaker = serializers.StringRelatedField()
    coordinator = serializers.StringRelatedField()
    student_enrolled = serializers.StringRelatedField(many = True)
    class Meta:
        model = SeminarDetail
        fields = ['seminar_title', 'coordinator', 'speaker', 'date', 'max_seats', 'created_at', 'student_enrolled']

class ResourceSerializer(serializers.ModelSerializer):
    course_detail = CourseDetailSerializer(many = True)
    FDP_detail = FDPDetailSerializer(many = True)
    seminar_detail = SeminarDetailSerializer(many = True)
    class Meta:
        model = Resource
        fields = ['resource_identifier', 'resource_type', 'resource_status', 'resource_title', 'created_at', 'course_detail', 'FDP_detail', 'seminar_detail']

class StudentDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.StringRelatedField()
    resource_taken = serializers.StringRelatedField(many = True)
    class Meta:
        model = StudentDetail
        fields = ['student_name', 'department', 'created_at', 'resource_taken']
    

class ProfessorDetailSerializer(serializers.ModelSerializer):
    professor_name = serializers.StringRelatedField()
    resource_undertaken = serializers.StringRelatedField(many = True)
    class Meta:
        model = ProfessorDetail
        fields = ['professor_name', 'department', 'created_at', 'resource_undertaken']

class PersonSerializer(serializers.ModelSerializer):
    student_detail = StudentDetailSerializer(many = True)
    professor_detail = ProfessorDetailSerializer(many = True)
    class Meta:
        model = Person
        fields = ['person_identifier', 'person_type', 'person_name', 'created_at', 'student_detail', 'professor_detail']