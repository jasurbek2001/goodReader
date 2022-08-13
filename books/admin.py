from django.contrib import admin

# Register your models here.

from .models import Book, Author, BookAuthor, BookRewiev

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title','isbn')
    list_display = ('title','isbn','description')

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookAuthorAdmin(admin.ModelAdmin):
    pass

class BookReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookRewiev, BookReviewAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
