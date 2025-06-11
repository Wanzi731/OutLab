from django import forms
from .models import Item
from .models import DesignerPost, Comment

class DesignerPostForm(forms.ModelForm):
    class Meta:
        model = DesignerPost
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full border p-2 rounded',
                'placeholder': 'Write your post here...',
                'rows': 4
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full border p-2 rounded'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'brand', 'size', 'image']
        widgets = {
            'category': forms.Select(choices=Item.CATEGORY_CHOICES),
        }
