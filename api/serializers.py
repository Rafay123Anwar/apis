# serializers.py
from rest_framework import serializers
from .models import User, Patient
import base64

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'password']

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        """ Exclude password from the response """
        representation = super().to_representation(instance)
        representation.pop('password')  # Remove password from response
        return representation

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
    def get_image(self, obj):
        if obj.image:
            with open(obj.image.path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')  # Encode as Base64
        return None
