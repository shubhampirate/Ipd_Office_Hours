from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status,permissions,viewsets
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token

from .models import User, Profile, FingerPrint, Location, Attendance, Timer, Efficiency, Project, ProjectEmployee, Task, Review, Meeting, Attendee, Notification
from .serializers import AttendanceSerializer, LocationSerializer, LoginSerializer, NotificationSerializer, ProfileSerializer, ProjectSerializer, TaskSerializer

@api_view(['GET',])
def home(request):
    return JsonResponse({"Hello":"Welcome to APIs"})

class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request):
		email = request.data.get('email',None)
		password = request.data.get('password',None)
		user = authenticate(email = email, password = password)
		if user :
			serializer = self.serializer_class(user)
			token,k = Token.objects.get_or_create(user=user)
			return JsonResponse({'token' : token.key,'email' : user.email},status = status.HTTP_200_OK, safe = False)
		return JsonResponse('Invalid Credentials',status = status.HTTP_404_NOT_FOUND, safe = False)

class ProfileAPI(GenericAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        try:
            obj = Profile.objects.get(user = request.user)
            serializer = self.serializer_class(obj)
            return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)
        except:
            return JsonResponse('Profile Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

    def post(self,request):
        #Create Profile
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data,status = status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)

    def patch(self,request):
        #Profile patch by Admin
        try:
            prof = Profile.objects.get(user = request.user)
            if prof.role != Profile.ADMIN:
                return JsonResponse('Only admins can update data! ',status = status.HTTP_403_FORBIDDEN, safe = False)
            obj = Profile.objects.get(user = request.data['user'])
            serializer = self.serializer_class(obj, data = request.data, partial =True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data,status = status.HTTP_202_ACCEPTED, safe = False)
            return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)
        except:
            return JsonResponse('Profile Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

    def delete(self,request):
        try:
            obj = Profile.objects.get(user = request.data['user'])
            obj.delete()
            return JsonResponse({'success':'success'},status = status.HTTP_202_ACCEPTED, safe = False)
        except:
            return JsonResponse('Profile Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

@api_view(['GET',])
def all_employees(request):
    obj = Profile.objects.all()
    serializer = ProfileSerializer(obj, many = True)
    return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)

@api_view(['GET',])
def view_employee(request,pk):
    try:
        obj = Profile.objects.get(user = pk)
        serializer = ProfileSerializer(obj)
        return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)
    except:
        return JsonResponse('Profile Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

class LocationAPI(GenericAPIView):

    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        try:
            prof = Profile.objects.get(user = request.user)
            obj = Location.objects.filter(profile = prof)
            serializer = self.serializer_class(obj, many = True)
            return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)
        except:
            return JsonResponse('No location Assignment',status = status.HTTP_404_NOT_FOUND, safe = False)

    def post(self,request):
        #Assign Location
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data,status = status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)

    def patch(self,request):
        #Location patch by Admin
        try:
            prof = Profile.objects.get(user = request.user)
            if prof.role != Profile.ADMIN:
                return JsonResponse('Only admins can update data! ',status = status.HTTP_403_FORBIDDEN, safe = False)
            obj = Location.objects.get(profile = request.data['profile'])
            serializer = self.serializer_class(obj, data = request.data, partial =True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data,status = status.HTTP_202_ACCEPTED, safe = False)
            return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)
        except:
            return JsonResponse('Location Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

    def delete(self,request):
        try:
            obj = Location.objects.get(profile = request.data['user'])
            obj.delete()
            return JsonResponse({'success':'success'},status = status.HTTP_202_ACCEPTED, safe = False)
        except:
            return JsonResponse('Location Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

class AttendanceAPI(GenericAPIView):

    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        try:
            prof = Profile.objects.get(user = request.user)
            obj = Attendance.objects.filter(profile = prof)
            serializer = self.serializer_class(obj, many = True)
            return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)
        except:
            return JsonResponse('No Attendance Report',status = status.HTTP_404_NOT_FOUND, safe = False)

class ProjectAPI(GenericAPIView):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        proem = ProjectEmployee.objects.filter(member__user = request.user)
        obj = Project.objects.filter(id__in = proem)
        serializer = self.serializer_class(obj, many = True)
        return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)

    def post(self,request):
        #Assign Project
        prof = Profile.objects.get(user = request.user)
        request.data['leader'] = prof
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data,status = status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)

    def patch(self,request):
        #Project patch by Admin
        try:
            prof = Profile.objects.get(user = request.user)
            obj = Project.objects.get(title = request.data['title'])
            if obj.leader != prof:
                return JsonResponse('Only leaders can update !',status = status.HTTP_403_FORBIDDEN, safe = False)
            serializer = self.serializer_class(obj, data = request.data, partial =True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data,status = status.HTTP_202_ACCEPTED, safe = False)
            return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)
        except:
            return JsonResponse('Project Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

    def delete(self,request):
        try:
            prof = Profile.objects.get(user = request.user)
            obj = Project.objects.get(title = request.data['title'])
            if obj.leader != prof:
                return JsonResponse('Only leaders can delete !',status = status.HTTP_403_FORBIDDEN, safe = False)
            obj.delete()
            return JsonResponse({'success':'success'},status = status.HTTP_202_ACCEPTED, safe = False)
        except:
            return JsonResponse('Project Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

class TaskAPI(GenericAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        prof = Profile.objects.get(user = request.user)
        obj1 = Task.objects.filter(assigned_to = prof)
        obj2 = Task.objects.filter(assigned_by = prof)
        serializer1 = self.serializer_class(obj1, many = True)
        serializer2 = self.serializer_class(obj2, many = True)
        dict = {'assigned_to_me':serializer1.data, 'assigned_by_me':serializer2.data}
        return JsonResponse(dict,status = status.HTTP_200_OK, safe = False)

    def post(self,request):
        #Assign Task
        prof = Profile.objects.get(user = request.user)
        request.data['assigned_by'] = prof
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data,status = status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)

    def patch(self,request):
        #Task patch by Admin
        try:
            prof = Profile.objects.get(user = request.user)
            obj = Task.objects.get(title = request.data['title'])
            if obj.assigned_by != prof:
                return JsonResponse('Only leaders can update !',status = status.HTTP_403_FORBIDDEN, safe = False)
            serializer = self.serializer_class(obj, data = request.data, partial =True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data,status = status.HTTP_202_ACCEPTED, safe = False)
            return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)
        except:
            return JsonResponse('Task Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

    def delete(self,request):
        try:
            prof = Profile.objects.get(user = request.user)
            obj = Task.objects.get(title = request.data['title'])
            if obj.assigned_by != prof:
                return JsonResponse('Only leaders can delete !',status = status.HTTP_403_FORBIDDEN, safe = False)
            obj.delete()
            return JsonResponse({'success':'success'},status = status.HTTP_202_ACCEPTED, safe = False)
        except:
            return JsonResponse('Project Does not exist',status = status.HTTP_404_NOT_FOUND, safe = False)

class MeetingAPI:
    #Coming Soon
    pass

class NotificationAPI(GenericAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        prof = Profile.objects.get(user = request.user)
        obj = Notification.objects.filter(receiver = prof).order_by('-sent_at')
        serializer = self.serializer_class(obj, many = True)
        return JsonResponse(serializer.data,status = status.HTTP_200_OK, safe = False)

    def post(self,request):
        prof = Profile.objects.get(user = request.user)
        request.data['sender'] = prof
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data,status = status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors,status = status.HTTP_400_BAD_REQUEST, safe = False)