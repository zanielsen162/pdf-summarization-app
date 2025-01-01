from django.shortcuts import render

# Create your views here.
# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import PromptForm
from pdf_summarization_app import call_llm
from django.shortcuts import get_object_or_404, render
from .models import Response

from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    user_form = PromptForm()
    result = None
    selected_response = None

    if request.method == 'POST':
        user_form = PromptForm(request.POST, request.FILES)

        if user_form.is_valid():
            field = user_form.cleaned_data['field']
            topics = user_form.cleaned_data['topics']
            file = request.FILES['file']

            # Call the LLM and process the file
            result, title = call_llm(file, field, topics)

            # Get or create the PrevResponses instance for the logged-in user
            if request.user.is_authenticated:
                prev_responses, created = PrevResponses.objects.get_or_create(user=request.user)

                # Create and save the Response object
                result_obj = Response.objects.create(
                    title=title,
                    content=result,
                    previous_responses=prev_responses
                )
                
    elif request.method == 'GET' and request.GET.get('response_id'):
        # Handle displaying a specific response if `response_id` is passed
        response_id = request.GET.get('response_id')
        selected_response = get_object_or_404(
            Response, id=response_id, previous_responses__user=request.user
        )

    # Retrieve all previous responses for the user
    previous_responses = (
        request.user.prev_responses.response_set.all()
        if request.user.is_authenticated and hasattr(request.user, 'prev_responses')
        else []
    )

    # Render the home page with the form, responses, and the selected response
    return render(
        request,
        'home.html',
        {
            'user_form': user_form,
            'previous_responses': previous_responses,
            'selected_response': selected_response,
            'result': result
        }
    )



# Define a view function for the home page
# @login_required
# def home(request, id):
#     context = { 'user_form': PromptForm() }
#     result_obj = None

#     result = None
#     # form = PromptForm(request.POST or None, request.FILES or None) 

#     if request.method == 'POST':
#         user_form = PromptForm(request.POST, request.FILES)

#         if user_form.is_valid():
#             field = user_form.cleaned_data['field']
#             topics = user_form.cleaned_data['topics']
#             file = request.FILES["file"]

#             result, t = call_llm(file, field, topics)   

#             try:
#                 # Get or create the user's `PrevResponses` object
#                 prev_responses, created = PrevResponses.objects.get_or_create(user=request.user)

#                 # Create a new Response and associate it with the user's PrevResponses
#                 result_obj = Response.objects.create(
#                     title=t,
#                     content=result,
#                     previous_responses=prev_responses
#                 )

#                 return redirect(f"/response/{result_obj.id}")
#             except Exception as e:
#                 return render(request, 'home.html', {'user_form': user_form, 'result': f"Error: {e}"})
#     else:
#         user_form = PromptForm()

#     return render(request,'home.html', {'user_form': user_form, 'result': result})

# Define a view function for the login page
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/home/')
    
    # Render the login page template (GET request)
    return render(request, 'login.html')

# Define a view function for the registration page
def register_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
    
    # Render the registration page template (GET request)
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect(home)

@login_required
def response_detail(request, id):
    response = get_object_or_404(Response, id=id, previous_responses__user=request.user)
    return render(request, 'response_detail.html', {'response': response})
