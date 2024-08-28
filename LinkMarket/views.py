# views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomLoginForm, ProductForm, CategoryForm, BusinessForm
from django.http import HttpResponse
from .models import Product, Category, Business, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'buyer':
                return redirect('buyer_account')
            else:
                return redirect('register_business')
        else:
            print(form.errors)
    else:
        selected_role = request.session.get('selectedRole')
        form = CustomUserCreationForm(initial={'role': selected_role})
    return render(request, 'LinkMarket/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'buyer':
                    return redirect('buyer_account')
                else:
                    return redirect('seller_account')
            else:
                form.add_error(None, 'Invalid email or password')
        else:
            print(form.errors)
    else:
        form = CustomLoginForm()
    return render(request, 'LinkMarket/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def landing_page(request):
    return render(request, 'LinkMarket/index.html')

@login_required
def buyer_account(request):
    first_name = request.user.first_name
    return render(request, 'LinkMarket/buyer/ecom.html')

@login_required
def seller_account(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    
    initials = f"{first_name[0]}{last_name[0]}".upper()
    return render(request, 'LinkMarket/seller/dash2.html', {'first_name': first_name, 'initials': initials})

@login_required
def dash(request):
    return render(request,'LinkMarket/seller/dash.html' )

# Business
@login_required
def register_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            return redirect('seller_account')  
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = BusinessForm()
    return render(request, 'LinkMarket/seller/register_business.html', {'form': form})


def registration_success(request):
    return render(request, 'LinkMarket/seller/registration_success.html')

def registration_success(request):
    return render(request, 'registration/registration_success.html')


# create category
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            business_id = form.cleaned_data['business_id']
            business = get_object_or_404(Business, id=business_id, user_id=request.user)
            category = form.save(commit=False)
            category.business = business
            category.save()
            return redirect('category_list')
    else:
        business_id = request.GET.get('business_id')
        form = CategoryForm(initial={'business_id': business_id})
    return render(request, 'LinkMarket/seller/category_form.html', {'form': form})
@login_required        
def category_list(request):
    categorys = Category.objects.all()
    return render(request, 'LinkMarket/seller/category_list.html', {'categorys': categorys})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'LinkMarket/seller/category_confirm_delete.html', {'category': category})    

@login_required
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    return  render(request, 'LinkMarket/seller/category_detail.html', {'category': category})

@login_required
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'LinkMarket/seller/category_edit.html', {'form': form})

# cart
@login_required
def cart(request):
    return render(request, 'LinkMarket/buyer/cart.html')


def About(request):
    return render(request, "LinkMarket/About.html")

# create product 
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list') 
    else:
        form = ProductForm()
    return render(request, 'LinkMarket/seller/add-product.html', {'form': form})

@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'LinkMarket/seller/product_detail.html', {'product': product})

@login_required
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'LinkMarket/seller/product_form.html', {'form': form})

@login_required
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  
    return render(request, 'LinkMarket/seller/product_confirm_delete.html', {'product': product})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'LinkMarket/seller/products.html', {'products': products})






