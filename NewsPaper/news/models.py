from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

NEWS = 'NW'
ARTICLE = 'AR'

CATEGORY_CHOICES = (
    (NEWS, 'Новость'),
    (ARTICLE, 'Статья'),
)


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):

        postR = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_R = 0
        p_R += postR.get('postRating') or 0

        commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_R = 0
        c_R += commentR.get('commentRating') or 0

        self.ratingAuthor = p_R * 3 + c_R
        self.save()

    def __str__(self):
        return str(self.authorUser)

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('NW', 'Новость'),
        ('AR', 'Статья'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='NW')
    dataCreations = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.postThrough} from the category: {self.categoryThrough}"


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    userPost = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Comment by {self.userPost} on {self.commentPost} at {self.dataCreation}"