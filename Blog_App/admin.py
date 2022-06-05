from django.contrib import admin
from .models import Blog_Post, Blog_Comment, User_Profile, Contacts


# class Admin(admin.ModelAdmin):
#     def change_initial_user(self, request):
#         get_data = super(Admin, self).change_initial_user(request)
#         get_data['author'] = request.user.pk
#         return get_data
    


# Register your models here.
admin.site.register(Blog_Post)
admin.site.register(Blog_Comment)
admin.site.register(User_Profile)
admin.site.register(Contacts)