from django.contrib import admin
from books import models

# Register your models here.

#from books import models#从app(应用)中导入
#admin.site.register(models.表名)#创建的表注册到admin中
class Useradmin(admin.ModelAdmin):
    list_display=('id','name','sex','age','signature','friends_list')
    list_editable=('name','age')
class WebGroupadmin(admin.ModelAdmin):
    list_display=('id','name')
    list_editable=('name',)   
# admin.site.register(models.User,Useradmin)#注册表到admin
admin.site.register(models.WebGroup,WebGroupadmin)
admin.site.register(models.User,Useradmin)