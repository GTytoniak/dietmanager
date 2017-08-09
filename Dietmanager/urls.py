"""Dietmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from dietmanager.views import CreateUserView, HomeView, LoginView, LogoutView, ProductCreateView, UserView, ProductEditView, BmiCalcView, BmiModifyView, GdaCalcView, GdaModifyView, ProductsView, DishesCreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create_user/', CreateUserView.as_view(), name='create_user'),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^login/', LoginView.as_view(), name='login'), 
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^create_product/', ProductCreateView.as_view(), name='create_product'),
    url(r'^user/(?P<user_id>(\d)+)', UserView.as_view(), name='user_view'),
    url(r'^edit_product/?P<pk>(\d)+', ProductEditView.as_view(), name='edit_product'),
    url(r'^bmi_calc/(?P<user_id>(\d)+)', BmiCalcView.as_view(), name='bmi_calc'), 
    url(r'^bmi_modify/(?P<user_id>(\d)+)', BmiModifyView.as_view(), name='bmi_modify'),
    url(r'^gda_calc/(?P<user_id>(\d)+)', GdaCalcView.as_view(), name='gda_calc'), 
    url(r'^gda_modify/(?P<user_id>(\d)+)', GdaModifyView.as_view(), name='gda_modify'),
    url(r'^products/', ProductsView.as_view(), name='products'),
    url(r'^dishes/(?P<user_id>(\d)+)', DishesCreateView.as_view(), name='dishes'), 
]
