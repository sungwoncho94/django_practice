from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)


def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    # 해당 아티클의 댓글만 가져와야함
    comments = Comment.objects.all()
    # comment = Comment.objects.all() -> 모~든 댓글을 다가지고옴
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


# POST or GET 으로 들어올 것!
def create(request):
    # post로 들어온다 == 내용을 담아서 올려달라고 부탁하는 것
    if request.method == 'POST':
        # POST로 들어온 요청을 ArticleForm에 담아서 form이라는 변수로 넘긴다
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 올바른 form이면 article에 저장!하고 바로 detail page 불러온다
            article = form.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'articles/create.html', context)

# POST or GET 으로 나눠서 실제 수정을 해주던가, 수정하는 form을 보여주던가
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'POST':
        # 수정할거니까 원래 있던 정보도 함께 넘겨주기
        form = ArticleForm(request.POST, instance=article)
        ## 주의! valid한 form이 들어왔으면 저장한다음 redirect해준다
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)

    # GET요청 -> 기존 article을 form에 담아서 준다
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form
    }
    return render(request, 'articles/update.html', context)


def delete(request, article_pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
    return redirect('articles:index')


def comments_create(request, article_pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # form에서 어떤 게시글에 대한 댓글인지 article_pk도 꺼내줘야한다.
            comment = form.save(commit=False)
            comment.article_id = article_pk
            comment.save()
    return redirect('articles:detail', article_pk)
            

def comments_delete(request, article_pk, comment_pk):
    if request.method == "POST":
        # Comment 에서 comment_pk인 값을 commet에 넣는다
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        # article_pk인 detail 페이지를 보여줘야함
        return redirect('articles:detail', article_pk)

