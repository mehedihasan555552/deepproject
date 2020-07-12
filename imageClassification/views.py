from .models import Users, Files, Result
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from .cancerModel import *
import re
from zipfile import ZipFile
import os


# Global variables
uploadedFile = None
currentUser = None
isUserExist = False
isinvalidUser = False
filelist = []
predictlist = []

# Create your views here.
#Index  home page
def Landing(request):
    return render(request, 'imageClassification/landing.html')

def Index(request):
    global uploadedFile
    global currentUser
    global filelist
    global predictlist
    if currentUser == None:
        return redirect(Landing)

    content = {'file':uploadedFile, 'user':currentUser, 'filelist':filelist, 'predictlist':predictlist}
    print(content)
    return render(request, 'imageClassification/index.html',content)
    
def createNew(request):
    global uploadedFile
    uploadedFile = None
    global filelist
    filelist = []
    global predictlist
    predictlist = []
    return redirect(Index)

def SignupOrLogin(request):
    global isUserExist
    global isinvalidUser
    content = {'isUserExist': isUserExist, 'isinvalidUser': isinvalidUser}
    print(f"content: {content}")
    return render(request, 'imageClassification/signup_login.html',content)

def processSignup(request):
    global isinvalidUser
    global isUserExist
    global currentUser
    tempUser = None
    if request.method == 'POST':
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Sign Up Data: Name: {fullname}, Email: {email}, Password: {password}")

        try:
            Users.objects.get(Email=email)
        except Users.DoesNotExist:
            tempUser = False

        if tempUser == False:
            currentUser = Users.objects.create(FullName=fullname, Email=email, Password=password)
            return redirect(Index)
        else:
            isinvalidUser = False
            isUserExist = True
            print(f"user exist : {isUserExist}")
            return redirect(SignupOrLogin)

    return redirect(SignupOrLogin)

def processLogin(request):
    global currentUser
    global isUserExist
    global isinvalidUser
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Log In Data: Email: {email}, Password: {password}")

        try:
            currentUser = Users.objects.get(Email=email, Password=password)
            return redirect(SignupOrLogin)
        except Users.DoesNotExist:
            tempUser = False
        
        if tempUser == False:
            isinvalidUser = True
            isUserExist = False
        else:
            isinvalidUser = False
        
        print(f"invalid User : {isinvalidUser}")
    return redirect(SignupOrLogin)
    

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
        return redirect(Index)

    return redirect(Index)

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


    return redirect(Index)