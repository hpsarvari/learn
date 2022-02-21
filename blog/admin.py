from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Article, Category


# Register your models here.
# admin.site.disable_action('delete_selected')
@admin.action(description='انتشار مقالات انتخاب شده')
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d مقاله منتشر شد',
        '%d تا از مقاله ها منتشر شدند',
        updated,
    ) % updated, messages.SUCCESS)


@admin.action(description='پیش نویس مقالات انتخاب شده')
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d مقاله پیش نویس شد',
        '%d تا از مقاله ها پیش نویس شدند',
        updated,
    ) % updated, messages.SUCCESS)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', 'publish']
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        return '، '.join([category.title for category in obj.category_published()])

    category_to_str.short_description = 'دسته بندی'


admin.site.register(Article, ArticleAdmin)