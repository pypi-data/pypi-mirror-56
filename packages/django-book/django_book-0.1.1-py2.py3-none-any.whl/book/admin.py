from django.contrib import admin
from .models import Book, Page, PageImage


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(PageImage)
class PageImageAdmin(admin.ModelAdmin):
    pass
