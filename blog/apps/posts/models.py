import uuid
from django.db import models
from apps.category.models import Category
from django.core.validators import MaxValueValidator,MinValueValidator

def blog_directory_path(instance, filename):
    return 'blogs/{0}/{1}'.format(instance.title, filename)


class Author(models.Model):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    picture = models.ImageField(default='media/users/user_default_profile.png',  upload_to='media/users/pictures/', blank=True, null=True, verbose_name='Picture')

    def __str__(self):
        return self.username
    

class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    id =                            models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title =                         models.CharField(max_length=200)
    short_description =             models.TextField(max_length=125, blank=True, null=True)
    thumbnail =                     models.ImageField(upload_to=blog_directory_path, blank=True, null=True) 

    content =                       models.TextField()

    created_at =                    models.DateTimeField(auto_now_add=True)
    updated_at =                    models.DateTimeField(auto_now=True)
    author =                        models.ForeignKey(Author, on_delete=models.CASCADE)

    keywords =                      models.CharField(max_length=255, blank=True, null=True)
    slug =                          models.SlugField(unique=True, default=uuid.uuid4)

    rating =                        models.ManyToManyField('Rate',blank=True, related_name='courseRating')
    rating_number =                 models.IntegerField(default=0, blank=True, null=True)

    language =                      models.CharField(max_length=50, blank=True, null=True)
    level =                         models.CharField(max_length=50, blank=True, null=True)

    # Analytics
    views =                         models.IntegerField(default=0, blank=True)
    clicks =                        models.IntegerField(default=0, blank=True, null=True)
    impressions =                   models.IntegerField(default=0, blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='posts_category',
    )
    sub_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='sub_category_posts',
    )
    topic = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='topic_posts',
    )

    status =                        models.CharField(max_length=10, choices=options, default='draft')

    objects =                       models.Manager()  # default manager
    postobjects =                   PostObjects()  # custom manager

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title

    def get_rating(self):
        ratings=self.rating.all()
        rate=0
        for rating in ratings:
            rate+=rating.rate_number
        try:
            rate/=len(ratings)
        except ZeroDivisionError:
            rate=0
        return rate

    def get_no_rating(self):
        return len(self.rating.all())
    
    def get_category_name(self):
        if(self.category):
            name = self.category.name
            return name
        else:
            return
    

class ViewCount(models.Model):
    post =                      models.ForeignKey(Post, related_name='post_view_count', on_delete=models.CASCADE)
    ip_address =                models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"
    

class Rate(models.Model):
    rate_number =               models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    user =                      models.UUIDField(blank=True, null=True)
    post =                      models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rate_belongs_to_post', blank=True, null=True)
