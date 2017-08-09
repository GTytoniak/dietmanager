from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.template.response import TemplateResponse
from django.views import View
from .forms import AddUserForm, LoginForm, BmiForm, BmiModifyForm, GdaForm, GdaModifyForm
from .models import Product, UserData, Bmi, UserMoreData, Gda
from django.template.backends.django import Template
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin,\
    LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView


class CreateUserView(View):
    def get(self, request):
        form = AddUserForm()
        ctx = {"form": form}
        return TemplateResponse(request, 'create_user.html', ctx)
    
    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)   
                ctx = {'msg': 'User created sucessfully, you can now login!'}
                return TemplateResponse(request, 'home.html', ctx)
            else:
                raise ValidationError("Password error!")
        
        else:
            ctx = {"form": form, 'msg': 'Wrong data!'}
            return TemplateResponse(request, 'create_user.html', ctx)

class HomeView(View):
    def get(self, request):
        ctx = {"msg": "Welcome in dietmanager!"}
        return TemplateResponse(request, 'home.html', ctx)
    def post(self, request):
        ctx = {"msg": "Welcome in dietmanager!"}
        return TemplateResponse(request, 'home.html', ctx)

class LoginView(View):
        
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'login.html', ctx)
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password=password)
            print('user', user)
            if user is not None:
                login(request, user)
                ctx = {'msg': 'You are logged in!' }
                return TemplateResponse( request, 'home.html', ctx)
            else:
                ctx = {'msg': 'Login attempt failed!'}
                return TemplateResponse( request, 'login.html', ctx)
            
class LogoutView(View):
    def get(self, request):
        ctx = {'msg': 'You have sucessfully logged out! '}
        logout(request)
        return TemplateResponse(request, 'logout.html', ctx)

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'dietmanager.add_product'
    model = Product
    template_name = "create_product.html"
    fields = '__all__'
    success_url = "/create_product"
    
class ProductEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'dietmanager.change_product'
    model = Product
    template_name = "edit_product.html"
    fields = '__all__'
    success_url = "/home.html"
    
class UserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user_id = int(user_id)        
        user = User.objects.get(id=user_id)
        
        if Bmi.objects.filter(user=user).count():
            bmi = Bmi.objects.get(user=user)    
            msg = ("Your current BMI is presented below. To update it, go to BMI calculator section. {}".format(bmi))
            bmi_url =  "bmi_modify"
            
        else:   
            msg = ("Your current BMI is not counted, go to BMI calculator section!")
            bmi_url = "bmi_calc"
        
        if Gda.objects.filter(user=user).count():
            gda = Gda.objects.get(user=user)    
            msg2 = ("Your current GDA is presented below. To update it, go to GDA calculator section. {}".format(gda))
            gda_url =  "gda_modify"
            
        else:   
            msg2 = ("Your current Gda is not counted, go to GDA calculator section!")
            gda_url = "gda_calc"
        CONTENT_DICT = {
                "username": user,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "bmi_url": bmi_url,
                "gda_url": gda_url,
                "msg":msg, 
                "msg2": msg2,  
            }
        
        return TemplateResponse(request, 'user.html', CONTENT_DICT)


class BmiCalcView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        
        form = BmiForm()
        ctx = {'form': form}
        return TemplateResponse( request, 'bmi_calc.html', ctx)
    
    def post(self, request, user_id):
        user_id = int(user_id)        
        form = BmiForm(request.POST)
        if form.is_valid():
            
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            bmi = weight / (height * height)
            userook = UserData.objects.create(user_id= user_id, weight=weight, height=height)
            bmiok = Bmi.objects.create(user_id= user_id, bmi=bmi)
            msg = {"msg": 'BMI counted succesfully!'}
            return TemplateResponse(request, 'home.html', msg)
        else:
            raise ValidationError("Data error!")
        
class BmiModifyView(LoginRequiredMixin, View):
     
    def get(self, request, user_id):
         
        userook = UserData.objects.get(user_id= user_id)
        initial={'weight': userook.weight,'height': userook.height}

        form = BmiModifyForm(initial=initial)
        ctx = {'form': form}    
         
        return TemplateResponse( request, 'bmi_modify.html', ctx)
     
    def post(self, request, user_id):
        user_id = int(user_id)        
        form = BmiModifyForm(request.POST)
        if form.is_valid():
             
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            bmi = weight / (height * height)
            userook = UserData.objects.get(user_id= user_id)
            userook.weight=weight
            userook.height=height
            userook.save()
            bmiok = Bmi.objects.get(user_id= user_id)
            bmiok.bmi=bmi
            bmiok.save()
            msg = {"msg":"Your BMI was updated sucessfully!"}
            return TemplateResponse(request, 'home.html', msg)
        else:
            raise ValidationError("Data error!")


class GdaCalcView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        
        form = GdaForm()
        ctx = {'form': form}
        return TemplateResponse( request, 'gda_calc.html', ctx)
    
    def post(self, request, user_id):
        user_id = int(user_id)        
        form = GdaForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            sex = form.cleaned_data['sex']
            activity = form.cleaned_data['activity']
            gda = (weight * 24) * float(sex) * float(activity)
            usermoreok = UserMoreData.objects.create(user_id= user_id, weight=weight, sex=sex, activity=activity)
            gdaok = Gda.objects.create(user_id= user_id, gda=gda)
            msg2 = {"msg2": "GDA counted succesfully!"}
            return TemplateResponse(request, 'home.html', msg2)
        else:
            raise ValidationError("Data error!")
        
class GdaModifyView(LoginRequiredMixin, View):
     
    def get(self, request, user_id):
         
        usermoreok = UserMoreData.objects.get(user_id= user_id)
        initial={'weight': usermoreok.weight,'sex': usermoreok.sex, 'activity': usermoreok.activity }

        form = GdaModifyForm(initial=initial)
        ctx = {'form': form}    
         
        return TemplateResponse( request, 'gda_modify.html', ctx)
     
    def post(self, request, user_id):
        user_id = int(user_id)        
        form = GdaModifyForm(request.POST)
        if form.is_valid():
             
            weight = form.cleaned_data['weight']
            sex = form.cleaned_data['sex']
            activity = form.cleaned_data['activity']
            gda = (weight * 24) * float(sex) * float(activity)
            usermoreok = UserMoreData.objects.get(user_id= user_id)
            usermoreok.weight=weight
            usermoreok.sex = sex
            usermoreok.activity = activity
            usermoreok.save()
            gdaok = Bmi.objects.get(user_id= user_id)
            gdaok.gda = gda
            gdaok.save()
            msg = {"msg":"Your GDA was updated sucessfully!"}
            return TemplateResponse(request, 'home.html', msg)
        else:
            raise ValidationError("Data error!")
        
class ProductsView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        CONTENT_DICT = {
            "products": products, 
        }
        return TemplateResponse(request, 'products.html', CONTENT_DICT)
        
class DishesCreateView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user_id = int(user_id)
        breakfasts = Product.objects.filter(food_category=1)
        brunches = Product.objects.filter(food_category=2)
        dinners = Product.objects.filter(food_category=3)
        suppers = Product.objects.filter(food_category=4)
        gda = Gda.objects.get(user_id=user_id).gda
        def breakfastdishkcal(dish):
            return abs(dish.kcal - gda * 0.4)
        breakfastdish = breakfasts[0]
        
        def brunchdishkcal(dish):
            return abs(dish.kcal - gda * 0.15)
        brunchdish = brunches[0]
        
        def dinnerdishkcal(dish):
            return abs(dish.kcal - gda * 0.3)
        dinnerdish = dinners[0]
        
        def supperdishkcal(dish):
            return abs(dish.kcal - gda * 0.15)
        supperdish = suppers[0]
        
        for breakfast in breakfasts:
            if (breakfastdishkcal(breakfast) <  breakfastdishkcal(breakfastdish)): 
                breakfastdish = breakfast
                
        for brunch in brunches:
            if (brunchdishkcal(brunch) <  brunchdishkcal(brunchdish)): 
                brunchdish = brunch
                
        for dinner in dinners:
            if (dinnerdishkcal(dinner) <  dinnerdishkcal(dinnerdish)): 
                dinnerdish = dinner
                
        for supper in suppers:
            if (supperdishkcal(supper) <  supperdishkcal(supperdish)): 
                supperdish = supper
        
        totalkcal = breakfastdish.kcal + brunchdish.kcal + dinnerdish.kcal + supperdish.kcal
        ctx = {"breakfastdish": breakfastdish, "brunchdish": brunchdish, "dinnerdish": dinnerdish, "supperdish": supperdish, "totalkcal": totalkcal}
            
        return TemplateResponse(request, 'dishes.html', ctx)

        