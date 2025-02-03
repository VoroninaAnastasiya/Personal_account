from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import serializers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from customuser.models import ProfileUser, UserImage, NewProduct
from .serializers import UserRegisterSerializer, NewProductSerializer, UserLoginSerializer, ProfileUserSerializer


@api_view(['POST'])
# @permission_classes([AllowAny])
def register_new_user(request):
    print('--------------------')
    print(request.data)
    if request.method == 'POST':
        print('+++++++++++++++')
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # profile = ProfileUser(user=user)
            # profile.save()
            # image = UserImage(image='no_photo/no_photo.jpg', is_main=True, user_profile=profile)
            # image.save()
            return Response({'message': 'User created', 'your_id': user.pk})
        # x = Response(serializer.errors, status=400)
        # print(x)
        # print(x.__dict__)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password =  request.data.get('password')
    user = authenticate(username=email, password=password)
    if user and user.is_active:
        token = RefreshToken.for_user(user=user)
        data = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data)
    return Response({'message': 'пользователь не авторизован! введите верные данные'})

    # elif request.method == 'PUT':
    #     try:
    #         user = User.objects.get(email=request.data['email'])
    #     except User.DoesNotExist:
    #         return Response({'error': 'User not found'}, status=404)
    #
    #     serializer = UserRegisterSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         return Response({'message': 'User updated', 'your id': user.pk})
    #     return Response(serializer.errors, status=400)
    #
    # return Response({'message': "You are on Register endpoint"})
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        profile = ProfileUser.objects.get(user=request.user)
    except ProfileUser.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=404)

    if request.method == 'GET':
        serializer = ProfileUserSerializer(profile)
        print(serializer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileUserSerializer(profile, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=400)
        else:
            return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     serializer = UserLoginSerializer(data=request.data)
#     try:
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         refresh = RefreshToken.for_user(user)
#         tokens = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#         return Response(tokens)
#     except serializers.ValidationError as e:
#         return Response({'errors': e.detail}, status=400)
@api_view(['GET','POST'])
def register_new_product(request):
    print(request.data)

    if request.method == 'POST':
        print(request.data, '+++++++++++++++++++++')
        # print(type(request.data))
    #     serializer = NewProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         new_product = serializer.save()
    #         return Response({'message':'new product created', 'product': new_product.pk})
    #
    # if request.method == 'GET':
    #
    #     serializer = NewProductSerializer(products, many=True)
    # obj = NewProduct(name='Johan', price=10.10)
    # print(obj)
    # print(type(obj.price))
    # print(obj.__dict__)
    x = {'message':'new product created'}
    products = NewProduct.objects.get(pk=2)
    s = NewProductSerializer(products)

    # print(type(x))
    r = Response(s.data)
    # print(r.__dict__)
    # print(type(r.data),'--------------------------')
    return r

# def validate_name(value):
#     if isinstance(value, str):
#         if len(value) > 10:
#             raise ValidationError("Имя слишком длинное")
#     else:
#         raise ValidationError("Имя не должно содержать цифры, только буквы")
# def validate_description(value):
#     if len(value) > 10:
#         raise ValidationError("Описание слишком длинное")
#
# VALID_IMAGE_EXTENSIONS = [
#     ".jpg",
#     ".jpeg",
#     ".png",
#     ".gif",
# ]
# def validate_image(value):
#     naming, ext = value.split(".")
#     print(naming)
#     print(ext)
#     if ext not in VALID_IMAGE_EXTENSIONS:
#         raise ValidationError('Не валидный формат файла')
#
#
# def validate_user(value):
#     try:
#         User.objects.get(id=value)
#     except ObjectDoesNotExist:
#         raise ValidationError("Пользователь не существует!")

# try:
#     validate_email('invalid email')
# except ValidationError as e:
#     print(f"Ошибка валидации: {e}")
