from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.conf import settings
import os
from django.urls import reverse
from .models import Post, Board, Reference, Board_Reply, Reference_Reply
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from .forms import ReferenceForm, UserForm, CustomSignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.decorators.http import require_POST
# from .models import Board

# Create your views here.
def index(request):
    # 게시판 데이터 조회
    board_data = Board.objects.all().order_by('-id')
    items_per_page_board = 10
    paginator_board = Paginator(board_data, items_per_page_board)
    page_board = request.GET.get('page_board', 1)
    try:
        board_page = paginator_board.page(page_board)
    except PageNotAnInteger:
        board_page = paginator_board.page(1)
    except EmptyPage:
        board_page = paginator_board.page(paginator_board.num_pages)

    # 공지사항 데이터 조회
    postlist = Post.objects.all().order_by('-id')
    items_per_page_post = 10
    paginator_post = Paginator(postlist, items_per_page_post)
    page_post = request.GET.get('page_post', 1)
    try:
        postlist_page = paginator_post.page(page_post)
    except PageNotAnInteger:
        postlist_page = paginator_post.page(1)
    except EmptyPage:
        postlist_page = paginator_post.page(paginator_post.num_pages)

    # 자료실 데이터 조회
    reference_data = Reference.objects.all().order_by('-id')
    items_per_page_reference = 10
    paginator_reference = Paginator(reference_data, items_per_page_reference)
    page_reference = request.GET.get('page_reference', 1)
    try:
        reference_page = paginator_reference.page(page_reference)
    except PageNotAnInteger:
        reference_page = paginator_reference.page(1)
    except EmptyPage:
        reference_page = paginator_reference.page(paginator_reference.num_pages)

    return render(
        request,
        'main/index.html',
        {'board_page': board_page, 'postlist_page': postlist_page, 'reference_page': reference_page}
    )
    
def download_file_view(request, post_id):
    # post_id를 사용하여 Reference 모델에서 해당 파일 정보를 가져온다.
    reference_data = get_object_or_404(Reference, id=post_id)

    # 파일 경로
    file_path = reference_data.file.path

    # 파일 이름
    file_name = reference_data.file.name.split("/")[-1]

    # 파일 오픈 및 HttpResponse로 전달
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


# 게시판 목록 조회
def board(request):
    board_data = Board.objects.all().order_by('-id')
    # print("서버와 디비 연결확인 :: ",board_data)

    # 페이지당 보여줄 게시물 수
    items_per_page = 10
    paginator = Paginator(board_data, items_per_page)

    # 요청된 페이지 번호 가져오기
    page = request.GET.get('page', 1)

    try:
        board_page = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 번째 페이지로 이동
        board_page = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어 있는 경우, 마지막 페이지로 이동
        board_page = paginator.page(paginator.num_pages)

    return render(request, 'main/board.html', {'board_page': board_page})

# 게시물 작성
def board_write(request):
    if request.method == 'POST':
        writer = request.user.username
        title = request.POST.get('title')
        content = request.POST.get('content')

        Board.objects.create(writer=writer, title=title, content=content) 
        # print(writer + title + content)

        board_data = Board.objects.all()

        return redirect('board')
    return render(request, 'main/bofard.html')

# 게시물 조회
def get_board_data(request):
    if request.method == 'GET':
        post_id = request.GET.get('postId')
        # 게시물 조회 로직을 여기에 추가
        try:
            Board.objects.filter(id=post_id).update(view_cnt=F('view_cnt') + 1)
            board_data = Board.objects.get(id=post_id)
            data = {
                 'title'   : board_data.title
                ,'writer'  : board_data.writer
                ,'content' : board_data.content
                ,'view_cnt': board_data.view_cnt
            }

            return JsonResponse(data)
        except Board.DoesNotExist:
            return JsonResponse({'error': '게시물이 존재하지 않습니다.'}, status=404)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

# 게시글 수정
def update_board(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        board = get_object_or_404(Board, id=post_id)
        board.title = request.POST.get('title')
        board.content = request.POST.get('content')
        board.writer = request.user.username
        board.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# 게시판 글삭제
@require_POST
def board_delete(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Board, id=post_id)
        post.delete()
        messages.success(request, '게시물이 성공적으로 삭제되었습니다.')
        return redirect('board')

    # POST 요청이 아니라면 삭제 전에 확인 메시지를 추가하고, 목록 페이지로 리디렉션
    messages.warning(request, '게시물을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')
    return redirect('board')

# 게시판 댓글 등록
def board_reply_write(request):
    if request.method == 'POST':
        writer = request.user.username
        content = request.POST.get('content')
        board_no = request.POST.get('search_board_id')

        Board_Reply.objects.create(writer=writer, content=content, board_no = board_no) 
        # print(writer + title + content)

        board_data = Board_Reply.objects.all()

        return redirect('board')
    return render(request, 'main/bofard.html')

# 댓글 조회
def get_comments(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    comments = Board_Reply.objects.filter(board_no=board_id).values('writer', 'content', 'regdate').all().order_by('-id')
    return JsonResponse({'comments': list(comments)})

def chk_login(request):
    is_logged_in = request.user.is_authenticated
    context = {
        'is_logged_in': is_logged_in  # 추가
    }
    return render(request, 'board.html', context)

# 자료실 글 목록 조회
def reference(request):
    reference_data = Reference.objects.all().order_by('-id')

    # 페이지당 보여줄 게시물 수
    items_per_page = 10
    paginator = Paginator(reference_data, items_per_page)

    # 요청된 페이지 번호 가져오기
    page = request.GET.get('page', 1)

    try:
        reference_page = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 번째 페이지로 이동
        reference_page = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어 있는 경우, 마지막 페이지로 이동
        reference_page = paginator.page(paginator.num_pages)

    return render(request, 'main/reference.html', {'reference_page': reference_page})

# 자료실 글 조회
def get_reference_data(request):
    if request.method == 'GET':
        post_id = request.GET.get('postId')
        # 게시물 조회 로직을 여기에 추가
        try:
            Reference.objects.filter(id=post_id).update(view_cnt=F('view_cnt') + 1)
            reference_data = Reference.objects.get(id=post_id)
            data = {
                'title'    : reference_data.title
                ,'writer'  : reference_data.writer
                ,'content' : reference_data.content
                ,'view_cnt': reference_data.view_cnt
            }

            return JsonResponse(data)
        except Reference.DoesNotExist:
            return JsonResponse({'error': '게시물이 존재하지 않습니다.'}, status=404)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

# 댓글 조회
def get_reference_comments(request, reference_id):
    reference = get_object_or_404(Reference, id=reference_id)
    comments = Reference_Reply.objects.filter(reference_no=reference_id).values('writer', 'content', 'regdate').all().order_by('-id')
    return JsonResponse({'comments': list(comments)})

# 자료실 댓글 등록
def reference_reply_write(request):
    if request.method == 'POST':
        writer = request.user.username
        content = request.POST.get('content')
        reference_no = request.POST.get('search_reference_id')

        Reference_Reply.objects.create(writer=writer, content=content, reference_no = reference_no) 
        # print(writer + title + content)

        reference_data = Reference_Reply.objects.all()

        return redirect('reference')
    return render(request, 'main/reference.html')


# 자료실 글쓰기
def reference_write(request):
    if request.method == 'POST':
        writer = request.user.username
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('file')  # 변경된 부분

        Reference.objects.create(writer=writer, title=title, content=content, file=file)
        print(writer, title, content, file)

        reference_data = Reference.objects.all()

        return redirect('reference')
    return render(request, 'main/reference.html')

# 첨부파일 다운로드
def download_reference_file(request, post_id):
    try:
        reference = Reference.objects.get(id=post_id)
        file_path = os.path.join(settings.MEDIA_ROOT, str(reference.file))
        
        # 파일이 존재하면 FileResponse를 사용하여 파일을 응답으로 반환
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = FileResponse(file)
                response['Content-Disposition'] = f'attachment; filename="{reference.file.name}"'
                return response
        else:
            return HttpResponse("File not found", status=404)
    except Reference.DoesNotExist:
        return HttpResponse("Reference not found", status=404)

# 자료실 글 수정
def update_reference(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        
        reference = get_object_or_404(Reference, id=post_id)
        reference.title = request.POST.get('title')
        reference.content = request.POST.get('content')
        reference.writer = request.user.username
        reference.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# 자료실 글삭제
def reference_delete(request, post_id):
    post = get_object_or_404(Reference, id=post_id)
    post.delete()
    return redirect('reference')

# 공지사항
def announcement(request):
    postlist = Post.objects.all().order_by('-id')
    
    # 페이지당 보여줄 게시물 수
    items_per_page = 10
    paginator = Paginator(postlist, items_per_page)

    # 요청된 페이지 번호 가져오기
    page = request.GET.get('page', 1)

    try:
        postlist_page = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 번째 페이지로 이동
        postlist_page = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어 있는 경우, 마지막 페이지로 이동
        postlist_page = paginator.page(paginator.num_pages)

    return render(request, 'main/announcement.html', {'postlist_page':postlist_page})

# 공지사항 조회
def get_announcement_data(request):
    if request.method == 'GET':
        post_id = request.GET.get('postId')
        # 게시물 조회 로직을 여기에 추가
        try:
            Post.objects.filter(id=post_id).update(view_cnt=F('view_cnt') + 1)
            board_data = Post.objects.get(id=post_id)
            data = {
                 'title'   : board_data.title
                ,'writer'  : board_data.writer
                ,'content' : board_data.content
                ,'view_cnt': board_data.view_cnt
            }

            return JsonResponse(data)
        except Post.DoesNotExist:
            return JsonResponse({'error': '게시물이 존재하지 않습니다.'}, status=404)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)


# 회원가입
def signUp(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 가입 성공 시 추가적인 처리
            return redirect('login')  # 로그인 페이지로 이동
    else:
        form = CustomSignUpForm()

    return render(request, 'main/signUp.html', {'form': form})

# 로그인 및 로그아웃
# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # 로그인이 성공하면 여기에 추가적인 로직을 넣습니다.
#         # return response
#         print("@@@@@@@@@@@")
#         return redirect(response.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
# 이미지 슬라이드
def img_slide(request):
        return render(request, 'main/img_slide.html', {})



