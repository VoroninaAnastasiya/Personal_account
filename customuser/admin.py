from django.contrib import admin

from customuser.models import User, ProfileUser, UserImage

# Register your models here.
admin.site.register(User)
admin.site.register(ProfileUser)
admin.site.register(UserImage)