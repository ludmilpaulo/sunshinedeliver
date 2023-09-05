import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .permissions import *

from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.parsers import *
from rest_framework import serializers


from .models import Restaurant, Meal, Order, OrderDetails
from .serializers import *

import stripe
from sunshinedelivery.settings import STRIPE_API_KEY

from django.contrib.auth import get_user_model
User = get_user_model()



AccessToken = Token

class DriverSignupView(generics.GenericAPIView):
    serializer_class=DriverSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            'user_id':user.pk,
            "message":"Conta criada com sucesso",
            'username':user.username,
            "status":"201"
        })


class CustomerSignupView(generics.GenericAPIView):
    serializer_class=CustomerSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            'user_id':user.pk,
            "message":"Conta criada com sucesso",
            'username':user.username,
            "status":"201"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'username':user.username,
            'message':"Login com sucesso",
            'is_customer':user.is_customer
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class CustomerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsCustomerUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user

class DriverOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsDriverUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
###############################*************************************

# class UserUpdate(generics.UpdateAPIView):
#     """
#     Update user.
#     """
#     parser_class = (FileUploadParser,)
#     permission_classes = (AllowAny,)
#     queryset = Customer.objects.all()
#     serializer_class = UserUpdateSerializer

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.user_id = request.data.get("user_id")
#         instance.save()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)


############################################################

###**********************************************************

####################################################
# CUSTOMERS
####################################################

@api_view(["POST"])
@parser_classes([JSONParser, MultiPartParser, FormParser, FileUploadParser])
def customer_update_profile(request, format=None):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    customer = Customer.objects.get(user=access)

    # Set location string => database
    customer.avatar = request.FILES.get('avatar')
    #driver.avatar = data['avatar']
    customer.phone = data["phone"]
    customer.address = data["address"]
    customer.save()

    customer_user = User.objects.get(username=access)
    customer_user.first_name = data["first_name"]
    customer_user.last_name = data["last_name"]
    customer_user.save()

    return JsonResponse({"status": "Os Seus Dados enviados com sucesso"})



def customer_get_restaurants(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many=True,
        context={
            "request": request
        }).data

    return JsonResponse({"restaurants": restaurants})


def customer_get_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id=restaurant_id).order_by("-id"),
        many=True,
        context={
            "request": request
        }).data

    return JsonResponse({"meals": meals})


#######################################################################################3

@api_view(['POST'])
def customer_get_detais(request):
    data = request.data

    customer_detais = CustomerSerializer(
         Customer.objects.get(user_id=data['user_id'])).data
     

    return JsonResponse({"customer_detais": customer_detais})

##################################################################
#@csrf_exempt
@api_view(['POST'])
def customer_add_order(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)


    if Order.objects.filter(customer=customer).exclude(
            status=Order.DELIVERED):
        return JsonResponse({
            "error": "failed",
            "status": "Seu último pedido deve ser entregue para Pedir Outro."
        })

    # Check Address
    if not data['address']:
        return JsonResponse({
            "status": "failed",
            "error": "Address is required."
        })

    # Get Order Details

    order_details = data["order_details"]


    order_total = 0
    for meal in order_details:
        order_total += Meal.objects.get(
            id=meal["meal_id"]).price * meal["quantity"]

    if len(order_details) > 0:

            # Step 2 - Create an Order
            order = Order.objects.create(
                customer=customer,
                restaurant_id=data["restaurant_id"],
                total=order_total,
                status=Order.COOKING,
                address=data["address"])

            # Step 3 - Create Order details
            for meal in order_details:
                OrderDetails.objects.create(
                    order=order,
                    meal_id=meal["meal_id"],
                    quantity=meal["quantity"],
                    sub_total=Meal.objects.get(id=meal["meal_id"]).price *
                    meal["quantity"])
            #serializer = OrderSerializer(order, many=False)
            return JsonResponse({"status": "success"})
    else:
        return JsonResponse({
            "status": "failed",
            "error": "Failed connect to Stripe."
        })



##############################################################


@api_view(["POST"])
def customer_get_latest_order(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    order = OrderSerializer(
        Order.objects.filter(customer=customer).last()).data

    return JsonResponse({"order": order})

@api_view(["POST"])
def customer_driver_location(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    current_order = Order.objects.filter(customer=customer,
                                         status=Order.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})


# GET params: access_token
@api_view(["POST"])
def customer_get_order_history(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    # Get profile

    customer = Customer.objects.get(user=access)
    order_history = OrderSerializer(Order.objects.filter(
        customer=customer, status=Order.DELIVERED).order_by("picked_at"),
                                    many=True,
                                    context={
                                        "request": request
                                    }).data

    return JsonResponse({"order_history": order_history})


####################################################
# RESTAURANTS
####################################################
# get a list of order notifications made AFTER last_request_time for restaurant
def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(
        restaurant=request.user.restaurant,
        created_at__gt=last_request_time).count()

    return JsonResponse({"notification": notification})


####################################################
# DRIVERS
####################################################
@api_view(['GET'])
def driver_get_ready_orders(request):
    orders = OrderSerializer(Order.objects.filter(status=Order.READY,
                                                  driver=None).order_by("-id"),
                             many=True).data

    return JsonResponse({"orders": orders})


@api_view(['POST'])
# params: access_token, order_id
def driver_pick_order(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

     # Get profile

    driver = Driver.objects.get(user=access)

    # Check if driver can only pick up one order at the same time
    if Order.objects.filter(driver=driver).exclude(status=Order.DELIVERED):
        return JsonResponse({
            "status":"failed",
            "error": "Você só pode pegar outros pedidos depois de entregar o pedido anterior"
        })

    try:
        order = Order.objects.get(id=data["order_id"],
                                  driver=None,
                                  status=Order.READY)
        order.driver = driver
        order.status = Order.ONTHEWAY
        order.picked_at = timezone.now()
        order.save()

        return JsonResponse({"status": "Ótimo, por favor, você tem no máximo 20 minutos para concluir esta entrega"})

    except Order.DoesNotExist:
        return JsonResponse({
            "status":
            "failed",
            "error":
            "Este pedido foi retirado por outro."
        })

    return JsonResponse({})


# GET params: access_token
@api_view(['POST'])
def driver_get_latest_order(request):
    # Get token
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

     # Get profile

    driver = Driver.objects.get(user=access)

    order = OrderSerializer(
        Order.objects.filter(driver=driver).order_by("picked_at").last()).data

    return JsonResponse({"order": order})


# POST params: access_token, order_id
@api_view(['POST'])
def driver_complete_order(request):
    # Get token
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    driver = Driver.objects.get(user=access)

    order = Order.objects.get(id=data["order_id"], driver=driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})

@api_view(["POST"])
# GET params: access_token
def driver_get_revenue(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    driver = Driver.objects.get(user=access)

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [
        today + timedelta(days=i)
        for i in range(0 - today.weekday(), 7 - today.weekday())
    ]

    for day in current_weekdays:
        orders = Order.objects.filter(driver=driver,
                                      status=Order.DELIVERED,
                                      created_at__year=day.year,
                                      created_at__month=day.month,
                                      created_at__day=day.day)

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})


# POST - params: access_token, "lat,lng"
@api_view(["POST"])
def driver_update_location(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    driver = Driver.objects.get(user=access)

    # Set location string => database
    driver.location = data["location"]
    driver.save()

    return JsonResponse({"status": "Driver location successfully sent"})


# GET params: access_token
@api_view(["POST"])
def driver_get_order_history(request):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    driver = Driver.objects.get(user=access)


    order_history = OrderSerializer(Order.objects.filter(
        driver=driver, status=Order.DELIVERED).order_by("picked_at"),
                                    many=True,
                                    context={
                                        "request": request
                                    }).data

    return JsonResponse({"order_history": order_history})


@api_view(['POST'])
def driver_get_detais(request):
    data = request.data

    customer_detais = DriverSerializer(
         Driver.objects.get(user_id=data['user_id'])).data
     

    return JsonResponse({"customer_detais": customer_detais})







@api_view(["POST"])
@parser_classes([JSONParser, MultiPartParser, FormParser, FileUploadParser])
def driver_update_profile(request, format=None):
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

    driver = Driver.objects.get(user=access)

    # Set location string => database
    driver.avatar = request.FILES.get('avatar')
    #driver.avatar = data['avatar']
    driver.phone = data["phone"]
    driver.address = data["address"]
    driver.save()

    driver_user = User.objects.get(username=access)
    driver_user.first_name = data["first_name"]
    driver_user.last_name = data["last_name"]
    driver_user.save()

    return JsonResponse({"status": "Os Seus Dados enviados com sucesso"})




@api_view(["POST"])
def driver_get_profile(request):
     # Get token
    data = request.data
    access = Token.objects.get(key=data['access_token']).user

     # Get profile

    driver = Driver.objects.get(user=access)

    order = OrderDriverSerializer(
        Driver.objects.filter(user=driver).order_by("-id")).data

    return JsonResponse({"order": order})


##########################################################################################################
from rest_framework.response import Response
from rest_framework import status

# ...

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def fornecedor_sign_up(request, format=None):
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Nome de usuário e senha são necessários."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "O nome de usuário já existe."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the User object
        new_user = User.objects.create_user(username=username, password=password, email=email)

        # Handle uploaded files
        logo = request.FILES.get('logo', None)
        licenca = request.FILES.get('restaurant_license', None)
        if logo:
            request.data['logo'] = logo
        if licenca:
            request.data['restaurant_license'] = licenca

        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            # Create the Restaurant object with the user field set
            serializer.validated_data['user'] = new_user
            restaurant = serializer.save()

            # Serialize the Restaurant object into a dictionary
            restaurant_data = RestaurantSerializer(restaurant).data

            # Authenticate the user after saving the data
            user = authenticate(username=username, password=password)
            if user is not None:
                return Response({
                    "token": Token.objects.get(user=user).key,
                    'user_id': user.pk,
                    "message": "Conta criada com sucesso",
                    "fornecedor_id": restaurant_data,  # Include the serialized restaurant data
                    'username': user.username,
                    "status": "201"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Falha na autenticação."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








