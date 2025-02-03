from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers

from customuser.models import User, ProfileUser, UserImage, NewProduct

# class UserSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     is_active = serializers.BooleanField(required=True)
#     is_staff = serializers.BooleanField(required=True)
class UserRegisterSerializer(serializers.Serializer):
    """Серилизатор для проверки пользователя"""
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        user_email = data.get('email').lower()
        if password1 != password2:
            raise serializers.ValidationError({'password1': 'пароли не совпадают'})
        if User.objects.filter(email=user_email).exists():
            raise serializers.ValidationError({'email': 'пользователь с такой почтой уже существует'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        validated_data.pop('password1')
        #validated_data["password"] = password
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        profile = ProfileUser(user=user)
        profile.save()
        image = UserImage(image='no_photo/no_photo.jpg', is_main=True, user_profile=profile)
        image.save()
        return user

    # def update(self, instance, validated_data):
    #     validated_data.pop('password2', None)
    #     password = validated_data.pop('password1', None)
    #     instance.email = validated_data.get('email', instance.email)
    #
    #     if password:
    #         instance.set_password(password)
    #
    #     instance.save()
    #     return instance

class UserLoginSerializer(serializers.Serializer):
    """Серилизатор для проверки правильного входа в профиль пользователя"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'))
            if not user:
                raise serializers.ValidationError("Неверный email или пароль.")
        else:
            raise serializers.ValidationError("Необходимо указать email и пароль.")

        data['user'] = user
        return data


class ProfileUserSerializer(serializers.Serializer):
    """Серилизатор для профиля пользователя"""
    first_name = serializers.CharField(max_length=500, required=False)
    date_birth = serializers.DateField(required=False)
    info_about_user = serializers.CharField(max_length=500, required=False)
    user = UserLoginSerializer()

    def validate_birth_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Дата рождения не может быть в будущем.")
        return value

    def create(self, validated_data):
        return ProfileUser.objects.create(**validated_data)

    # def update(self, validate_data):
    #
    #     return ProfileUser.objects.update(**validate_data)

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = User.objects.create(**user_data)
    #     profile_user = ProfileUser.objects.create(user=user, **validated_data)
    #     return profile_user
    #
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.email = user_data.get('email', user.email)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.date_birth = validated_data.get('date_birth', instance.date_birth)
        instance.info_about_user = validated_data.get('info_about_user', instance.info_about_user)
        instance.save()
        return instance


class NewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewProduct
        fields = ['name', 'price']









