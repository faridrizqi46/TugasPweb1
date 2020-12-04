# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
import datetime
from .decorators import unauthenticated_user
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'AppPweb1/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('TodoList')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'AppPweb1/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def index(request): #the index view
	todos = TodoList.objects.all() #quering all todos with the object manager
	categories = Category.objects.all() #getting all categories with object manager
	if request.method == "POST": #checking if the request method is a POST
		if "taskAdd" in request.POST: #checking if there is a request to add a todo
			title = request.POST["description"] #title
			date = str(request.POST["date"]) #date
			category = request.POST["category_select"] #category
			content = title + " -- " + date + " " + category #content
			Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
			Todo.save() #saving the todo 
			return redirect("/") #reloading the page
		
		if "taskDelete" in request.POST: #checking if there is a request to delete a todo
			checkedlist = request.POST["checkedbox"] #checked todos to be deleted
			for todo_id in checkedlist:
				todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
				todo.delete() #deleting todo

	return render(request, "AppPweb1/index.html", {"todos": todos, "categories":categories})
