from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User,Code,Attendance
import uuid
from .utils import send_email_token
from django.http import HttpResponse 
from django.db.models import Q
from .models import IncomingRequest, OutgoingRequest, Status

from datetime import datetime, timedelta
import pytz


TIME_ZONE =  'Asia/Kolkata'
Game_time = 2   #in min 



def check(request):     #deletes requests which have their time over 2hrs
    out_requests = OutgoingRequest.objects.filter(sender=request.user)
    in_requests = IncomingRequest.objects.filter(receiver=request.user)
    time_now = datetime.now(pytz.timezone(TIME_ZONE))   #timezone
    print(time_now)
    for out_req in out_requests:
        if(out_req.game_status=='pending' and out_req.valid_until<time_now):
            try:
                # out_req.sender.worst_case_points+=int(out_req.points)
                # #out_req.sender.points+=int(out_req.points)
                # out_req.sender.requests_left+=1
                # out_req.sender.save()
                request.user.worst_case_points+=int(out_req.points)
                request.user.requests_left+=1
                request.user.save()

                in_req = IncomingRequest.objects.get(game_link=out_req.game_link)
                in_req.receiver.worst_case_points+=int(out_req.points)
                in_req.receiver.save()

                out_req.delete() 
                in_req.delete()
            except:
                pass

        elif(out_req.game_status=='accepted' and out_req.valid_until<time_now): #when accepted the game but the game isnt completed, then sender wins
            try:
                points = int(out_req.points) 
                
                in_req = IncomingRequest.objects.get(game_link=out_req.game_link)
                in_req.receiver.points-=points
                in_req.receiver.save()
                in_req.delete()

                # out_req.sender.points+=points
                # #out_req.sender.points+=2*points
                # out_req.sender.worst_case_points+=2*points
                # out_req.sender.save()
                request.user.points+=points
                request.user.worst_case_points+=2*points
                request.user.save()

                link = out_req.game_link
                out_req.delete() 

                new_status = Status.objects.create(
                    sender_name = request.user.username,
                    receiver_name = in_req.receiver.username,
                    game_link = link,
                    game_forfeited = True,
                    points = points,
                )
                new_status.save()

                

                     

                # out_req.game_status = 'You won'
                # out_req.save()
            except:
                pass


    for in_req in in_requests:
        
        if(in_req.game_status=='pending' and in_req.valid_until<time_now):
            try:
                # in_req.receiver.worst_case_points+=int(in_req.points)
                # in_req.receiver.save()
                request.user.worst_case_points+=int(in_req.points)
                request.user.save()

                out_req = OutgoingRequest.objects.get(game_link=in_req.game_link)
                out_req.sender.worst_case_points+=int(in_req.points)
                out_req.sender.requests_left+=1
                out_req.sender.save()

                out_req.delete() 
                in_req.delete()
            except:
                pass

        elif(in_req.game_status=='accepted' and in_req.valid_until<time_now):   #when accepted the game but the game isnt completed, then sender wins
            try:
                out_req = OutgoingRequest.objects.get(game_link=in_req.game_link)
                points = int(in_req.points)
                
                out_req.sender.points+=points
                out_req.sender.worst_case_points+=2*points
                out_req.sender.save()

                # in_req.receiver.points-=points
                # in_req.receiver.save()
                request.user.points-=points
                request.user.save()
                in_req.delete()

                name = out_req.sender.username
                link = out_req.game_link
                out_req.delete()
                print("deleted outgoing request")

                new_status = Status.objects.create(
                    sender_name = name,
                    receiver_name = request.user.username,
                    game_link = link,
                    game_forfeited = True,
                    points = points,
                )
                # out_req.game_status = 'You won'
                # out_req.save()
                new_status.save()
                
            except:
                pass
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
            if user.email_verified==False:
                messages.error(request, 'Email is not verified')
                return redirect('login')
        except:
            messages.error(request, 'User does not exist')
        
        
        
        user = authenticate(request, email=email, password=password , email_verified=True)

        if user is not None:
            login(request, user)
            return redirect('participant_home') 
        else:
            messages.error(request, 'Email or password does not exit') 
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
            if 'iiitb.ac.in' in user.email:
                messages.error(request, 'Please use your personal email id, preferably gmail')
            else:
                user.username = user.username.lower()
                user.email_token = str(uuid.uuid4())
                send_email_token(user.email, user.email_token)
                user.save()
                messages.success(request, f'Email has been sent to {user.email}')
        else:
            messages.error(request, 'An error occurred during registration (Ensure that you are not using the same email id or username /Check rules for password has mentioned in the registration form, this error could have been caused by that)')

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

def verify(request,token, email):
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
        sender= request.user
        if sender.admin==True:
            messages.error(request, 'Admins are not allowed to play the Game')
            return redirect('participant_home')
        
            #main game logic
        check(request)
        flag = 0
        if request.method == 'POST'  and request.POST['action']=='Make request':
            num1 = request.POST.get('num1')
            num2 = request.POST.get('num2')
            num3 = request.POST.get('num3')
            points = int(request.POST.get('points'))
            flag = 1
            if(sender.requests_left<=0):
                messages.success(request, 'Limits for sending requests reached')
            elif(sender.worst_case_points>=int(points)):
                receiver = User.objects.filter(Q(worst_case_points__gte=int(points)) & ~Q(email=sender.email) & Q(admin=False)).order_by('?').first()
                game_link = str(uuid.uuid4())
                if(receiver==None):
                    messages.error(request, 'No other user is available to play this game, Please wait until there are other acive users')
                
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
                    messages.error(request, 'You do not have enough points to play this game')
                else:
                    messages.error(request,'Calm down there! According to the worst case scenario of your pending challenges, you don’t have enough points for another challenge. Wait for the result of existing challenges to place another bet')
            return redirect('dummy')

        # out_requests = OutgoingRequest.objects.filter(Q(sender=sender) & (Q(game_status='pending')))
        out_requests = OutgoingRequest.objects.filter(sender=sender)
        in_requests = IncomingRequest.objects.filter(receiver=sender)
        in_status = Status.objects.filter(Q(receiver_name=request.user.username))
        out_status = Status.objects.filter(Q(sender_name=request.user.username))
        context = {'user':request.user, 'out_requests' : out_requests, 'in_requests' :in_requests, 'flag':flag, 'in_statuses':in_status, 'out_statuses':out_status}
        
        return render(request,'playGame.html', context)
    else:
        return redirect('login')    
    



def confirmGame(request, game_link):  #receiver plays the game
    
    if(request.user.is_authenticated):
        try:    #if out_req or in_req does not exist redirect to main page
            in_req = IncomingRequest.objects.get(game_link=game_link)
            out_req = OutgoingRequest.objects.get(game_link=game_link)
        except:
            messages.error(request,'No such game link exists, the game may have expired')
            return redirect('playGame')
        if(in_req.game_status=='accepted'):
            messages.success(request, 'Please finish the game.')
            return redirect('Game', game_link)
        
        if(in_req.game_status!='pending'):  #if game is already played
            messages.error(request,'This game has already been played')
            return redirect('playGame')
         
        user = in_req.receiver  #is the receiver
    
        if(request.user!=user and request.user.admin==False):
            messages.error(request,'You do not have access to this game link')
            return redirect('playGame')
        
        if request.method == 'POST'  and request.POST['confirm']=='accept':
            # out_req = OutgoingRequest.objects.get(game_link=game_link)
            messages.success(request,'Game request accepted')
            out_req.game_status='accepted'
            in_req.game_status='accepted'
            in_req.valid_until = datetime.now(pytz.timezone(TIME_ZONE)) + timedelta(minutes=Game_time)
            out_req.valid_until = datetime.now(pytz.timezone(TIME_ZONE)) + timedelta(minutes=Game_time)
            out_req.save()
            in_req.save()
            return redirect('Game', game_link=game_link)
        elif request.method == 'POST'  and request.POST['confirm']=='decline':
            
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


def Game(request, game_link):
    if(request.user.is_authenticated == False):
        return redirect('login')
   
    try:    #if out_req does not exist redirect to main page
        out_req = OutgoingRequest.objects.get(game_link=game_link)
        in_req = IncomingRequest.objects.get(game_link=game_link)
    except:
        messages.error(request,'No such game link exists, the game may have expired')
        return redirect('playGame')

    if(request.user!=in_req.receiver and request.user.admin==False):
        return HttpResponse("You do not have access to this Game")


    if(out_req.game_status=='pending'): #HTTP response if already played
        messages.error("Accept the game request first")
        return redirect('confirmGame', game_link=game_link)
    
    if(out_req.game_status!='accepted'):
        return HttpResponse(request,'This game has already been played')
     
    
    game_play = [i > 7 for i in [out_req.num1, out_req.num2, out_req.num3]] #true if greater than 7 else false
    sender = out_req.sender
    receiver = in_req.receiver
    points = int(in_req.points)
    
    now = datetime.now(pytz.timezone(TIME_ZONE))
    flag = now<out_req.valid_until

    
    if(not flag):
        messages.error(request,'Time limit exceeded, you have lost this game')
        sender.points+=points
        sender.worst_case_points+=2*points
        receiver.points-=points
        in_req.delete()
        out_req.delete();
        # out_req.game_status = 'You won'
        new_status = Status.objects.create(
            sender_name = out_req.sender.username,
            receiver_name = in_req.receiver.username,
            game_link = out_req.game_link,
            points = points,
            game_forfeited = True,
        )
        new_status.save()
        #out_req.save()
        sender.save()
        receiver.save()
        return redirect('playGame') #change to game playgame
    if request.method == 'POST':
        choice = request.POST.get('choice')
        choice = choice=='True'
        #setattr(in_req, 'play'+str(out_req.turn), choice)
        if(game_play[out_req.turn-1] ^ choice): #sender win
            out_req.wins+=1
            if(out_req.turn<3):
                messages.success(request,'Oops! that was incorrect, You lost this round')
        else:
            if(out_req.turn<3):
                messages.success(request,'Correct! congratulations, You won this round')
        
        if(out_req.turn==3):
            if(out_req.wins>1):
                messages.success(request,'Oh no! you guessed wrong one too many times, you lost the game')
                sender.points+=points
                sender.worst_case_points+=2*points
                receiver.points-=points     
                #out_req.game_status = 'You won'
            else:
                messages.success(request,'Your gambling addiction has finally paid off! you won the game')
                sender.points-=points
                receiver.points+=points
                receiver.worst_case_points+=2*points
                #out_req.game_status = 'You lost'
            
            # out_req.save()
            wins = out_req.wins
            sender.save()
            receiver.save()
            in_req.delete()
            out_req.delete()
            new_status = Status.objects.create(
                sender_name = sender.username,
                receiver_name = receiver.username,
                game_link = game_link,
                sender_wins = wins,
                receiver_wins = 3-wins,
                points = points,
                # num1 = out_req.num1,
                # num2 = out_req.num2,
                # num3 = out_req.num3,
                # play1 = in_req.play1,
                # play2 = in_req.play2,
                # play3 = in_req.play3,
            )
            
            print(in_req.play1, in_req.play2, in_req.play3)
            new_status.save()
            return redirect('playGame')
        
        out_req.turn+=1
        out_req.save()
        in_req.save()
        return redirect('dummygame', game_link=game_link)
    

    context = {
        'turn':out_req.turn,
        'game_link': game_link, 
        'in_req':in_req,
        'out_req':out_req,
        'wins':out_req.turn-out_req.wins-1,
        'valid_until':out_req.valid_until,
        }    
    return render(request, 'Game.html', context)




# def GameStatus(request, game_link):
#     if(request.user.is_authenticated == False):
#         return redirect('login')
    
#     try:
#         out_req = OutgoingRequest.objects.get(game_link=game_link)
#     except:
#         messages.error(request,'No such game link exists, maybe the game has expired')
#         return redirect('playGame')
#     if(out_req.game_status=='pending' or out_req.game_status=='accepted'):
#         messages.error(request,'Game is still pending')
#         return redirect('playGame')
        
#     try:
#         status = Status.objects.get(game_link=game_link)
#     except:
#         messages.error(request,'No such game link exists')
#         return redirect('playGame')
#     flag1 = status.num1>7 ^ status.play1
#     flag2 = status.num2>7 ^ status.play2
#     flag3 = status.num3>7 ^ status.play3
    
#     context = {
#         'status':status, 
#         'flag1':flag1, 
#         'flag2':flag2, 
#         'flag3':flag3,
#     }
#     return render(request, 'gameStatus.html', context)
    
    
#handling form resubmission on refresh
def dummy(request):
    return redirect('playGame')

def dummygame(request,game_link):
    return redirect('Game', game_link=game_link)