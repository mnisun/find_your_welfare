from django.db import models
from django.utils import timezone


# Create your models here.
# 공지사항에 들어가는 컬럼을 넣는다.
class Post(models.Model):
    # no = models.AutoField(primary_key=True, default=1)
    writer   = models.CharField(max_length=10, null=True)
    title    = models.CharField(max_length=50)
    content  = models.TextField()
    regdate  = models.DateTimeField(default=timezone.now)
    view_cnt = models.IntegerField(default=0)

    # 게시글의 제목(title)이 Post object 대신하기
    def __str__(self):
        return self.title
    
    @property
    def update_counter(self):
        self.view_cnt += 1
        self.save()

#게시판에 들어가는 컬럼 추가
class Board(models.Model):
    # 필요한 필드를 추가합니다.
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    writer   = models.CharField(max_length=50, null=True)
    regdate  = models.DateTimeField(default=timezone.now)
    view_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    @property
    def update_counter(self):
        self.view_cnt += 1
        self.save()

#자료실에 들어가는 컬럼 추가
class Reference(models.Model):
    title    = models.CharField(max_length=100)
    content  = models.TextField()
    writer   = models.CharField(max_length=50)
    regdate  = models.DateTimeField(default = timezone.now)
    file     = models.FileField(upload_to='reference_files/')
    view_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    @property
    def update_counter(self):
        self.view_cnt += 1
        self.save()

#게시판 댓글 컬럼
class Board_Reply(models.Model):
    content = models.TextField()
    writer  = models.CharField(max_length=50)
    regdate = models.DateTimeField(default = timezone.now)
    board_no = models.IntegerField(default=0)

    def __str__(self):
        return self.content
    
#자료실 댓글 컬럼
class Reference_Reply(models.Model):
    content  = models.TextField()
    writer   = models.CharField(max_length=50)
    regdate  = models.DateTimeField(default = timezone.now)
    reference_no = models.IntegerField(default=0)

    def __str__(self):
        return self.content
