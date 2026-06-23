from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns=[
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_db',views.admin_db,name="admin_db"),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('',views.index,name="index"),
    path('seller_registration',views.seller_registration,name='seller_registration'),
    path('seller_login',views.seller_login,name='seller_login'),
    path('approve_user/<int:user_id>',views.approve_user,name='approve_user'),
    path('delete_user/<int:user_id>',views.delete_user,name='delete_user'),
    path('login_view',views.login_view,name='login_view'),
    path('registration',views.registration,name='registration'),
    path('seller_db',views.seller_db,name='seller_db'),
    path('sell_car',views.sell_car,name='sell_car'),
    path('edit_car/<int:id>',views.edit_car,name='edit_car'),
    path('delete_bike/<int:bike_id>/', views.delete_bike, name='delete_bike'),
    path('seller_booking_details',views.seller_booking_details,name='seller_booking_details'),
    path('seller_logout',views.seller_logout,name='seller_logout'),
    path('user_db',views.user_db,name='user_db'),
    path('single_car/<int:id>/<int:seller_id>',views.single_car,name='single_car'),
    path('booking_details',views.booking_details,name='booking_details'),
    path('cancel_booking/<int:booking_id>/',views.cancel_booking,name='cancel_booking'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('confirm/<int:booking_id>/<int:bike_id>', views.confirm_booking, name='confirm_booking'),
    path('liked_car', views.liked_car, name='liked_car'),
    path('like_car/',views.like_car,name='like_car'),
    path('unlike_car/', views.unlike_car, name='unlike_car'),
    path('profile/', views.profile, name='profile'),
]
