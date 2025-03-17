from django.contrib import admin
from userauths.models import Profile, User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email','phone']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'country']
    # list_editable = ["gender", "country"]
    # list_filter = ["gender", "country"]
    search_fields = ["full_name"    ]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
