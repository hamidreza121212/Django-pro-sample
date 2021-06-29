from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Article, Category

# Create your views here.


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 3


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status='y')
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 2)
#     articles = paginator.get_page(page)
#     context = {
#         "category": category,
#         "articles": articles
#     }
#     return render(request, 'blog/category_list.html', context)
class CategoryList(ListView):
    paginate_by = 2
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context




