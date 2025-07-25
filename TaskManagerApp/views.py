from django.shortcuts import render,redirect
from .models import *
# Create your views here.

#Homeview
def HomeView(request):
    return render (request,'home.html')

#Create task
def AddTaskView(request):
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']

        data=TaskManager.objects.create(name=name,description=description)
        data.save()
        return redirect('home')

    return render(request,'task_form.html')

#view task
def ListTaskView(request):
    data=TaskManager.objects.all()
    return render(request,'task_list.html',{'tasks':data})


#Update task
def UpdateTaskView(request,pk):
    data=TaskManager.objects.get(id=pk)
    if request.method=='POST':
        data.name=request.POST['name']
        data.description=request.POST['description']

        # obj=data.objects.create(name=name,description=description)
        # obj.save()
        data.save()
        return redirect('home')
    return render(request,'task_update.html',{'tasks':data})

#Delete task
def DeleteTaskView(request,pk):
    data=TaskManager.objects.get(id=pk)
    data.delete()
    return redirect('list_task')

