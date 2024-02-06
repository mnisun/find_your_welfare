"""
URL configuration for proj01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import myapp.views
from myapp.views import board_delete, reference_delete
from django.contrib.auth.views import LoginView, LogoutView, LoginView
from myapp.views import download_reference_file, download_file_view

urlpatterns = [
     path('admin/', admin.site.urls)
    ,path('', myapp.views.index, name='index')

    #게시판 관련
    ,path('board/', myapp.views.board, name='board')
    ,path('board_write/', myapp.views.board_write, name='board_write')
    ,path('board_delete/<int:post_id>/', myapp.views.board_delete, name='board_delete')
    ,path('get_board_data/', myapp.views.get_board_data, name='get_board_data')
    ,path('update_board/', myapp.views.update_board, name='update_board')
    ,path('board_reply_write/', myapp.views.board_reply_write, name='board_reply_write')
    ,path('get_comments/<int:board_id>/', myapp.views.get_comments, name='get_comments')

    #공지사항 관련
    ,path('announcement/', myapp.views.announcement, name='announcement')
    ,path('get_announcement_data/', myapp.views.get_announcement_data, name='get_announcement_data')    

    #자료실 관련
    ,path('reference/', myapp.views.reference, name='reference')
    ,path('reference_write/', myapp.views.reference_write, name='reference_write')
    ,path('get_reference_data/', myapp.views.get_reference_data, name='get_reference_data')
    ,path('reference_delete/<int:post_id>/', myapp.views.reference_delete, name='reference_delete')
    ,path('update_reference/', myapp.views.update_reference, name='update_reference')
    ,path('download_reference_file/<int:post_id>/', myapp.views.download_reference_file, name='download_reference_file')
    ,path('download/<int:post_id>/', myapp.views.download_file_view, name='download_file')
    ,path('reference_reply_write/', myapp.views.reference_reply_write, name='reference_reply_write')
    ,path('get_reference_comments/<int:reference_id>/', myapp.views.get_reference_comments, name='get_reference_comments')

    #회원가입
    ,path('signUp/', myapp.views.signUp, name='signUp')

    # 로그인 및 로그아웃
    ,path('login/', LoginView.as_view(), name='login')
    ,path('logout/', LogoutView.as_view(), name='logout')

    # 이미지 슬라이드
    ,path('img_slide/', myapp.views.img_slide, name='img_slide')
]

# 파일업로드 관련
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



