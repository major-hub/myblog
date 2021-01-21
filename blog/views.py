from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db.models import Count, F
from django.core.cache import cache
from django.contrib import messages

from .models import Contact, Post, Subscriber, Comment


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        posts = cache.get('posts')
        if not posts:
            posts = Post.objects.filter(is_published=True).annotate(
                cnt=Count('comments')).select_related('category').order_by('-updated_at')
            cache.set('posts', posts, (2 * 60))
        return posts


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category_and_tag.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(is_published=True, category__slug=self.kwargs['slug']).annotate(
            cnt=Count('comments')).select_related('author').order_by('-updated_at')


class TagView(ListView):
    model = Post
    template_name = 'blog/category_and_tag.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(is_published=True, tags__slug=self.kwargs['slug']).annotate(
            cnt=Count('comments')).select_related('author').order_by('-updated_at')


def post_detail(request, slug):

    post = Post.objects.get(slug=slug)
    comments_cnt = post.comments.count()

    if request.method == "POST":
        print(request.POST)
        if request.POST['ism'].isalpha():
            Comment.objects.create(post=post, name=request.POST['ism'], body=request.POST['body'])
            return redirect(f'{post.get_absolute_url()}#comment')
    else:
        post.views = F('views') + 1
        post.save(update_fields=('views',))
        # update_fields=() qaysi elementlarni update qilsak oshalarni ozini yozishimiz mumkin
        post.refresh_from_db()  # bizga shart emas bazani yangilash sababi postda view ni kormimiz
    context = {'post': post, 'comments_cnt': comments_cnt}
    return render(request, 'blog/post.html', context)


class AuthorView(ListView):
    model = Post
    template_name = 'blog/author.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True, author__name=self.kwargs['name']).annotate(
            cnt=Count('comments')).select_related('category', 'author').order_by('-updated_at')


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    if request.method == "POST":
        try:
            Contact.objects.create(name=request.POST['name'], email=request.POST['email'],
                                   subject=request.POST['subject'],
                                   body=request.POST['body'])
            messages.success(request, 'Muvofaqqiyatli yuborildi')
        except Exception as e:
            print(e)
            messages.error(request, 'Yuborishda xatolik! iltimos, qayta urinib ko\'ring')
    return render(request, 'blog/contact.html')


def subscribe(request):
    if request.method == "POST":
        if '@' in request.POST['email']:
            try:
                subs, _ = Subscriber.objects.get_or_create(email=request.POST['email'])
                if _:
                    messages.success(request, "Obuna bo'lish muvofaqqiyatli amalga oshirildi")
                    html_message = f"<h3>Siz bizning Blogimizga obuna bo'ldingiz</h3>" \
                                   f"<p>Bizga a'zo bolganiz uchun tashakkur</p>" \
                                   f"<a href='https://major-blog.herokuapp.com'>Our Blog</a>"
                    mail = send_mail("Assalomu alaykum", "", from_email=settings.EMAIL_HOST_USER,
                                     recipient_list=[request.POST['email']], fail_silently=False,
                                     html_message=html_message)
                else:
                    messages.info(request, "Siz avval obuna bo'lgansiz")
            except Exception as e:
                print(e)
                messages.error(request, 'Yuborishda xatolik! iltimos, qayta urinib ko\'ring')
        else:
            messages.error(request, "Iltimos, Emailingizni to'g'ri kiriting")
    return redirect('home')
