from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User,Code,Attendance
import uuid
from .utils import send_email_token
from django.http import HttpResponse 
from django.db.models import Q
from .models import IncomingRequest, OutgoingRequest

from datetime import datetime, timedelta
import pytz



def check(request):     #deletes requests which have their time over 2hrs
    out_requests = OutgoingRequest.objects.filter(sender=request.user)
    in_requests = IncomingRequest.objects.filter(receiver=request.user)
    for out_req in out_requests:
        time = datetime.now(pytz.timezone('Asia/Kolkata'))-timedelta(hours=2)
        if(out_req.game_status=='pending' and out_req.request_time<time):
            request.user.worst_case_points+=int(out_req.points)
            request.user.requests_left+=1
            out_req.delete() 
    for in_req in in_requests:
        time = datetime.now(pytz.timezone('Asia/Kolkata'))-timedelta(hours=2)
        if(in_req.game_status=='pending' and in_req.request_time<time):
            in_req.receiver.worst_case_points+=int(in_req.points)
            in_req.delete()
    return        



def loginPage(request): 
    page = 'login'
    if request.user.is_authenticated:
        return redirect('participant_home') 

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password , email_verified=True)

        if user is not None:
            login(request, user)
            return redirect('participant_home') 
        else:
            messages.error(request, 'Email OR password does not exit') 
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.username.lower()
            user.email_token = str(uuid.uuid4())
            send_email_token(user.email, user.email_token)
            user.save()
            messages.success(request, f'Email has been sent to {user.email}')
        else:
            messages.error(request, 'An error occurred during registration (Ensure that you are not using the same email id, this error could have been caused by that)')

    return render(request, 'login_register.html', {'form': form})


def participant_home(request):
    d={}
    attendance = Attendance.objects.all().values()
    for x in attendance:
        d[x['code']]=x['value']
    k_l=list(d.keys())
    flag=1

    if request.user.is_authenticated:
        user_1= User.objects.get(email=str(request.user))
        if user_1.admin==True:
            flag=0
        check(request)
        if request.method == 'POST':
                if flag==1:
                    k_l=list(d.keys())
                    a=request.POST.get('text_input').strip().lower()
                    passcode = list(Code.objects.filter(user=request.user).values())
                    new_arr=[]
                    for x in passcode:
                        new_arr.append(x['data_item'])
                    if a not in new_arr:
                        if a in k_l:
                            Code.objects.create(
                            user=user_1,
                            data_item=a,
                            )
                            user_1.points +=d[a]
                            user_1.worst_case_points +=d[a]
                            user_1.save()
                            messages.success(request,'Attendance code accepted')
                        else:
                            messages.error(request,'Attendance code is not valid')
                    else:
                        messages.error(request,'You have already got points for submitting the above code . This is a repeat submission') 
                else:
                    a=request.POST.get('text_input').strip().lower()
                    if a in d:
                        messages.success(request,'Attendance code will no longer be accepted')
                        d.pop(a)
                        k_l=list(d.keys())
                        a1=Attendance.objects.get(code=a)
                        a1.delete()
                    else:
                        messages.error(request,'Attendance code is not valid')

        users=User.objects.all().order_by('-points').values()
        context = {
            'users': users,
            'flag':flag,
        }
        return render(request, 'participant_home.html', context)
    else:
        users=User.objects.all().order_by('-points').values()
        context = {
            'users': users,
            'flag':flag,
        }
        return render(request, 'participant_home.html', context)

def verify(request,token):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('participant_home')
    try:
        user = User.objects.get(email_token=token)
        user.email_verified = True
        user.save()
        messages.success(request, 'Email verified')
        login(request, user)
        return redirect('participant_home')
    except Exception as e:
        messages.error(request, 'Invalid request')
    
    return HttpResponse('verify')


def playGame(request):
    if request.user.is_authenticated:
        sender= User.objects.get(email=str(request.user))
        if sender.admin==True:
            messages.error(request, 'Admins are not allowed to play the Game')
            return render(request,'participant_home.html')
        
            #main game logic
        if request.method == 'POST'  and request.POST['action']=='make_request':
            num1 = request.POST.get('num1')
            num2 = request.POST.get('num2')
            num3 = request.POST.get('num3')
            points = request.POST.get('points')

            if(sender.requests_left<=0):
                messages.error(request, 'Daily Limits for requests reached')
                
            elif(sender.worst_case_points>=int(points)):
                receiver = User.objects.filter(Q(worst_case_points__gte=int(points)) & ~Q(email=sender.email) & Q(admin=False)).order_by('?').first()
                game_link = str(uuid.uuid4())
                if(receiver==None):
                    messages.error(request, 'No other user is available to play this game, Please wait until there are acive users.')
                
                else:
                    OutgoingRequest.objects.create(
                        sender=sender,
                        num1=num1,
                        num2=num2,
                        num3=num3,
                        points=points,
                        game_link=game_link,
                    ) 
                    IncomingRequest.objects.create(
                        receiver=receiver,
                        num1=num1,
                        num2=num2,
                        num3=num3,
                        points=points,
                        game_link=game_link,
                    )
                    #plan to do is to during acceptance get users by game_link
                    sender.requests_left-=1
                    sender.worst_case_points-=int(points)
                    receiver.worst_case_points-=int(points)
                    sender.save()
                    receiver.save()
                    messages.success(request,'Game request sent')
            else:
                if(sender.points<points):
                    messages.error(request, 'You do not have enough points or requests to play this game')
                else:
                    messages.error(request,'Please accept/decline pending requests to play the game')
        
        out_requests = OutgoingRequest.objects.filter(sender=sender)
        in_requests = IncomingRequest.objects.filter(receiver=sender)
        context = {'user':sender, 'out_requests' : out_requests, 'in_requests' :in_requests}
        
        return render(request,'playGame.html', context)
    else:
        return redirect('login')    
    



def Game(request, game_link):  #receiver plays the game
    
    if(request.user.is_authenticated):
        user = IncomingRequest.objects.get(game_link=game_link).receiver
        if(request.user.email!=user.email and request.user.admin==False):
            messages.error(request,'You do not have access to this game link')
            return redirect('playGame')
        
        if request.method == 'POST'  and request.POST['confirm']=='accept':
            in_req = IncomingRequest.objects.get(game_link=game_link)
            out_req = OutgoingRequest.objects.get(game_link=game_link)
            messages.success(request,'Game request accepted')
            context = {'user':user, 'in_req' : in_req, 'out_req' :out_req}
            #gotta start timer
            return redirect('theGame', game_link=game_link)
        elif request.method == 'POST'  and request.POST['confirm']=='decline':
            in_req = IncomingRequest.objects.get(game_link=game_link)
            out_req = OutgoingRequest.objects.get(game_link=game_link)
            points = in_req.points
            
            sender= out_req.sender
            user.worst_case_points+=int(points) #worst_case points increased
            sender.worst_case_points+=int(points)
            sender.requests_left+=1
            user.save()
            sender.save()
            in_req.delete()
            out_req.delete()

            messages.success(request,'Game request declined') 
            return redirect('playGame') 

        return render(request, 'Confirm.html', {'game_link': game_link})
    return redirect ('login')


def acceptRequest(request, game_link):
    if(request.user.is_authenticated == False):
        return redirect('login')
    
    
    out_req = OutgoingRequest.objects.get(game_link=game_link)
    
    if(out_req.game_status!='pending'):
        messages.error(request,'This game has already been played')
        return redirect('playGame')
    in_req = IncomingRequest.objects.get(game_link=game_link)
    if(request.user!=in_req.receiver and request.user.admin==False):
        messages.error(request,'You do not have access to this game link')
        return redirect('playGame')
    
    game_play = [i > 7 for i in [in_req.num1, in_req.num2, in_req.num3]]
    print(game_play)
    sender = out_req.sender
    receiver = in_req.receiver
    points = in_req.points
    
    if request.method == 'POST':
        
        choice = request.POST.get('choice')
        choice = choice=='True'
        
        if(game_play[out_req.turn-1] ^ choice): #sender win
            out_req.wins+=1
            messages.success(request,'You lost this round')
        else:
           messages.success(request,'You won this round')
        
        if(out_req.turn==3):
            if(out_req.wins>1):
                messages.success(request,'You lost this game')
                sender.points+=int(points)
                sender.worst_case_points+=2*(int(points))
                receiver.points-=int(points)      
                out_req.game_status = 'You won'
            else:
                messages.success(request,'You won this game')
                sender.points-=int(points)
                receiver.points+=int(points)
                receiver.worst_case_points+=2*(int(points))
                out_req.game_status = 'You lost'
            print("hello")
            in_req.delete()
            out_req.save()
            sender.save()
            receiver.save()
            return redirect('playGame')
        out_req.turn+=1
        out_req.save()

    context = {'turn':out_req.turn, 'game_link': game_link, 'in_req':in_req, 'out_req':out_req,'wins':out_req.turn-out_req.wins-1}    
    return render(request, 'acceptRequest.html', context)
