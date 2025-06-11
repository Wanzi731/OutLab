from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.outfit_selector, name='outfit_selector'),
    path('add_item/', views.add_item, name='add_item'),
    path('favorites/', views.favorites, name='favorites'),
    path('designer/', views.designer_posts, name='designer_posts'),
    path('save_favorite/', views.save_favorite, name='save_favorite'),
    path('manage_items/', views.manage_items, name='manage_items'),

]

urlpatterns += [
    path('designer/create/', views.create_post, name='create_post'),
    path('designer/<int:post_id>/like/', views.like_post, name='like_post'),
    path('designer/<int:post_id>/comment/', views.comment_post, name='comment_post'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='wardrobe/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]

urlpatterns += [
    # ... 既有的路由 ...
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('favorite/delete/<int:favorite_id>/', views.delete_favorite, name='delete_favorite'),
]