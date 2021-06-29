from django.contrib import admin
from .models import Article, Category
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'jalali_publish', 'category_to_str', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-publish', '-status')

    def category_to_str(self, obj):
        return " , ".join(category.title for category in obj.category_published())
    category_to_str.short_description = "دسته بندی"


admin.site.register(Article, ArticleAdmin)
