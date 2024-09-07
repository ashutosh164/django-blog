from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    shared_title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='image', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    class Meta:
        ordering = ['-date_created', '-shared_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('detail',kwargs={'pk': self.pk})
        return reverse('index')

    @property
    def num_like(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comments.all().count()

    # RESIZE THE IMAGE

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Profile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile')
    bio = models.CharField(max_length=200,null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    qul = models.CharField(max_length=200, blank=True)
    mob = models.CharField(max_length=10, blank=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='post')
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f"{self.user.username} "

    def profile_post(self):
        # return self.post_set.all()  # reverse relationship fetch the post data we can return by calling related name
        return self.post
    @property
    def follower_count(self):
        return self.following.all().count()

    # class Meta:
    #     ordering = ('-created',)

    # RESIZE THE IMAGE
    def save(self,*args,**kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return f'{self.user}--{self.post}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}--{self.post}--{self.body}'
