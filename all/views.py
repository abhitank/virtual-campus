from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PersonList(APIView):
    def get(self, request):
        response = {}
        password = request.data['password']
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        person_identifier = request.data['person_identifier']
        if 'person_identifier' and 'password' in request.data:
            if PersonPassword.objects.filter(password = hashed_password, user__person_identifier = person_identifier, is_deleted = False).exists():
                person = PersonPassword.objects.get(password = hashed_password, user__person_identifier = person_identifier, is_deleted = False).user
            
            else:
                response["result"] = 0
                response["errors"] = ["Password and user details doesn't matched"]
                return Response(response, status=status.HTTP_200_OK)
        else:
             response["result"] = 0
             response["errors"] = ["Submit complete details"]
             return Response(response, status=status.HTTP_200_OK)
        person_token = PersonToken.objects.get(user = person)
        person_token.save()
        serializer = PersonSerializer(person, many = False).data
        response['result'] = 1
        response['token'] = person_token.token
        response['data'] = serializer
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        response = {}
        token = request.data['token']
        person_identifier = request.data['person_identifier']
        person_type = request.data['person_type']
        person_name = request.data['person_name']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            new_person = Person(person_identifier = person_identifier, person_type = person_type, person_name = person_name)
            new_person.save()
            response['result'] = 1
            response['data'] = 'New user added successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 1
            response['data'] = 'You don\'t have permission to add new user'
            return Response(response, status=status.HTTP_200_OK)
        
class ResourceList(APIView):
    def get(self, request):
        response = {}
        token = request.data['token']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            queryset = Resource.objects.all()
            serializer = ResourceSerializer(queryset, many = True).data
            response['result'] = 1
            response['data'] = serializer
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to access resources'
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        response = {}
        token = request.data['token']
        resource_identifier = request.data['resource_identifier']
        resource_type = request.data['resource_type']
        resource_status = request.data['resource_status']
        resource_title = request.data['resource_title']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            resource = Resource(resource_identifier = resource_identifier, resource_type = resource_type, resource_status = resource_status, resource_title = resource_title)
            resource.save()
            response['result'] = 1
            response['data'] = 'New resource posted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to post new resource'
            return Response(response, status=status.HTTP_200_OK)
        
    def put(self, request):
        response = {}
        token = request.data['token']
        resource_identifier = request.data['resource_identifier']
        resource_type = request.data['resource_type']
        resource_status = request.data['resource_status']
        resource_title = request.data['resource_title']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            resource = Resource.objects.get(resource_identifier = resource_identifier)
            resource.resource_type = resource_type
            resource.resource_status = resource_status
            resource.resource_title = resource_title
            resource.save()
            response['result'] = 1
            response['data'] = 'Resource updated successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission update existing resource'
            return Response(response, status=status.HTTP_200_OK)
        
    def delete(self, request):
        response = {}
        token = request.data['token']
        resource_identifier = request.data['resource_identifier']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            resource = Resource.objects.get(resource_identifier = resource_identifier)
            resource.delete()
            response['result'] = 1
            response['data'] = 'Resource deleted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to delete existing resource'
            return Response(response, status=status.HTTP_200_OK)


class CourseDetailList(APIView):
    def get(self, request):
        response = {}
        token = request.data['token']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            queryset = CourseDetail.objects.all()
            serializer = CourseDetailSerializer(queryset, many = True).data
            response['result'] = 1
            response['data'] = serializer
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to see course details'
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        response = {}
        token = request.data['token']
        course_identifier = request.data['course_identifier']
        department = request.data['department']
        professor_1 = request.data['professor_1']
        professor_2 = request.data['professor_2']
        course_credits = request.data['course_credits']
        n = int(request.data["number"])
        student_enrolled = [] 
        for i in range(n):
            student_enrolled.append(request.data['student_enrolled'+str([i+1])])
        person = PersonToken.objects.get(token = token).user
        course = Resource.objects.get(resource_identifier = course_identifier)
        professor_1 = Person.objects.get(person_identifier = professor_1)
        professor_2 = Person.objects.get(person_identifier = professor_2)
        student = []
        for i in range(n):
            student.append(Person.objects.get(person_identifier = student_enrolled[i]))
        if person.person_type == 'Administrator':
            coursedetail = CourseDetail(course_title = course, department = department, professor_1 = professor_1, professor_2 = professor_2, course_credits = course_credits)
            coursedetail.save()
            for i in range(n):
                coursedetail.student_enrolled.add(student[i])
                coursedetail.save()
            response['result'] = 1
            response['data'] = 'New course details posted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to post new course details'
            return Response(response, status=status.HTTP_200_OK)
    
    def put(self, request):
        response = {}
        token = request.data['token']
        course_identifier = request.data['course_identifier']
        department = request.data['department']
        professor_1 = request.data['professor_1']
        professor_2 = request.data['professor_2']
        course_credits = request.data['course_credits']
        
        person = PersonToken.objects.get(token = token).user
        course = Resource.objects.get(resource_identifier = course_identifier)
        professor_1 = Person.objects.get(person_identifier = professor_1)
        professor_2 = Person.objects.get(person_identifier = professor_2)
        if person.person_type == 'Administrator':
            coursedetail = CourseDetail.objects.get(course_title = course)
            coursedetail.department = department
            coursedetail.professor_1 = professor_1
            coursedetail.professor_2 = professor_2
            coursedetail.course_credits = course_credits
            coursedetail.save()
            response['result'] = 1
            response['data'] = 'Course details updated successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to update existing course detail'
            return Response(response, status=status.HTTP_200_OK)
        
    def delete(self, request):
        response = {}
        token = request.data['token']
        course_identifier = request.data['course_identifier']
        person = PersonToken.objects.get(token = token).user
        course = Resource.objects.get(resource_identifier = course_identifier)
        if person.person_type == 'Administrator':
            coursedetail = CourseDetail.objects.get(course_title = course)
            coursedetail.delete()
            response['result'] = 1
            response['data'] = 'Course detail deleted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to delete course detail'
            return Response(response, status=status.HTTP_200_OK)
        

class FDPDetailList(APIView):
    def get(self, request):
        response = {}
        token = request.data['token']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            queryset = FDPDetail.objects.all()
            serializer = FDPDetailSerializer(queryset, many = True).data
            response['result'] = 1
            response['data'] = serializer
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to see FDP details'
            return Response(response, status=status.HTTP_200_OK)    
    
    def post(self, request):
         response = {}
         token = request.data['token']
         FDP_identifier = request.data['FDP_identifier']
         department = request.data['department']
         tutor = request.data['tutor']
         co_tutor = request.data['co_tutor']
         student_assigned = request.data['student_assigned']
         person = PersonToken.objects.get(token = token).user
         resource = Resource.objects.get(resource_identifier = FDP_identifier)
         tutor = Person.objects.get(person_identifier = tutor)
         co_tutor = Person.objects.get(person_identifier = co_tutor)
         student_assigned = Person.objects.get(person_identifier = student_assigned)
         if person.person_type == 'Administrator':
             fdpdetail = FDPDetail(FDP_title = resource, department= department, tutor = tutor, co_tutor = co_tutor, student_assigned = student_assigned)
             fdpdetail.save()
             response['result'] = 1
             response['data'] = 'New FDP detail posted successfully'
             return Response(response, status=status.HTTP_200_OK)
         else:
             response['result'] = 0
             response['errors'] = 'You don\'t have permission to post new FDP details'
             return Response(response, status=status.HTTP_200_OK)   
      
    def put(self, request):
        response = {}
        token = request.data['token']
        FDP_identifier = request.data['FDP_identifier']
        department = request.data['department']
        tutor = request.data['tutor']
        co_tutor = request.data['co_tutor']
        student_assigned = request.data['student_assigned']
        person = PersonToken.objects.get(token = token).user
        resource = Resource.objects.get(resource_identifier = FDP_identifier)
        tutor = Person.objects.get(person_identifier = tutor)
        co_tutor = Person.objects.get(person_identifier = co_tutor)
        student_assigned = Person.objects.get(person_identifier = student_assigned)
        if person.person_type == 'Administrator':
            fdpdetail = FDPDetail.objects.get(FDP_title = resource)
            fdpdetail.department = department
            fdpdetail.tutor = tutor
            fdpdetail.co_tutor = co_tutor
            fdpdetail.student_assigned = student_assigned
            fdpdetail.save()
            response["result"] = 1
            response["data"] = 'FDP details updated successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response["result"] = 0
            response["errors"] = 'You don\'t have permission to update existing FDP details'
            return Response(response, status=status.HTTP_200_OK) 
        
    def delete(self, request):
        response = {}
        token = request.data['token']
        FDP_identifier = request.data['FDP_identifier']
        person = PersonToken.objects.get(token = token).user
        resource = Resource.objects.get(resource_identifier = FDP_identifier)
        if person.person_type == 'Administrator':
            fdpdetail = FDPDetail.objects.get(FDP_title = resource)
            fdpdetail.delete()
            response['result'] = 1
            response['data'] = 'FDP details deleted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to delete existing FDP details'
            return Response(response, status=status.HTTP_200_OK)


class SeminarDetailList(APIView):
    def get(self, request):
        response = {}
        token = request.data['token']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            queryset = SeminarDetail.objects.all()
            serializer = SeminarDetailSerializer(queryset, many = True).data
            response['result'] = 1
            response['data'] = serializer
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to see seminar details'
            return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
         response = {}
         token = request.data['token']
         seminar_identifier = request.data['seminar_identifier']
         coordinator = request.data['coordinator']
         speaker = request.data['speaker']
         date = request.data['date']
         max_seats = request.data['max_seats']
         n = int(request.data["number"])
         student_enrolled = [] 
         for i in range(n):
             student_enrolled.append(request.data['student_enrolled'+str([i+1])])
         person = PersonToken.objects.get(token = token).user
         resource = Resource.objects.get(resource_identifier = seminar_identifier)
         coordinator = Person.objects.get(person_identifier = coordinator)
         speaker = Person.objects.get(person_identifier = speaker)
         student = []
         for i in range(n):
             student.append(Person.objects.get(person_identifier = student_enrolled[i]))
         if person.person_type == 'Administrator':
             seminardetail = SeminarDetail(seminar_title = resource, coordinator = coordinator, speaker = speaker, date = date, max_seats = max_seats)
             seminardetail.save()
             for i in range(n):
                seminardetail.student_enrolled.add(student[i])
                seminardetail.save()
             response['result'] = 1
             response['data'] = 'New seminar details posted successfully'
             return Response(response, status=status.HTTP_200_OK)
         else:
             response['result'] = 0
             response['errors'] = 'You don\'t have permission to post new seminar details'
             return Response(response, status=status.HTTP_200_OK)   
    
    def put(self, request):
        response = {}
        token = request.data['token']
        seminar_identifier = request.data['seminar_identifier']
        coordinator = request.data['coordinator']
        speaker = request.data['speaker']
        date = request.data['date']
        max_seats = request.data['max_seats']
        person = PersonToken.objects.get(token = token).user
        resource = Resource.objects.get(resource_identifier = seminar_identifier)
        coordinator = Person.objects.get(person_identifier = coordinator)
        speaker = Person.objects.get(person_identifier = speaker)
        if person.person_type == 'Administrator':
            seminardetail = SeminarDetail.objects.get(seminar_title = resource)
            seminardetail.coordinator = coordinator
            seminardetail.speaker = speaker
            seminardetail.date = date
            seminardetail.max_seats = max_seats
            seminardetail.save()
            response['result'] = 1
            response['data'] = 'Seminar details updated successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['errors'] = 'You don\'t have permission to update exisiting seminar details'
            return Response(response, status=status.HTTP_200_OK) 
    
    def delete(self, request):
        response = {}
        token = request.data['token']
        seminar_identifier = request.data['seminar_identifier']
        person = PersonToken.objects.get(token = token).user
        resource = Resource.objects.get(resource_identifier = seminar_identifier)
        if person.person_type == 'Administrator':
            seminardetail = SeminarDetail.objects.get(seminar_title = resource)
            seminardetail.delete()
            response['result'] = 1
            response['data'] = 'Seminar details deleted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['errors'] = 'You don\'t have permission to delete seminar details'
            return Response(response, status=status.HTTP_200_OK)            


class StudentDetailList(APIView):
    def get(self, request):
        response = {}
        token = request.data['token']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            queryset = StudentDetail.objects.all()
            serializer = StudentDetailSerializer(queryset, many = True).data
            response['result'] = 1
            response['data'] = serializer
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to view student details'
            return Response(response, status=status.HTTP_200_OK)
            
    def post(self, request):
         response = {}
         token = request.data['token']
         student_identifier = request.data['student_identifier']
         department = request.data["department"]
         n = int(request.data['number'])
         resource_taken = []
         for i in range(n):
             resource_taken.append(request.data['resource_taken' + str([i+1])])
         person = PersonToken.objects.get(token = token).user
         student = Person.objects.get(person_identifier = student_identifier)
         resources = []
         for i in range(n):
             resources.append(Resource.objects.get(resource_identifier = resource_taken[i]))    
         if person.person_type == 'Administrator':
             studentdetail = StudentDetail(student_name = student, department = department) 
             studentdetail.save()
             for i in range(n):
                 studentdetail.resource_taken.add(resources[i])
                 studentdetail.save()
             response['result'] = 1
             response['data'] = 'Student details posted successfully'
             return Response(response, status=status.HTTP_200_OK)
         else:
             response['result'] = 0
             response['errors'] = 'You don\'t have permission to post student details'
             return Response(response, status=status.HTTP_200_OK)   
      
    def put(self, request):
        response = {}
        token = request.data["token"]
        student_identifier = request.data["student_identifier"]
        department = request.data["department"]
        person = PersonToken.objects.get(token = token).user
        student = Person.objects.get(person_identifier = student_identifier)
        if person.person_type == 'Administrator':
            studentdetail = StudentDetail.objects.get(student_name = student)
            studentdetail.department = department
            studentdetail.save()
            response['result'] = 1
            response['data'] = 'Student details updated successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['errors'] = 'You don\'t have permission to update student details'
            return Response(response, status=status.HTTP_200_OK) 
    
    def delete(self, request):
        response = {}
        token = request.data["token"]
        student_identifier = request.data["student_identifier"]
        person = PersonToken.objects.get(token = token).user
        student = Person.objects.get(person_identifier = student_identifier)
        if person.person_type == 'Administrator':
            studentdetail = StudentDetail.objects.get(student_name = student)
            studentdetail.delete()
            response['result'] = 1
            response['data'] = 'Student details deleted successfully'
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['errors'] = 'You don\'t have permission to delete student details'
            return Response(response, status=status.HTTP_200_OK) 
        
        
class ProfessorDetailList(APIView):
    def get(self, request):
        response = {}
        token = request.data['token']
        person = PersonToken.objects.get(token = token).user
        if person.person_type == 'Administrator':
            queryset = ProfessorDetail.objects.all()
            serializer = ProfessorDetailSerializer(queryset, many = True).data
            response['result'] = 1
            response['data'] = serializer
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['error'] = 'You don\'t have permission to view professor details'
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
         response = {}
         token = request.data["token"]
         professor_identifier = request.data["professor_identifier"]
         department = request.data["department"]
         n = int(request.data['number'])
         resource_undertaken = []
         for i in range(n):
             resource_undertaken.append(request.data['resource_undertaken' + str([i+1])])
         person = PersonToken.objects.get(token = token).user
         professor = Person.objects.get(person_identifier = professor_identifier)
         resources = []
         for i in range(n):
             resources.append(Resource.objects.get(resource_identifier = resource_undertaken[i]))
         if person.person_type == 'Administrator':
             professordetail = ProfessorDetail(professor_name = professor, department = department) 
             professordetail.save()
             for i in range(n):
                 professordetail.resource_undertaken.add(resources[i])
                 professordetail.save()
             response['result'] = 1
             response['data'] = 'New professor details posted successfully'
             return Response(response, status=status.HTTP_200_OK)
         else:
             response['result'] = 0
             response['errors'] = 'You don\'t have permission to post professor details'
             return Response(response, status=status.HTTP_200_OK)   
    
    def put(self, request):
        response = {}
        token = request.data["token"]
        professor_identifier = request.data["professor_identifier"]
        department = request.data["department"]
        person = PersonToken.objects.get(token = token).user
        professor = Person.objects.get(person_identifier = professor_identifier)
        if person.person_type == 'Administrator':
            professordetail = ProfessorDetail.objects.get(professor_name = professor)
            professordetail.department = department
            professordetail.save()
            response['result'] = 1
            response['data'] = "Professor detail updated successfully"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['errors'] = 'You don\'t have permission to update professor details'
            return Response(response, status=status.HTTP_200_OK) 
    
    def delete(self, request):
        response = {}
        token = request.data["token"]
        professor_identifier = request.data["professor_identifier"]
        person = PersonToken.objects.get(token = token).user
        professor = Person.objects.get(person_identifier = professor_identifier)
        if person.person_type == 'Administrator':
            professordetail = ProfessorDetail.objects.get(professor_name = professor)
            professordetail.delete()
            response['result'] = 1
            response['data'] = "Professor details deleted successfully"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['result'] = 0
            response['errors'] = 'You don\'t have permission to delete professor details'
            return Response(response, status=status.HTTP_200_OK)  