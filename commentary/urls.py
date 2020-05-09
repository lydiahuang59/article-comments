from . import views
from django.urls import path

app_name = 'commentary'
urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'),
    path('<int:article_id>/', views.detail, name='article_detail'),
    path('upvote/', views.upvote, name='comment_upvote'),
]