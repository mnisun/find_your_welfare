from django.contrib import admin
from .models import Post
# Register your models here.

# 관리자(admin)가 게시판에 접근 가능
admin.site.register(Post)

