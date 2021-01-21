from django.urls import path

from .views import HomeView, about, contact, TagView, AuthorView, CategoryView, subscribe, post_detail


urlpatterns = [
    path('', HomeView.as_view(), name='home'),                                               # done
    path('about/', about, name='about'),                                                     # done
    path('contact/', contact, name='contact'),                                               # done
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),                   # done
    path('tag/<str:slug>/', TagView.as_view(), name='tag'),                                  # done
    path('post/<str:slug>/', post_detail, name='post'),                                      # done
    path('author/<str:name>/', AuthorView.as_view(), name='author'),                         # done
    path('subscribe/', subscribe, name='subscribe'),                                         # done
]
