from django.contrib import admin
from Core.models import News, NewsParagraph, NewsParagraphImage

class NewsParagraphInline(admin.TabularInline):
    model = NewsParagraph
    extra = 0


class NewsParagraphImageInline(admin.TabularInline):
    model = NewsParagraphImage
    extra = 0


@admin.register(NewsParagraph)
class NewsParagraphAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'title')
    inlines = [NewsParagraphImageInline]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'created_at', 'updated_at', 'author', 'title')
    inlines = [NewsParagraphInline]