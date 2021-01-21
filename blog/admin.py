from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.core.mail import send_mass_mail, send_mail

from .models import Category, Tag, Author, Subscriber, Post, Comment, Contact
from .forms import PostAdminForm
from django.conf import settings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', ('photo', 'get_photo'), 'about')
    list_display = ('name', 'get_photo')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="50">')

    get_photo.short_description = 'Rasmi'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)
    readonly_fields = ('subscribed_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    form = PostAdminForm
    # fieldsets = (
    #     ('Post sarlavhasi', {
    #         'fields': ('title', 'slug')
    #     }),
    #     ('Avtor, kategoriya va teglar', {
    #         'fields': (('author', 'category'), 'tags')
    #     }),
    #     ('Fon uchun foto va qisqa ko\'rinish', {
    #         'fields': (('face_photo', 'get_face_photo'), 'face_content')
    #     }),
    #     ('Asosiy Post', {
    #        'fields': ('content', )
    #     }),
    #     ('Yaratilgan va yangilangan vaqtlari', {
    #         'classes': ('collapse', ),
    #         'fields': ('created_at', 'updated_at')
    #     }),
    #     (None, {
    #         'fields': ('is_published', )
    #     }),
    # )
    actions = ('send_to_subscribers',)
    list_display = ('title', 'category', 'get_face_photo', 'author', 'created_at', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('created_at', 'category', 'author', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'get_face_photo')

    def send_to_subscribers(self, request, queryset):
        for obj in queryset:
            subscribers = []
            for subs in Subscriber.objects.values('email'):
                print(subs['email'])
                subscribers.append(subs['email'])
                print(subscribers)
            try:
                html_message = f"<h3>{obj.title}</h3><Bizga a'zo bolganiz uchun tashakkur>"
                mail = send_mail("Salom", f"{obj.face_content}", from_email=settings.EMAIL_HOST_USER,
                                 recipient_list=subscribers, fail_silently=False, html_message=html_message)
                self.message_user(request, "Post haqida xabar hamma subscriberlarga yuborildi", level=messages.SUCCESS)
            except Exception as e:
                print(e)
                self.message_user(request, f"Yuborishda xatolik\n{e}", level=messages.ERROR)

    send_to_subscribers.short_description = "Post haqida subscriberlarga jo'natish"

    def get_face_photo(self, obj):
        return mark_safe(f'<img src={obj.face_photo.url} width="50">')

    get_face_photo.short_description = 'fon'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'active')
    list_editable = ('active',)
    list_filter = ('created_at', 'active')
    search_fields = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('name', 'subject')
