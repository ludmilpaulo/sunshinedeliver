from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import time, date, datetime

from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail


##########################################################################
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message


def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()



####################################################################################

class User(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_driver=models.BooleanField(default=False)

    def __str__(self) :
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

####################################################################################

class ImageField(models.ImageField):
    def value_to_string(self, obj): # obj is Model instance, in this case, obj is 'Class'
        return obj.avatar.url # not return self.url


#######################################################################################
class Category(models.Model):
       name = models.CharField(max_length=200,
                               db_index=True)
       slug = models.SlugField(max_length=200,
                               unique=True)
       class Meta:
           ordering = ('name',)
           verbose_name = 'category'
           verbose_name_plural = 'categories'
       def __str__(self):
           return self.name



class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário',blank=True)
    name = models.CharField(max_length=500, verbose_name='Nome do restaurante')
    phone = models.CharField(max_length=500, verbose_name='Telefone do restaurante')
    address = models.CharField(max_length=500, verbose_name='Endereço do restaurante')
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False, verbose_name='Logotipo do restaurante')
    restaurant_license = models.FileField(upload_to='vendor/license', blank=True, verbose_name='Licenca do restaurante')
    is_approved = models.BooleanField(default=False)



	
    def __str__(self):
        return self.name
    
    def is_open(self):
        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(restaurant=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Restaurant.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = "Parabéns! Seu restaurante foi aprovado."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "Nós lamentamos! Você não está qualificado para publicar seu cardápio de comida em nosso mercado."
                    send_notification(mail_subject, mail_template, context)
        return super(Restaurant, self).save(*args, **kwargs)
    
  



DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('restaurant', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()



class Customer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='customer', verbose_name='usuário')
    avatar = models.ImageField(upload_to='customer/', blank=True)
    phone = models.CharField(max_length=500, blank=True, verbose_name='telefone')
    address = models.CharField(max_length=500, blank=True, verbose_name='Endereço')

    class Meta:
        verbose_name ='Cliente'
        verbose_name_plural ='Clientes'

    def __str__(self):
        return self.user.get_username()






class Driver(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='driver', verbose_name='Utilizador')
    avatar = models.ImageField(upload_to='driver/', blank=True)
    phone = models.CharField(max_length=500, blank=True, verbose_name='telefone')
    address = models.CharField(max_length=500, blank=True, verbose_name='Endereço')
    location = models.CharField(max_length=500, blank=True, verbose_name='localização')

    class Meta:
        verbose_name ='Motorista'
        verbose_name_plural ='Motoristas'


    def __str__(self):
        return self.user.get_username()





class Meal(models.Model):
    category = models.ForeignKey(Category,
                                    related_name='meal',
                                    on_delete=models.CASCADE,
                                    null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restaurante')
    name = models.CharField(max_length=500, verbose_name='Nome')
    short_description = models.CharField(max_length=500, verbose_name='Pequena descrição')
    image = models.ImageField(upload_to='meal_images/', blank=False)
    price = models.IntegerField(default=0, verbose_name='preço')
    quantity = models.IntegerField(default=1, blank=True)

    class Meta:
        verbose_name ='Refeição'
        verbose_name_plural ='Refeições'

    def __str__(self):
        return self.name






class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cozinhando"),
        (READY, "Pedido Pronto"),
        (ONTHEWAY, "A caminho"),
        (DELIVERED, "Entregue"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='cliente')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='restaurante')
    driver = models.ForeignKey(Driver, blank=True, null=True, on_delete=models.CASCADE, verbose_name='motorista')  # can be blank
    address = models.CharField(max_length=500, verbose_name='Endereco')
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name='stado')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='criado em')
    picked_at = models.DateTimeField(blank=True, null=True, verbose_name='pegar em')


    class Meta:
        verbose_name ='Pedido'
        verbose_name_plural ='Pedidos'

    def __str__(self):
        return str(self.id)






class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE, verbose_name='Pedido')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name='Refeição')
    quantity = models.IntegerField(verbose_name='Quantidade')
    sub_total = models.IntegerField()

    class Meta:
        verbose_name ='Detalhe do pedido'
        verbose_name_plural ='Detalhes dos pedidos'



    def __str__(self):
        return str(self.id)



