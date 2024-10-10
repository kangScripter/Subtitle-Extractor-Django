import os
from django.http import JsonResponse
from django.shortcuts import render,redirect 
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from utils.subtitle_extract import SubtitlesExtract,SearchQuery
from django.conf import settings
from .models import Substitle,  Video
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
import urllib.parse

# Create your views here.

def Home(requests):
    if requests.method == 'GET':
        videos = Video.objects.all()
        subtitles = Substitle.objects.all().values()
        return render(requests,"home.html",{"videos":videos,"subtitles":subtitles})
def Login(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']
        user = authenticate(requests, username=username, password=password)
        if user is not None:
            login(requests, user)
            return redirect('/video')  # redirect to home page after login
        else:
            messages.info(requests,"Invalid Username/Password")
            return render(requests,"login.html")
    return render(requests, 'login.html')

def Register(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(requests,"Username already exists")
            return render(requests,"Login.html")
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(requests,user)
        return redirect('/video')
    
    return render(requests, 'register.html')

def Logout(requests):
    auth.logout(requests)
    return redirect("/")


def VideoUpload(requests):
    try:
        if not requests.user.is_authenticated:
            messages.info(requests,"Login Required")
            return render(requests,"home.html")
        if requests.method == "POST":
            print(requests)
            print(requests.FILES)
            if 'video' not in requests.FILES:
                messages.error(requests,"Select a file")
                return render(requests,"video.html")
            file = requests.FILES['video']
            file_save = FileSystemStorage()
            file_save.save(file.name,file)
            file_url = file_save.url(file)
            BASE_DIR = os.path.abspath(settings.BASE_DIR)
            print(BASE_DIR)
            file_path =BASE_DIR + file_url
            if requests.user.is_authenticated:
                if not Video.objects.filter(video_filename=file.name).exists():
                    vidObj = Video.objects.create(Fkey=requests.user,video_filename=file.name)
                    vidObj.save()
                else:
                    vidObj = Video.objects.filter(video_filename=file.name).get()
                if not Substitle.objects.filter(video_file_name=file.name).exists():
                    Extract = SubtitlesExtract()
                    dir , subtitles = Extract.runExtractor(file_path)
                    for idx,sub in enumerate(subtitles):
                        subtitle_language = sub["lang"]
                        sub_file =sub["file"]
                        fp = os.path.join(dir,sub_file)
                        f = open(fp,"rb")
                        subtitle_file = File(f,name=sub_file)
                        print(subtitle_file)
                        if not Substitle.objects.filter(video_file_name=file.name,lang = subtitle_language).exists():
                            obj = Substitle.objects.create(Fkey=vidObj,file_name=sub_file,lang=subtitle_language,subtitles_file=subtitle_file,video_file_name=file.name)
                            obj.save()
                            print("Object Created")
                        else:
                            print("Object Already Created")
                    Extract.clean(dir,subtitles)
                mydata = Substitle.objects.filter(video_file_name=file.name).values()
                print(mydata)
                MediaClean()
                return render(requests,"player.html",{"video_url":file_url,"tracks":mydata,"media":settings.MEDIA_URL})
           
            else:
                return render(requests,"login.html")
                
        
        else:
            return render(requests,'video.html')
    except Exception as e:
        return JsonResponse({'status':'false','error':e }, status=500)

def MediaClean():
    media_path = settings.MEDIA_ROOT
    for f in os.listdir(media_path):
        if f.endswith(".srt") or f.endswith(".vtt"):
            file = os.path.join(media_path,f)
            try:
                os.remove(file)
            except:
                pass
def Query(requests):
    if not requests.user.is_authenticated:
        messages.info(requests,"Login Required")
        return render(requests,"home.html")
    if requests.method == "GET":
        query = requests.GET.get("query")
        lang  =  requests.GET.get("lang")
        file_path = urllib.parse.unquote(requests.GET.get("video_file"))
        video_name = file_path.split("/")[2]
        media_path = file_path.split("/")[1]
        print(query,lang,video_name)
        mydata = Substitle.objects.filter(video_file_name=video_name,lang = lang).values()
        print(mydata)
        subtitle_path = os.path.join(media_path, mydata[0]['subtitles_file'])
        SearchObj = SearchQuery(subtitle_path,query)
        timestamps = SearchObj.search()
        print(timestamps)
        if len(timestamps)==0:
            messages.info(requests,"Not Found")
            return render(requests,"player.html",{"video_url":f"/{media_path}/{video_name}","tracks":mydata,"media":settings.MEDIA_URL})
        return render(requests,"player.html",{"video_url":f"/{media_path}/{video_name}","tracks":mydata,"media":settings.MEDIA_URL,"timestamps": timestamps})


def List(requests):
    if not requests.user.is_authenticated:
        messages.info(requests,"Login Required")
        return render(requests,"home.html")
    if requests.method == "GET":
        videos = Video.objects.all()
        subtitles = Substitle.objects.all().values()
        return render(requests,"list.html",{"videos":videos,"subtitles":subtitles})
    
def PlayVideo(requests):
    if not requests.user.is_authenticated:
        messages.info(requests,"Login Required")
        return render(requests,"home.html")
    if requests.method == "GET":
        video_filename = requests.GET.get("video_url")
        mydata = Substitle.objects.filter(video_file_name=video_filename).values()
        media_path = settings.MEDIA_URL
        return render(requests,"player.html",{"video_url":f"{media_path}{video_filename}","tracks":mydata,"media":settings.MEDIA_URL})
