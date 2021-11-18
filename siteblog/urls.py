import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from blog.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('get_post/<slug:slug>/', post_detail, name='single'),
    path('tag/<str:slug>/', PostByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('like/<int:pk>', LikeView, name='like_comment'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
