from . import views
from django.urls import path

app_name = 'commentary'
urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'),
    path('<int:article_id>/', views.detail, name='article_detail'),
    path('<int:article_id>/upvote/<int:comment_id>/', views.upvote, name='comment_upvote'),
    path('<int:article_id>/downvote/<int:comment_id>/', views.downvote, name='comment_downvote')
]