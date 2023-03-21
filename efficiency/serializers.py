from rest_framework import serializers
from .models import User, Profile, FingerPrint, Location, Attendance, Timer, Efficiency, Project, ProjectEmployee, Task, Review, Meeting, Attendee, Notification

class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=32,min_length=8,write_only = True)
    
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','phone']

class FingerPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = FingerPrint
        fields = '__all__'

class EfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Efficiency
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    efficiency = serializers.SerializerMethodField(read_only=True)
    fingerprints = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = ['user','name','role','joining_date','picture','efficiency','fingerprints']

    def get_fingerprints(self,obj):
        objs = FingerPrint.objects.filter(profile = obj)
        serializer = FingerPrintSerializer(objs,many=True)
        return serializer.data

    def get_efficiency(self,obj):
        objs = Efficiency.objects.filter(profile = obj)
        serializer = EfficiencySerializer(objs,many=True)
        return serializer.data

    def get_name(self,obj):
        first_name = obj.user.first_name
        last_name = obj.user.last_name
        return f"{first_name} {last_name}"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    sessions = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Attendance
        fields = ['sessions','profile','date','hours_assigned','hours_present','type',]

    def get_sessions(self,obj):
        objs = Timer.objects.filter(log_for = obj)
        serializer = TimerSerializer(objs,many=True)
        return serializer.data

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'