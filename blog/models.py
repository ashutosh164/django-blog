from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image',null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('detail',kwargs={'pk': self.pk})
        return reverse('index')

    # def save(self, *args, **kwargs):
    #     super().save( *args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile')
    bio = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} "

    # RESIZE THE IMAGE
    # def save(self,*args,**kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
