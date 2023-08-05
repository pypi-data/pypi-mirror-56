from django.db import models


class Book(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title


class Page(models.Model):
    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"Page {self.number} for {self.book.title}"

    class Meta:
        ordering = ["number"]


class PageImage(models.Model):
    page: Page = models.ForeignKey(Page, on_delete=models.CASCADE)
    image = models.ImageField()
