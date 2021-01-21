from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField('kategoriya nomi', max_length=50)
    slug = models.SlugField(verbose_name='url', max_length=60, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Tag(models.Model):
    title = models.CharField('tag nomi', max_length=50)
    slug = models.SlugField(verbose_name='url', max_length=60, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Taglar'


class Author(models.Model):
    name = models.CharField('avtor ismi', max_length=70, help_text="to'liq ism familyangizni kiriting", unique=True)
    photo = models.ImageField(upload_to='authors/', verbose_name='avtor rasmi')
    about = models.TextField("o'zingiz haqingizda qisqacha")

    def get_absolute_url(self):
        return reverse('author', kwargs={'name': self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Avtor'
        verbose_name_plural = 'Avtorlar'


class Subscriber(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField('azo bolgan vaqti', auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Obunachi'
        verbose_name_plural = 'Obunachilar'


class Post(models.Model):
    title = models.CharField('post nomi', max_length=100)
    slug = models.SlugField(verbose_name='url', max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='kategoriyasi',
                                 related_name='posts')
    tags = models.ManyToManyField(Tag, verbose_name='taglari', related_name='posts')
    face_photo = models.ImageField(upload_to='post_faces/%Y/%m/%d/', verbose_name='fon uchun rasm')
    face_content = models.TextField('postning yuzi', help_text='qisqacha, oziga tortadigan bo\'lsin')
    content = models.TextField('asosiy postingizni korinishi')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='yaratilgan vaqti')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='yangilangan vaqti')
    is_published = models.BooleanField('chop etilganmi', default=True)
    views = models.PositiveIntegerField("Ko'rilgan", default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['updated_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Postlar'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField('ismi', max_length=70)
    body = models.TextField('yozgan commenti')
    created_at = models.DateTimeField('comment yozgan vaqti', auto_now_add=True)
    active = models.BooleanField('comment activmi', default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Komment'
        verbose_name_plural = 'Kommentlar'


class Contact(models.Model):
    name = models.CharField('ismi', max_length=70)
    email = models.EmailField()
    subject = models.CharField('xabar mavzusi', max_length=70)
    body = models.TextField('xabar mazmuni')
    sent_at = models.DateTimeField('xabar jo\'natgan vaqti', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kontakt'
        verbose_name_plural = 'Kontaklar'
