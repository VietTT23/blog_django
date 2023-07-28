from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    # context_object_name = 'post_list'     # mac dinh khi khong set thuoc tinh thi se la ten model + _list
    paginate_by = 3


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}

    return render(request, template_name, context)


def post_list(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 1)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        num_post_listt = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        num_post_listt = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        num_post_listt = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'page': page, 'post_list': num_post_listt})
