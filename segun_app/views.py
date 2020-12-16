from django.shortcuts import render, redirect
from django.urls import reverse
import stripe
from .models import rate
from .forms import UserRegisterForm
from django.views.generic import CreateView
from django.views.generic import View
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import kycinfo
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView



stripe.api_key = "sk_test_51Hv5SxJXt3VVluZYBA3Yzh0WkSYQEygc4XzjkYbHpqc0am6FT8QzkXMWyJeDOIUNsZDfDNJwlmiCaOocEySZw3rf00g1SYZq8u"


# 'cherry0269boo@gmail.com'
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            mail = form.cleaned_data.get('email')
            form.save()

            userr = User.objects.get(username=username)
            print(userr)

            uidb64 = urlsafe_base64_encode(force_bytes(userr.pk))

            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(userr)})
            activate_url = 'http://'+domain+link
            email_subject = 'Activate your account'
            email_body = 'Hello {0} thanks for signing up with us, please use this link to verify your account \n {1}'.format(username, activate_url)

            email = send_mail(email_subject, email_body, 'Noreply@FX.com', [mail])
            messages.success(request, f'Congrats {username}, Your account was created successfully')

            return redirect('verify')
    else:
        form = UserRegisterForm()
    return render(request, 'segun_app/register.html', {'form': form})

def verify_mail(request):
    return render(request, 'segun_app/verify_mail.html')


def home(request):
    try:
        kyc = kycinfo.objects.get(id = request.user.id)
        print(kyc)
    except Exception as e:
        return redirect(reverse('uploadKyc', args=[request.user.id]))
    
    context = {
        'kyc': kyc
    }
    
    return render(request, 'segun_app/home.html')   #return redirect(reverse('success', args=[amount]))


@login_required
def transaction(request):
    return render(request, 'segun_app/transaction.html')

class verification(View):
    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message'+'User already activated')
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account actvated successfully')
            return redirect('login')
        except Exception as e:
            pass
        return redirect('login')


@login_required
def charge(request):
    query = rate.objects.get(id=1)
    val = query.exchange_rate
    total = 100 * val
    amount = int(request.POST['amount'])
    if request.method == 'POST':
        print('Date:', request.POST)

        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['name'],
            source=request.POST['stripeToken']
        )
        charges = stripe.Charge.create(
            customer=customer,
            amount=amount*total,
            currency='ngn',
            description='Exchanges'
        )

    return redirect(reverse('success', args=[amount]))

def successmsg(request, args):
    amount = args
    context = {
        'amount': amount
    }
    return render(request, 'segun_app/success.html', context)


def email_success(request):
    messages.success(request, 'Mail Verification Successful...')
    return render(request, 'segun_app/Email_success.html')



class createKycinfo(CreateView):
    model = kycinfo
    template_name = 'segun_app/upkyc.html'
    fields = ['name','home_address', 'personal_ids', 'dob']
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        form.instance.Link = self.request.user
        return super().form_valid(form)

def kyc_msg(request, user_id):
    user = User.objects.get(id = user_id)
    messages.error(request, f'KYC data has not been provides for {user.username},  an email would be sent to them to do so immediately...')
    return render(request, 'segun_app/kycmessge.html')

@login_required
def kyc_detail(request, user_id):
    try:
        user_kyc = kycinfo.objects.get(pk = user_id)
        user = User.objects.get(pk = user_id)
    except Exception as e:
        return redirect(reverse('kyc-msg', args=[user_id]))
 
    
   # checkin = User.kycinfo_set.get(pk = user_id)
    #print(checkin)

    context = {'user': user, 'user_kyc': user_kyc}
    return render(request, 'segun_app/viewKyc.html', context)






# Create your views here.
