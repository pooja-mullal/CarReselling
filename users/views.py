import json
from django.shortcuts import render
from django.shortcuts import render,redirect
#from django.contrib.auth.models import NewUser,
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login ,logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import CarDetails, Booking_details, LikedCar, NewUser


def admin_login(request):
    print("hiiiii")
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            print(request.user)
            return redirect('/admin_db')
        else:
            messages.error(request,'Wrong Credentials')
            return redirect('/admin_login')
    return render(request,'admin_login.html')


@login_required(login_url="/admin_login")
def admin_db(request):
    data=NewUser.objects.filter(user_type="seller")
    return render(request,'admin_db.html',{'data':data,'name':request.user.username})

@login_required(login_url="/admin_login")
def approve_user(request, user_id):
    user = get_object_or_404(NewUser, id=user_id)

    if request.method == 'POST':
        # Update user's approve status to approved
        user.approve = 'approved'
        user.save()

        # Optionally, you can redirect to the same page after approval
        return redirect('admin_db')  # Redirect to the same page

    # If the request method is not POST (GET request or others), handle accordingly
    return render(request, 'admin_db.html', {'data': [user]})

@login_required(login_url="/admin_login")
def delete_user(request, user_id):
    user = get_object_or_404(NewUser, id=user_id)

    if request.method == 'POST':
        # Update user's approve status to approved

        user.delete()

        # Optionally, you can redirect to the same page after approval
        return redirect('admin_db')  # Redirect to the same page

    # If the request method is not POST (GET request or others), handle accordingly
    return render(request, 'admin_db.html', {'data': [user]})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def index(request):
    return render(request,'index.html')


def seller_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.user_type == "seller" and user.approve == 'approved':  # Check if the authenticated NewUser is a staff member
                login(request, user)
            # Redirect to a success page.
                return redirect('seller_db')  # Replace 'seller_db' with the name of your success URL
            else:
                error_message = "wait till account varifies"
                return render(request,'seller_login.html',{'error_message':error_message})
        else:
            # Return an 'invalid login' error message.
            error_message = "Invalid username or password."

            return render(request, 'seller_login.html',{'error_message':error_message})
    else:
        return render(request, 'seller_login.html')


def seller_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        last_name = request.POST.get('last_name')
        contact_no = request.POST.get('contact_no')
        passw = make_password(password)
        record = NewUser.objects.filter(username=username).first()
        if record:
            error_message = "User already exists"
            return render(request,'seller_registration.html',{'error_message':error_message})
        user = NewUser.objects.create(username=username,password=passw,email=email,first_name=first_name,
        contact_no=contact_no,user_type='seller')

        if user:
            return redirect('seller_login')
        # Return JSON response indicating successful registration
    return render(request, "seller_registration.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == "user" :
            login(request, user)
            # Redirect to a success page.
            return redirect('user_db')  # Replace 'NewUser_dashboard' with the name of your success URL
        else:
            # Return an 'invalid login' error message.
            error_message = "Invalid Username or password."

            return render(request, 'login.html',{'error_message':error_message})
    else:
        return render(request, 'login.html')


def registration(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        passw = make_password(password)
        record = NewUser.objects.filter(username=username).first()
        if record :
            error_message = "User already exist"
            return render(request,'registration.html',{'error_message':error_message})
        user = NewUser.objects.create(username=username,password=passw,email=email,first_name=first_name,
        contact_no=contact_no)

        if user:
            return redirect('login_view')
        # Return JSON response indicating successful registration
    return render(request, "registration.html")


@login_required(login_url="/seller_login")
def seller_db(request):
    data=CarDetails.objects.filter(user_id=request.user.id)
    return render(request,'seller_db.html',{'data':data,'name':request.user.username})


@login_required(login_url="/seller_login")
def sell_car(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        year = request.POST.get('year')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        bike = CarDetails.objects.create(
            user_id=request.user,  # Pass the NewUser instance, not the ID
            car_name=model,
            year=year,
            price=price,
            description=description,
            image=image
        )

    return render(request, 'sell_car.html',{'name':request.user.username})


@login_required(login_url="/seller_login")
def edit_car(request,id):
    data=CarDetails.objects.filter(id=id).first()
    if request.method == 'POST':
        data.car_name = request.POST.get('model')
        data.year = request.POST.get('year')
        data.price = request.POST.get('price')
        data.description = request.POST.get('description')

        data.save()
        return redirect('seller_db')

    return render(request,'edit_car.html',{'data':data,'name':request.user.username})


@login_required(login_url="/seller_login")
def delete_bike(request, bike_id):
    bike = get_object_or_404(CarDetails, id=bike_id, user_id=request.user.id)
    bike.delete()
    messages.success(request, 'Bike deleted successfully!')
    return redirect('seller_db')


@login_required(login_url="/seller_login")
def seller_booking_details(request):
    data=Booking_details.objects.select_related('car_id').filter(seller_id=request.user.id)
    return render(request,'seller_booking_details.html',{'data':data,'name':request.user.username})


def seller_logout(request):
    logout(request)
    return redirect('/')

from django.db.models import Q
@login_required(login_url="/login_view")

def user_db(request):
    query = request.GET.get('query', '')
    price = request.GET.get('price', '')

    if query or price:
        filters = Q()
        if query:
            filters |= Q(car_name__icontains=query)
        if price:
            filters |= Q(price__icontains=price)
        data = CarDetails.objects.filter(filters)
        liked_bike = LikedCar.objects.filter(user_id=request.user).values_list('bike_id', flat=True)
        for bike in data:
            bike.is_liked = bike.id in liked_bike
    else:
        data = CarDetails.objects.filter(available='True')
        liked_bike = LikedCar.objects.filter(user_id=request.user).values_list('bike_id', flat=True)
        for bike in data:
            bike.is_liked = bike.id in liked_bike

    return render(request, 'user_db.html', {'data': data, 'query': query, 'price': price})


@login_required(login_url="/login_view")
def single_car(request, id, seller_id):
    bike = get_object_or_404(CarDetails, id=id)
    user_details = NewUser.objects.get(id=request.user.id)
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')

        # Create a booking instance
        booking = Booking_details.objects.create(
            seller_id=seller_id,
            user_id=request.user,
            car_id=bike,  # Pass the Bike instance, not the ID
            name=name,
            email=email,
            phone_no=phone_no,
            address=address
        )
        success = True

    return render(request, 'single_car.html', {'data': bike, 'user_details': user_details, 'success': success})

@login_required(login_url="/login_view")

def booking_details(request):
    data=Booking_details.objects.select_related('car_id').filter(user_id=request.user.id)
    return render(request,'booking_details.html',{'data':data,'name':request.user.username})


@login_required(login_url="/login_view")
def cancel_booking(request, booking_id):
    # Assuming you have a Booking_details model with a status field
    booking = get_object_or_404(Booking_details, id=booking_id, user_id=request.user)

    booking.delete()
    return HttpResponse(json.dumps({'message': 'Booking canceled successfully'}), content_type="application/json")


def user_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/seller_login")
def confirm_booking(request, booking_id, bike_id):
    booking = get_object_or_404(Booking_details, id=booking_id)
    bike = get_object_or_404(CarDetails, id=bike_id)

    if request.method == 'POST':
        # Update booking status to confirmed

        booking.status = 'confirmed'
        booking.save()
        bike.available='False'
        bike.save()
        # Optionally, you can redirect to a different page after confirmation
        return redirect('seller_booking_details')


def like_car(request):
    if request.method == 'POST':
        bike_id = request.POST.get('bike_id')
        bike = CarDetails.objects.get(id=bike_id)
        like, created = LikedCar.objects.get_or_create(user_id=request.user, bike_id=bike)
        if created:
            return JsonResponse({'status': 'liked'})
        else:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


def unlike_car(request):
    if request.method == 'POST':
        bike_id = request.POST.get('bike_id')
        bike = CarDetails.objects.get(id=bike_id)
        LikedCar.objects.filter(user_id=request.user, bike_id=bike).delete()
        return JsonResponse({'status': 'unliked'})
    return JsonResponse({'status': 'error'})


def liked_car(request):
    user_id = request.user.id
    liked_bikes = LikedCar.objects.select_related('bike_id').filter(user_id=user_id)
    bikes = [like.bike_id for like in liked_bikes]

    for bike in bikes:
        bike.is_liked = True

    context = {'data': bikes}
    return render(request, 'liked_bike.html', context)

def profile(request):
    return render(request,'profile.html')
