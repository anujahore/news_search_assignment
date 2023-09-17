

from django.urls import path
from app1 import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_page, name='login'),
    path('admin-page/', views.admin_view, name='admin'),
    path('logout/', views.logout_page, name='logout'),
    path('admin-page/all-users/', views.get_all_users , name='all_users'),
    path('admin-page/all-users/edit-user/<int:id>/', views.user_edit , name='user_edit'),
    path('home/filter/', views.filter_results, name='filter_results'),
    
    # path('in-apis/', views.test_view, name='test_view'),
    
    

    
    
    
    
    
]