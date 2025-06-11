from django.shortcuts import render, redirect
from .models import Item, FavoriteOutfit, DesignerPost, Like
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ItemForm, DesignerPostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('outfit_selector')
    else:
        form = UserCreationForm()
    return render(request, 'wardrobe/register.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = DesignerPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('designer_posts')
    else:
        form = DesignerPostForm()
    return render(request, 'wardrobe/create_post.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = DesignerPost.objects.get(id=post_id)
    if not Like.objects.filter(user=request.user, post=post).exists():
        Like.objects.create(user=request.user, post=post)
    return redirect('designer_posts')

@login_required
def comment_post(request, post_id):
    post = DesignerPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('designer_posts')

@login_required
def save_favorite(request):
    if request.method == 'POST':
        try:
            favorite = FavoriteOutfit.objects.create(
                user=request.user,
                accessory=Item.objects.get(id=request.POST['accessory_id']),
                top=Item.objects.get(id=request.POST['top_id']),
                bottom=Item.objects.get(id=request.POST['bottom_id']),
                shoes=Item.objects.get(id=request.POST['shoes_id']),
            )
            messages.success(request, '穿搭已成功收藏！')
        except Exception as e:
            messages.error(request, f'收藏失敗：{e}')
    return redirect('favorites')

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('outfit_selector')
    else:
        form = ItemForm()
    return render(request, 'wardrobe/add_item.html', {'form': form})

@login_required
def outfit_selector(request):
    items = Item.objects.filter(user=request.user)
    items_map = {
        'accessory': list(items.filter(category__iexact='accessory')),
        'top': list(items.filter(category__iexact='top')),
        'bottom': list(items.filter(category__iexact='bottom')),
        'shoes': list(items.filter(category__iexact='shoes')),
    }
    sections = [
        ('accessory', 'Accessory'),
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
    ]
    return render(request, 'wardrobe/outfit_selector.html', {
        'items_map': items_map,
        'sections': sections,
    })

@login_required
def manage_items(request):
    category = request.GET.get('category', 'top')  # 預設顯示 top
    items = Item.objects.filter(user=request.user, category=category)
    categories = [
        ('accessory', 'Accessory'),
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
    ]
    return render(request, 'wardrobe/manage_items.html', {
        'items': items,
        'categories': categories,
        'current_category': category,
    })




@login_required
def favorites(request):
    outfits = FavoriteOutfit.objects.filter(user=request.user)
    return render(request, 'wardrobe/favorites.html', {'outfits': outfits})

def designer_posts(request):
    posts = DesignerPost.objects.all().order_by('-created_at')
    return render(request, 'wardrobe/designer_posts.html', {'posts': posts})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    item.delete()
    return redirect('outfit_selector')

@login_required
def delete_favorite(request, favorite_id):
    outfit = get_object_or_404(FavoriteOutfit, id=favorite_id, user=request.user)
    outfit.delete()
    return redirect('favorites')
