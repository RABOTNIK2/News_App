from django.urls import path
from . import views

urlpatterns = [
    path('main/delete/<int:pk>/<int:del_comment>', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('main/<int:pk>/<int:comment>', views.CommentUpdateView.as_view(), name='comment_change'),
    path('main/<int:pk>', views.NewsDetailView.as_view(), name='detail_news'),
    path('main/', views.NewsListView.as_view(), name='main'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('account_sent/', views.Account_activation_sent.as_view(), name='account_sent'),
    path('activate/<uidb64>/<token>/', views.Activate.as_view(), name='activate'),
    path('account_complete/', views.Account_activation_complete.as_view(), name='account_complete'),
    path('profile/update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    path('profile/password_change/<int:pk>/', views.UserChangePassword.as_view(), name='password_change'),
    path('profile/password_change_done/<int:pk>', views.UserChangePasswordDone.as_view(), name='password_change_done'),
    path('profile/image/<int:pk>/', views.ImageUpdateView.as_view(), name='image'),
    path('profile/logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='profile'),

]