from .models import Users, Files, Result
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from .cancerModel import *
import re
from zipfile import ZipFile
import os
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *




def usersignup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account was Created for ' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'imageClassification/signup.html',context)




def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')

        else:
            messages.info(request,'username or password incorrect.')
    context={}
    return render(request, 'imageClassification/login.html',context)



# Global variables
uploadedFile = None
currentUser = None
#isUserExist = False
#isinvalidUser = False
filelist = []
predictlist = []

# Create your views here.
#Index  home page
def Landing(request):
    return render(request, 'imageClassification/landing.html')


@login_required(login_url='login')
def Index(request):
    global uploadedFile
    global currentUser
    global filelist
    global predictlist
    #if currentUser == None:
        #return redirect('Landing')

    #content = {'file':uploadedFile, 'user':User, 'filelist':filelist, 'predictlist':predictlist}
    #print(content)
    return render(request, 'imageClassification/index.html',{'file':uploadedFile,'filelist':filelist,'predictlist':predictlist,'user':currentUser,})

def createNew(request):
    global uploadedFile
    uploadedFile = None
    global filelist
    filelist = []
    global predictlist
    predictlist = []
    return redirect(Index)






#def SignupOrLogin(request):
    #global isUserExist
    #global isinvalidUser
    #content = {'isUserExist': isUserExist, 'isinvalidUser': isinvalidUser}
    #print(f"content: {content}")
#    return render(request, 'imageClassification/signup_login.html')

#def processSignup(request):
    #global isinvalidUser
    #global isUserExist
#    global currentUser
#    tempUser = None
#    if request.method == 'POST':
#        fullname = request.POST.get('name')
#        email = request.POST.get('email')
#        password = request.POST.get('password')

#        print(f"Sign Up Data: Name: {fullname}, Email: {email}, Password: {password}")

#        try:
#            Users.objects.get(Email=email)
#        except Users.DoesNotExist:
#            tempUser = False

#        if tempUser == False:
#            currentUser = Users.objects.create(FullName=fullname, Email=email, Password=password)
#            return redirect('Index')
#        else:
#            isUserExist = True
#            print(f"user exist : {isUserExist}")
#            return redirect(SignupOrLogin)

#    return redirect('SignupOrLogin')

#def processLogin(request):
#    global currentUser
    #global isUserExist
    #global isinvalidUser
#    if request.method == 'POST':
##        password = request.POST.get('password')

#        print(f"Log In Data: Email: {email}, Password: {password}")
#
#        try:
#            currentUser = Users.objects.get(Email=email, Password=password)
#            return redirect('Index')
#        except Users.DoesNotExist:
#            pass
            #tempUser = False

        #if tempUser == False:
            #isinvalidUser = True
            #isUserExist = False
        #else:
            #isinvalidUser = False

        #print(f"invalid User : {isinvalidUser}")


#    return redirect('SignupOrLogin')


def logout(request):
    global uploadedFile
    uploadedFile = None
    global currentUser
    currentUser = None
    global filelist
    filelist = []
    global predictlist
    predictlist = []
    return redirect(Landing)

def uploadFile(request):
    global uploadedFile
    global currentUser
    if request.method == 'POST':
        uploaded_file = request.FILES['sampleFile']
        fileSystem = FileSystemStorage()
        fileName = fileSystem.save(uploaded_file.name, uploaded_file)
        res = Files(Path = '/media/'+fileName, userId=currentUser)
        print(f"files object instance: {res}")
        uploadedFile = fileName
        print(f'file name : {uploadedFile}')
        return redirect('Index')

    return redirect('Index')

def processPrediction(request):
    global filelist
    global predictlist
    res = None
    if uploadedFile.find('.zip') > -1:
        #zipfile code goes here
        print('uploaded file is a zip file')
        zf = ZipFile(os.getcwd()+'/media/'+uploadedFile)
        zf.extractall(os.getcwd()+'/media/')
        arr = zf.namelist()
        # print(arr[0])
        # print(arr[0].split('/'))
        prediction('/media/'+arr[0].split('/')[0])
    else:
        print('uploaded file is a NOT a zip file')
        res = prediction('/media/'+uploadedFile)
        filelist.append(res['file'])
        predictlist.append(res['prediction'])


    return redirect('Index')
