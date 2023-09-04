from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from rest_auth.registration.views import VerifyEmailView

from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from django.contrib.auth import views as auth_views
from Gestão import views, apis

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
     #####################################################
    path('signup/driver/', apis.DriverSignupView.as_view()),
    path('signup/', apis.CustomerSignupView.as_view()),
    path('fornecedor/', apis.fornecedor_sign_up),
    path('login/',apis.CustomAuthToken.as_view(), name='auth-token'),
    path('logout/', apis.LogoutView.as_view(), name='logout-view'),
    ##############################################

    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')), # new
    path('api/v1/rest-auth/registration/', # new
            include('rest_auth.registration.urls')),

    path('restaurant/sign-in/', auth_views.LoginView.as_view(), {'template_name': 'restaurant/sign_in.html'}, name = 'restaurant-sign-in'),
    path('restaurant/sign-out/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name = 'restaurant-sign-out'),
    path('restaurant/', views.restaurant_home, name='restaurant-home'),
    path('restaurant/sign-up/', views.restaurant_sign_up, name='restaurant-sign-up'),

    path('restaurant/', views.restaurant_home, name='restaurant-home'),
    path('restaurant/account/',
        views.restaurant_account,
        name='restaurant-account'),

    # Restaurant CRUD operations on Meals
    path('restaurant/meal/', views.restaurant_meal, name='restaurant-meal'),
    path('restaurant/meal/add/',
        views.restaurant_add_meal,
        name='restaurant-add-meal'),

    url(r'^restaurant/meal/edit/(?P<meal_id>\d+)/$',
        views.restaurant_edit_meal,
        name='restaurant-edit-meal'),

    path('restaurant/order/',
        views.restaurant_order,
        name='restaurant-order'),

    path('restaurant/report/',
        views.restaurant_report,
        name='restaurant-report'),
    path('restaurant/customers/',
        views.restaurant_customers,
        name='restaurant-customers'),
    path('restaurant/drivers/',
        views.restaurant_drivers,
        name='restaurant-drivers'),


    # Sign In/ Sign Up/ Sign Out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/restaurant/order/notification/(?P<last_request_time>.+)/$',
        apis.restaurant_order_notification),

    # REST API to be used with android mobile front ends

    url(r'^api/customer/restaurants/$', apis.customer_get_restaurants),
    url(r'^api/customer/meals/(?P<restaurant_id>\d+)/$',
        apis.customer_get_meals),
    url(r'^api/customer/order/add/$', apis.customer_add_order),
    url(r'^api/customer/order/latest/$', apis.customer_get_latest_order),
    url(r'^api/customer/driver/location/$', apis.customer_driver_location),
    url(r'^api/customer/order/history/$', apis.customer_get_order_history),
    url(r'^api/customer/profile/update/$', apis.customer_update_profile),
    url(r'^api/customer/profile/$', apis.customer_get_detais),

    # APIs for DRIVERS
    url(r'^api/driver/orders/ready/$', apis.driver_get_ready_orders),
    url(r'^api/driver/order/pick/$', apis.driver_pick_order),
    url(r'^api/driver/order/latest/$', apis.driver_get_latest_order),
    url(r'^api/driver/order/complete/$', apis.driver_complete_order),
    url(r'^api/driver/revenue/$', apis.driver_get_revenue),
    url(r'^api/driver/location/update/$', apis.driver_update_location),
    url(r'^api/driver/profile/update/$', apis.driver_update_profile),
    url(r'^api/driver/profile/view/$', apis.driver_get_profile),
    url(r'^api/driver/order/history/$', apis.driver_get_order_history),
    url(r'^api/driver/profile/$', apis.driver_get_detais),


]

#urlpatterns += accounts_urlpatterns # add URLs for authentication


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

