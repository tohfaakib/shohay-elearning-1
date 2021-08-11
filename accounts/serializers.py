from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UpdateProfileSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=False)
    # username = serializers.CharField(required=True)

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'phone', 'current_institute', 'preferred_higher_education')

    def validate_username(self, value):
        user = self.context['request'].user
        if Account.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        # print(validated_data)
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        # instance.email = validated_data['email']
        instance.username = validated_data['username']
        if 'phone' in validated_data:
            if validated_data['phone'] != '':
                instance.phone = validated_data['phone']
        if 'current_institute' in validated_data:
            if validated_data['current_institute'] != '':
                instance.current_institute = validated_data['current_institute']
        if 'preferred_higher_education' in validated_data:
            if validated_data['preferred_higher_education'] != '':
                instance.preferred_higher_education = validated_data['preferred_higher_education']

        instance.save()

        return instance


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('uuid', 'email', 'username', 'first_name')
