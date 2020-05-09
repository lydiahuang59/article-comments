from django.views import generic
from .models import Article, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

logger = logging.getLogger("django")

class ArticleList(generic.ListView):
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'article_list'
    template_name = 'index.html'

class ArticleDetail(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'

# helper function that returns a request for the article detail page
def reload_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.filter(status=1,parent__isnull=True)
    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': CommentForm(auto_id=False)
    })

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.filter(status=1,parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            new_comment = comment_form.save(commit=False)
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    # assign parent_obj to comment
                    new_comment.parent = parent_obj
            # assign article/author to the comment
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('commentary:article_detail', args=(article.id,)))
    return reload_article(request, article_id)

@login_required
@require_POST
def upvote(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id', None)
        comment = get_object_or_404(Comment, pk=comment_id)
        logger.info("comment " + str(comment_id) + " has score " + str(comment.score))
        if comment.votes.up(request.user.id):
            comment.score += 1
            comment.save()
            logger.info("increased " + str(comment_id) + " by 1, score is now " + str(comment.score))
    result = {'likes': comment.score}
    return HttpResponse(json.dumps(result), content_type='application/json')
        


