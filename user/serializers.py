from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User 
        fields = [
            'id',
            'username',
            'name',
            'email',
            'phone',
            'birth_date',
            'marital_status',
            'gender',
            'password',
            'followers',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'marital_status',
            'gender',
            'followers'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user