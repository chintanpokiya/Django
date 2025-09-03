# event/views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import RegistrationForm, LoginForm, ProfileForm
from .models import Category, Photo  , Profile,Contact
from django.db import transaction
import random, string
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cruds.models import Becholer,Wedding,Reception
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from cruds.models import Becholer,Wedding,Reception
from addmin.views import chart_order
from django.conf import settings
from .forms import PasswordResetForm,ContactForm
from django.views.generic import ListView

class ViewPDF(View):
    def get(self, request, order_type, order_id, *args, **kwargs):
        # Fetch the order based on type and ID
        if order_type == 'becholer':
            order = Becholer.objects.get(oid=order_id, user=request.user)
        elif order_type == 'wedding':
            order = Wedding.objects.get(oid=order_id, user=request.user)
        elif order_type == 'reception':
            order = Reception.objects.get(oid=order_id, user=request.user)
        else:
            return HttpResponse("Invalid order type", status=400)

        # Prepare context for rendering the PDF
        context = {
            'order': order,
            'order_type': order_type,
            # Add any additional details needed for the PDF
        }
        
        pdf = render_to_pdf('event/pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    
class DownloadPDF(View):
    def get(self, request, order_type, order_id, *args, **kwargs):
        # Fetch the order based on type and ID
        if order_type == 'becholer':
            order = Becholer.objects.get(oid=order_id, user=request.user)
        elif order_type == 'wedding':
            order = Wedding.objects.get(oid=order_id, user=request.user)
        elif order_type == 'reception':
            order = Reception.objects.get(oid=order_id, user=request.user)
        else:
            return HttpResponse("Invalid order type", status=400)

        # Prepare context for rendering the PDF
        context = {
            'order': order,
            'order_type': order_type,
            # Add any additional details needed for the PDF
        }
        
        pdf = render_to_pdf('event/pdf_template.html', context)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{order_type}_{order_id}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None

@login_required(login_url='/login/')
def viewplotw(request):
    return render(request,"event/wedpartyplot.html")

@login_required(login_url='/login/')
def becholertheme(request):
    return render(request,"event/becholertheme.html")

@login_required(login_url='/login/')
def receptiondest(request):
    return render(request,"event/receptiondest.html")

def send_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        guest = request.POST.get('guest')
        event = request.POST.get('event')
        message = request.POST.get('message')

        # Prepare the email content
        subject = f"Feedback from {name}"
        body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Number of Guests: {guest}\n"
            f"Event: {event}\n"
            f"Message: {message}"
        )
        admin_email = settings.ADMIN_EMAIL  # The admin's email defined in settings.py

        # Send email to admin
        try:
            send_mail(
                subject,
                body,
                email,  # From email
                [admin_email],  # To email
                fail_silently=False,
            )
            return HttpResponse("Thank you for your feedback!")  # Success response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")  # Error handling

    return HttpResponse("Invalid request.")

@login_required(login_url='/login/')
def my_protected_view(request):
    return render(request, 'myproject\templates\event\index.html')

@transaction.atomic
def generate_otp(length=6):
    digits = string.digits
    otp = ''.join(random.choices(digits, k=length))
    return otp


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                otp = generate_otp()
                send_mail(
                    "Your Registration OTP",
                    f"Thank you for registering. Your OTP is {otp}.",
                    'your_email@example.com',
                    [form.cleaned_data['email']]
                )
                request.session['otp'] = otp
                request.session['user_id'] = user.id
                return redirect('verify_otp')
            except Exception as e:
                transaction.set_rollback(True)
                return render(request, "event/error.html", {"error": str(e)})
    else:
        form = RegistrationForm()
    return render(request, "event/register.html", {"form": form})


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp'):
            user_id = request.session.get('user_id')
            del request.session['otp']
            del request.session['user_id']
            return redirect('/')
        else:
            return render(request, 'event/verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'event/verify_otp.html')




def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if the username and password are both "admin"
            if username == 'admin' and password == 'admin':
                return redirect('add-index')  # Redirect to admin page if both are "admin"

            # Authenticate for regular users
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('/')
    else:
        form = LoginForm()

    return render(request, "event/login.html", {'form': form})


def admin_login(request):
    return render(request, "addmin/addmin-index.html")

def contact(request):
    return render(request, "event/Contact.html")


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('/')

def index(request):
    if request.user.is_authenticated:
        # Retrieve photos of the current user
        photos = Photo.objects.filter(category__user=request.user)
    else:
        # Retrieve all photos for unauthenticated users
        photos = Photo.objects.all()

    context = {'photos': photos}
    return render(request, 'event/index.html', context)


def usershow(request):
    obj=User.objects.all() 
    return render(request,"event/usershow.html",{'obj':obj})

def userDelete(request, f_username):
    obj = User.objects.get(username=f_username)
    form = RegistrationForm(instance=obj)
    if request.method == 'GET':
        obj.delete()
        return redirect('usershow')
    return render(request, "event/usershow.html", {'form':form})


# Use addmin models to display categories and photos
def gallery(request):
    user = request.user
    category_name = request.GET.get('category')

    if user.is_authenticated:
        if category_name:
            photos = Photo.objects.filter(category__name=category_name, category__user=user)
        else:
            photos = Photo.objects.filter(category__user=user)
        categories = Category.objects.filter(user=user)
    else:
        # Show all public categories/photos for anonymous users
        if category_name:
            photos = Photo.objects.filter(category__name=category_name)
        else:
            photos = Photo.objects.all()
        categories = Category.objects.filter(user__isnull=True)  # Categories with no specific user assigned

    context = {'categories': categories, 'photos': photos}
    return render(request, 'event/gallery.html', context)


def delete_photo(request, photo_id):
    # Get the photo by ID or return a 404 if it doesn't exist
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        # Delete the photo
        photo.delete()
        # Redirect back to the gallery (or any page you want)
        return redirect('gallery')

    # In case someone accesses this view via GET, redirect to the gallery
    return redirect('gallery')

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('gallery') 

# def viewPhoto(request):
#     photo = Photo.objects.get()
#     return render(request, 'event/photo.html', {'photo': photo})


# Add new photos to the gallery
def addPhoto(request):
    user = request.user
    categories = user.category_set.all() if user.is_authenticated else Category.objects.filter(user__isnull=True)

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        # Get category if existing, otherwise create new
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user if user.is_authenticated else None,
                name=data['category_new']
            )
        else:
            category = None

        # Save all uploaded images
        for image in images:
            Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'event/add.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session with new password
            messages.success(request, "Your password was successfully updated!")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'event/changepassword.html', {'form': form})



def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                # Logic to generate a password reset token and send the email
                # You can use Django's built-in password reset functionality here
                send_mail(
                    'Password Reset Request',
                    'Please click the link below to reset your password.',
                    'from@example.com',  # Replace with your sender email
                    [user.email],  # Assuming user has an email field
                    fail_silently=False,
                )
                return redirect('password_reset_done')  # Redirect to a success page
            except User.DoesNotExist:
                form.add_error('username', 'No user found with this username.')
    else:
        form = PasswordResetForm()
    return render(request, "event/password_reset.html", {'form': form})



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if form:
                return redirect('userprofile')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'event/profile.html', {'form': form})

@login_required
def userprofile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Fetch the services the user has ordered
    becholer_orders = Becholer.objects.filter(user=request.user)
    wedding_orders = Wedding.objects.filter(user=request.user)
    reception_orders = Reception.objects.filter(user=request.user)
    
    # Check if the profile is incomplete (e.g., required fields like mobile, address)
    profile_incomplete = not all([
        profile.image,
        profile.mobile,
        profile.address,
        profile.city,
        profile.state,
        profile.zipcode
    ])
    
    return render(request, 'event/userprofile.html', {
        'profile_incomplete': profile_incomplete,
        'profile': profile,
        'becholer_orders': becholer_orders,
        'wedding_orders': wedding_orders,
        'reception_orders': reception_orders
    })



def complete_order(request, order_type, order_id):
    if order_type == 'bachelor':
        order = get_object_or_404(Becholer, oid=order_id)
    elif order_type == 'wedding':
        order = get_object_or_404(Wedding, oid=order_id)
    elif order_type == 'reception':
        order = get_object_or_404(Reception, oid=order_id)

    if order:
        # Update the order status to "Completed"
        order.status = 'Completed'
        order.invoice_sent = True
        order.save()

        # Set the email message based on the order type
        message = ""
        if order_type == 'bachelor':
            message = f"Dear {order.fname}, your bachelor party order is completed. Please download your invoice using the following link: {request.build_absolute_uri(reverse('pdf_download', args=[order_type, order.oid]))}"
        elif order_type == 'wedding':
            message = f"Dear {order.gname}, your wedding order is completed. Please download your invoice using the following link: {request.build_absolute_uri(reverse('pdf_download', args=[order_type, order.oid]))}"
        elif order_type == 'reception':
            message = f"Dear {order.gname}, your reception order is completed. Please download your invoice using the following link: {request.build_absolute_uri(reverse('pdf_download', args=[order_type, order.oid]))}"

        # Send the email
        send_mail(
            subject="Your Order Invoice",
            message=message,
            from_email="krinspatel583@gmail.com",
            recipient_list=[order.user.email],
            fail_silently=False,
        )


    if order_type == 'bachelor':
        return HttpResponseRedirect(reverse('bechshow'))
    elif order_type == 'wedding':
        return HttpResponseRedirect(reverse('wedshow'))
    elif order_type == 'reception':
        return HttpResponseRedirect(reverse('recshow'))



def showcall(request):
    obj = Contact.objects.all()
    return render(request, "event/showcall.html", {'obj': obj})

class CallSearchView(ListView):
    model = Contact
    template_name = 'event/showcall.html'
    context_object_name = 'obj'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Contact.objects.filter(contact_number__icontains=query).order_by('contact_number')
    

def sendmail(request, email):
    # Retrieve the specific Contact object using the provided email
    order = get_object_or_404(Contact, email=email)
    
    # Define the email details
    subject = "User Acknowledgement Email"
    message = "Our Contact Team Will Contact You Shortly Through Phone Call Or Via Email."
    recipient_list = [order.email]
    from_email = settings.DEFAULT_FROM_EMAIL
    
    # Attempt to send the email
    try:
        send_mail(subject, message, from_email, recipient_list)
        order.email_sent = True  # Mark email as sent
        order.save()  # Save the change to the database
        messages.success(request, "Confirmation email sent successfully.")
    except Exception as e:
        messages.error(request, f"Failed to send email: {e}")
    
    return redirect("showcall")

# def senddelete(request, email):
#     contact = get_object_or_404(Contact, email=email)
    
#     contact.delete()
#     messages.success(request, "Contact deleted successfully.")
    
#     return redirect("showcall")


def senddelete(request, email):
    contacts = Contact.objects.filter(email=email)
    
    if contacts.exists():
        contacts.delete()
        messages.success(request, "All contacts with this email have been deleted successfully.")
    else:
        messages.warning(request, "No contacts found with this email.")
    
    return redirect("showcall")

@login_required(login_url='/login/')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return render(request, 'event/Contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()

    return render(request, 'event/Contact.html', {'form': form, 'success': False})