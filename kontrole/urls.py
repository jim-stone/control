from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from kontrolBack.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('', include('kontrolBack.urls'))
]
