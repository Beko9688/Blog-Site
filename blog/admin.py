from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Tag, Post, Comment
from django.utils.safestring import mark_safe


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'author', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'author', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'category', 'tags', 'author', 'content', 'photo', 'get_photo', 'views', 'created_at',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')
        else:
            return '-'

    get_photo.short_description = 'картинка'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'post', 'created', 'moderation')
    list_filter = ('moderation',)
    readonly_fields = ('created',)
    search_fields = ('name', 'email', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(moderation=True)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
