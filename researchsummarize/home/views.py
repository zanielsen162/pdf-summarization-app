from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member, Summary
from .forms import PromptForm
from pdf_summarization_app import call_llm

def home(request):
    context = {'user': request.user}  # Pass the user object explicitly
    print(request.GET)
    return render(request, 'home.html', context)

# Create your views here.

def html_button(request):
    if request.method == "POST":  
        print("Request POST data:", request.POST)  # Print POST data
        print("Request FILES data:", request.FILES)

        form = PromptForm(request.POST, request.FILES)  

        if form.is_valid():  
            field = form.cleaned_data['field']
            topics = form.cleaned_data['topics']
            file = request.FILES["file"]
            print(file)

            print("File received:", file)  # Debugging line to check the file

            if file:
                try:
                    # Assuming genai.upload_file expects a file-like object
                    with open(file.name, 'wb') as f:
                        for chunk in file.chunks():  # Writing file in chunks
                            f.write(chunk)
                    result = "File uploaded and processed."
                except Exception as e:
                    result = f"Error uploading file: {str(e)}"
            else:
                result = "No file uploaded"

            # result = call_llm(file, field, topics)
            print("Request files:", request.FILES)
            return render(request, 'home.html', {'form': form, 'result': result})
    else:  
        form = PromptForm()  
    return render(request,'home.html',{'form':form})