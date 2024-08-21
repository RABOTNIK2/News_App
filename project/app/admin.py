from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import *
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

class PersonAdmin(UserAdmin):
    form = PersonChangeForm
    add_form = PersonCreationForm

    list_display = ('email', 'name', 'age', 'is_staff', 'is_superuser')
    list_filter = ('is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('name', 'age', 'image')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'age', 'image')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, PersonAdmin)

admin.site.register(Category)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'news_text', 'category', 'get_news_image']
    search_fields = ('title', 'category')
    fields = ['title', 'news_text', 'category', 'news_posted_at', 'news_image','get_news_image']
    readonly_fields = ['get_news_image', 'news_posted_at']

    def get_news_image(self, obj):
        if obj.news_image:
            return mark_safe(f'<img src="{obj.news_image.url}" width="100">')
        
    get_news_image.short_description = 'Загруженное фото'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment_text', 'comment_to_news', 'get_author_image']


    def get_author_image(self, obj):
        if obj.author.image.url:
            return mark_safe(f'<img src="{obj.author.image.url}" width="100">')
        
    get_author_image.short_description = 'Фото автора'


admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    search_fields = ('name', 'domain')
admin.site.register(Site, SiteAdmin)

# Register your models here.
