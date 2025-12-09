from django.shortcuts import render, redirect
# from .forms import RegisterForm, TodoForm
from todoApp.models import Todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    # the commented block below is for if we're using a django model form
    
    # form = TodoForm(request.POST)
    # if request.method == 'POST':
    #     if form.is_valid():
    #         todo = form.save(commit=False)
    #         todo.user = request.user
    #         todo.save()
    
    
    name = request.user.username
    alltasks = Todo.objects.filter(user=request.user)
    completed = Todo.objects.filter(completed=True, user=request.user)
    uncompleted = Todo.objects.filter(completed=False, user=request.user)
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        
        # check for empty content fields
        if not content:
            messages.error(request, 'Please input a Todo')
            return redirect('home')
        
        obj = Todo.objects.create(
            user= user,
            content = content
        )
        obj.save()
        messages.success(request, 'Task added successfully')
        return redirect('home')
        
    return render(request, 'home.html', {
        'name': name,
        'comp': len(completed),
        'uncomp': len(uncompleted),
        'all': alltasks,
        'comp1': completed
        })


def delete_task(request, p_id):
    obj = Todo.objects.get(id=p_id)
    obj.delete()
    messages.success(request, 'Task deleted successfully')
    return redirect('home')

def update_task(request, p_id):
    obj = Todo.objects.get(id=p_id)
    obj.completed = True
    obj.save()
    return redirect('home')

def register_user(request):
    # form = RegisterForm(request.POST)
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    
    # ensures that the register page cannot be accessed by an already logged in user.
    if request.user.is_authenticate:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        # unique username validation
        if User.objects.filter(username = username).exists():
            messages.error(request, 'A user with the same username already exists!')
            return redirect('register')
        
        # password match validation
        if password != confirm_password:
            messages.error(request, 'The two passwords do not match!')
            return redirect('register')
        
        # checks for empty fields
        if not (username and firstname and lastname and email and password and confirm_password):
            messages.error(request, 'Fill in all the fields!')
            return redirect('register')
        
        # create the user object
        user = User.objects.create_user(
            username=username,
            first_name=firstname,
            last_name = lastname,
            email=email,
            password = password
        )
        user.save()
        messages.success(request, 'Registered succesfully')
        return redirect('login')
    return render(request, 'register_user.html', {})


def login_user(request):
    # login page cannot be accessed if user is logged in
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        
        # checks for empty login fields
        if not (username and password):
            messages.error(request, 'Fill in the fields')
            return redirect('login')
            
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login succesful!')
            return redirect('home')
        else:
            messages.error(request, 'invalid login')
            return redirect('login')
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')