from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from .models import Profile,FoodEntry,completed




def adminhis(request):
    query = '''
        SELECT foodwasteapp_completed.id as id, foodwasteapp_completed.userr as userr,foodwasteapp_completed.food_name as food_name, foodwasteapp_completed.address as address, foodwasteapp_profile.mobile_number as mobile_number,  foodwasteapp_completed.link as link
        FROM auth_user 
        INNER JOIN foodwasteapp_profile ON auth_user.id = foodwasteapp_profile.user_id 
        INNER JOIN foodwasteapp_completed ON auth_user.username = foodwasteapp_completed.userr
    '''
    data = Profile.objects.raw(query)
    for x in data:
        print(x)
    return render(request, 'adminhis.html', {'data': data})



def complete(request,id):
    if id:
        user=request.user
        data = FoodEntry.objects.get(id = id)
        completed.objects.create(
            food_name = data.food_name,
            date = data.date,
            address = data.address,
            link = data.link,
            userr = data.userr,
            source = data.source,
            ruser = user
        )
        data.delete()
        return redirect('/foodrequest')
    return render(request,'complete.html')


def orders(request):
    user=request.user
    query = 'SELECT foodwasteapp_foodentry.id as id, foodwasteapp_foodentry.userr as userr, ' \
        'foodwasteapp_foodentry.food_name as food_name, foodwasteapp_foodentry.address as address, ' \
        'foodwasteapp_profile.mobile_number as mobile_number, foodwasteapp_foodentry.link as link, ' \
        'foodwasteapp_foodentry.source as source ' \
        'FROM auth_user ' \
        'INNER JOIN foodwasteapp_profile ON auth_user.id = foodwasteapp_profile.user_id ' \
        'INNER JOIN foodwasteapp_foodentry ON auth_user.username = foodwasteapp_foodentry.userr ' \
        'WHERE foodwasteapp_foodentry.userr != %s'
    data = Profile.objects.raw(query, [user])
    return render(request, 'order.html', {'data': data})




def history(request):
    user=request.user
    data = completed.objects.filter(userr=user)
    return render(request,'history.html',{'data':data})


def request(request):
    user=request.user
    data = FoodEntry.objects.filter(userr=user)
    return render(request,'request.html',{'data':data})


def donate(request):
    user=request.user
    if request.method == 'POST':
        food_name = request.POST.get('name')
        source = request.POST.get('source')
        date = request.POST.get('date')
        address = request.POST.get('address')
        link = request.POST.get('link')

        FoodEntry.objects.create(
            food_name=food_name,
            date=date,
            address=address,
            link=link,
            userr = user,
            source = source
        )
        
        return redirect('/user')
    return render(request,'donate.html')

def index(request):
    return render(request,'index.html')

def useradmin(request):
    return render(request,'useradmin.html')

def user(request):
    return render(request,'userportal.html')

def logout_req(request):
    logout(request)
    return redirect('/') 



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile_number')
        hotel_name = request.POST.get('hotel_name')
        location = request.POST.get('location')
        address = request.POST.get('address')
        designation = request.POST.get('designation')
        if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(
                    user=user,
                    mobile_number=mobile_number,
                    hotel_name=hotel_name,
                    location=location,
                    stored_password=password,   
                    address = address,
                    designation = designation        
                )

                return redirect('/login')  
        else:
            error = 'User name is already exist why can you try with differnt user names? 😉'
            return render(request,'signup.html',{'error':error})  
        
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                designation = profile.designation
                print(designation)
                if designation == 'user':
                    return redirect('/user')
                else:
                    return redirect('/useradmin')  
            except Profile.DoesNotExist:
                return redirect('/useradmin/')  
        else:
            error = 'Invalid username or password'
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')
