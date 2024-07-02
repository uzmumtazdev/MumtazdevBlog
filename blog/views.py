from django.shortcuts import render, redirect
from .models import Post, Tag, Category, Rating, Comment
from django.core.paginator import Paginator
from .utils import check_view_articles

# Create your views here.
def home(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    last_comments = [post for post in Comment.objects.all()][:10]
    tops = Post.objects.filter(on_top=True)

    if request.method == 'GET':
        query = request.GET.get('query', '')
        if query != '':
            posts = Post.objects.filter(title__icontains=query)
    else:
        query = ''

    category_type = request.GET.get('category')
    if category_type is not None:
        if category_type == 'tops':
            posts = tops
        else:
            cat = Category.objects.get(name=category_type)
            posts = Post.objects.filter(category=cat)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = {'posts': page_obj,
            'categories': categories,
            'last_comments': last_comments,
            'query': query,
            'tops': tops
            }

    return render(request, 'blog/index.html', data)


def detail(request, pk):
    post = Post.objects.get(id=pk)
    categories = Category.objects.all()
    comments = Comment.objects.filter(post=post)
    category = Category.objects.get(id=post.category.id)
    relation_posts = Post.objects.filter(category=category).exclude(id__in=[0, post.id])
    ratings = Rating.objects.filter(post=post)

    request.session.modified = True
    if pk in check_view_articles(request):
        pass
    else:
        post.views += 1
        post.save()
        check_view_articles(request).append(pk)

    rating = request.GET.get('rating')
    if rating is not None:
        Rating.objects.create(post=post, value=rating)
        return redirect('/blog/'+str(pk)+'/')
    else:
        pass


    if request.method == 'POST':
        author = request.user
        comment = request.POST['comment']
        if comment:
            Comment.objects.create(author=author, comment=comment, post=post)
        return redirect('/blog/'+str(pk)+'/')



    if len([rating for rating in ratings]) != 0:
        rating = sum([rating.value for rating in ratings]) / len([rating for rating in ratings])
    else:
        rating = 0


    data = {'post': post, 'comments': comments, 'rating': rating, 'categories': categories, 'relation_posts': relation_posts}

    return render(request, 'blog/detail.html', data)

