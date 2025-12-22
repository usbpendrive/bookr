from django.db import models
from django.contrib import auth


class Publisher(models.Model):
    name = models.CharField(max_length=50, help_text="The name of the publisher")
    website = models.URLField(help_text="The website of the publisher")
    email = models.EmailField(help_text="The email of the publisher")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=70, help_text="The title of the book")
    publication_date = models.DateField(help_text="The publication date of the book")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(
        'Contributor', through='BookContributor')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    first_names = models.CharField(max_length=50, help_text="The contributor's first name or names")
    last_names = models.CharField(max_length=50, help_text="The contributor's last name or names")
    email = models.EmailField(help_text="The contributor's email")

    def __str__(self):
        return self.first_names


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this ccntributor had in the book.",
        choices=ContributionRole.choices, max_length=20)


class Review(models.Model):
    content = models.TextField(help_text="The review content")
    rating = models.IntegerField(help_text="The rating of the review")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was made")
    date_edited = models.DateTimeField(auto_now=True, help_text="The date and time the review was edited")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The book the review was made")
