from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.TaskLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.TaskSignup.as_view(), name='signup'),
    path('', views.TaskList.as_view(), name='list_view'),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='detail_view'),
    path('task/new/',views.TaskCreate.as_view(), name='create_view'),
    path('task/<int:pk>/update/', views.TaskUpdate.as_view(), name='update_view'),
    path('task/<int:pk>/delete/', views.delete, name='delete_view'),
    path('task/<int:pk>/complete/', views.uupdate_complete, name='uupdate-complete'),
    path('task/<int:pk>/incomplete/', views.uupdate_incomplete, name='uupdate-incomplete'),
]