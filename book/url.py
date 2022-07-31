from django.urls import URLPattern, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.index , name="home"),
    path('recommendations', views.recommend , name="recommendations"),
    path('books/<str:name>', views.bookInfo , name="book_info")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
