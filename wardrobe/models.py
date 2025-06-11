from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('top', '上衣'),
        ('bottom', '下身'),
        ('shoes', '鞋子'),
        ('accessory', '飾品'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class FavoriteOutfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='top_outfits')
    bottom = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bottom_outfits')
    shoes = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='shoes_outfits')
    accessory = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='accessory_outfits')
    created_at = models.DateTimeField(auto_now_add=True)

class DesignerPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='designer_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(DesignerPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(DesignerPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


