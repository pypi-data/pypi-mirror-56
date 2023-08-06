from django.db import models
from django.utils import timezone


class Publisher(models.Model):
    name = models.CharField(max_length=255, default="Foo Bar")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=255, default="John")
    last_name = models.CharField(max_length=255, default="Doe")
    gender = models.CharField(
        max_length=255, default="active", choices=((u"female", u"female"), (u"1", u"male"))
    )

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
    avg_rating = models.DecimalField(default=4.55, decimal_places=2, max_digits=3)
    date_published = models.DateField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    stock = models.IntegerField(default=10)
    title = models.CharField(max_length=255, default="Lorem Ipsum")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("pk",)
