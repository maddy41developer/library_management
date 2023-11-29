from django.shortcuts import render,redirect
from .form import CustomUserForm
# from app.form import CustomUserForm
from app.models import *
from django.contrib.auth.models import User
# from django.contrib.auth import get_user
# from django.http import HttpResponse,JsonResponse
# from rest_framework.decorators import api_view
# from app.models import Book_Login
from django.contrib.auth import authenticate,login
from datetime import datetime, timedelta
from django.db import transaction
# Create your views here.

def home(request):
    return render(request,'home.html')
def signup(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        query_dict = request.POST
        username = query_dict.get('username')
        email =  query_dict.get('email')
        if form.is_valid():
            form.save()
            admin_user = User.objects.filter(email=email).first()
            user_id = admin_user.id
            print(user_id)
            user_details = StudentDetails(username = username,email = email,user_id = user_id)
            user_details.save()
            return redirect('student_login')
    return render(request,'student_register.html',{'form':form})

def studentlogin(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        try:
            user=authenticate(request,username=name,password=pwd)
            print(1)
            if user is not None:
                print(2)
                login(request,user)
                print(3)
                user_id = request.user.id
            print(4)
            student=StudentDetails.objects.filter(user_id = user_id).first()
            print(5)
            if student.status==1:
                return redirect('take')
            else:
                print(6)
                return redirect ('student_login')

        except:
            pass
    return render(request,'student_login.html')

def adminlogin(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        try:
            print(3)
            user=authenticate(request,username=name,password=pwd)
            print(user)
            print(4)
            if user is not None:
                print(5)
                login(request,user)
                print(6)
                return redirect('Bookdetails')
            else:
                print(7)
                return redirect ('admin_login')

        except:
            pass
    return render(request,'admin_login.html')

def bookdetails(request):
    obj=BookDetails.objects.all()
    return render(request,'Bookdetails.html',{'obj':obj})

def take(request):
    return render(request,'take.html')
def lib(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            date = datetime.now().date()
            library=BookDetails.objects.create(name=request.POST.get('Name'),book_code=request.POST.get('Code'),author_name=request.POST.get('Author'),
                                            date=request.POST.get('Date'),status=request.POST.get('Status'),amount=request.POST.get('Amount'),
                                            created_date=date,created_by=user_id,available_books = request.POST.get('available_books'),
                                            book_img = request.FILES['updatebook'])
            return redirect("Bookdetails")
        else:
            return redirect("book")
    return render(request, 'book.html')

def updatebook(request,pk):
    obj=BookDetails.objects.get(id=pk)
    if request.method=='POST':
        library = BookDetails.objects.filter(id=pk).first()
        library.name = request.POST.get('Name')
        library.book_code = request.POST.get('Code')
        library.author_name = request.POST.get('Author')
        library.date = request.POST.get('Date')
        library.amount = request.POST.get('Amount')
        library.available_books = request.POST.get('available_books')
        library.book_img = request.FILES['updatebook']
        date = datetime.now().date()
        library.updated_date = date
        library.save()
        return redirect('Bookdetails')
    return render(request,'updatebook.html',{'obj':obj})

def deletebook(request,pk):
    obj=BookDetails.objects.filter(id=pk).delete()
    return redirect('Bookdetails')