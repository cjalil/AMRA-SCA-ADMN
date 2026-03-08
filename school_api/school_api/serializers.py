from rest_framework import serializers
from .models import Student, PickupRequest

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class PickupRequestSerializer(serializers.ModelSerializer):
    # باش نرجعو سمية التلميذ ماشي غير الـ ID ديالو
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    class_name = serializers.CharField(source='student.class_name', read_only=True)

    class Meta:
        model = PickupRequest
        fields = ['id', 'student', 'student_name', 'student_last_name', 'class_name', 'created_at', 'is_completed']