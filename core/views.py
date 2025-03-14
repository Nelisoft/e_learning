from django.shortcuts import render,get_object_or_404,redirect
from .models import Contactinfo, Course,Category,Instructor
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver

from django.urls import reverse

# Create your views here.

def Home(request):
    course= Course.objects.filter(status='PUBLISH').order_by('-id')
    category = Category.objects.all().order_by('-id')[:4]
    instructors = Instructor.objects.all().order_by('-id')[:4]

    
    context={
        'courese':course,
        'category':category,
        'instructor':instructors
    }
    return render (request, 'core/index.html',context)



def About(request):
    return render(request, 'core/about.html')

def Contact(request):
    contact = Contactinfo.objects.order_by('-id')[0:1]
    context ={
        'contact':contact
    }
    
    return render(request, 'core/contact.html',context)

def Testimonials(request):
    return render(request, 'core/testimonial.html')

def Team(request):
  
    instructors = Instructor.objects.all().order_by('-id')[:4]

    
    context={
     
        'instructor':instructors
    }
    return render(request, 'core/team.html', context)

def Courses(request):
    course= Course.objects.filter(status='PUBLISH').order_by('-id')
    category = Category.objects.all().order_by('-id')[:4]
    instructors = Instructor.objects.all().order_by('-id')[:4]
    
    context={
        'courese':course,
        'category':category,
        'instructor':instructors
    }
    return render(request, 'core/courses.html', context)

# def handler404(request,exception):
#     return render(request,'core/404.html', status=404)



def Course_details(request, slug):
    course = Course.objects.filter(course_slug = slug)
    instructors = Instructor.objects.all().order_by('-id')[:4]
    if course.exists():
        course= course.first()
        
    else:
        return redirect('404')
    context={
        'course':course,
        'instructor':instructors
    }
    return render(request, 'core/details.html', context) 

def PAGE_NOT_FOUND(request):
    return render(request,'core/404.html')



def Checkout(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': course.price,
        'item_name': course.title,
        # 'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        # 'return_url': f"http://{host}{reverse('payment-success', kwargs = {'course_id': course.course_slug})}",
        # 'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'course_id': course.id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'course': course,
        'paypal': paypal_payment
    }

    return render(request, 'core/chectout.html', context)

def PaymentSuccessful(request, course_id):

    course = Course.objects.get(course_slug=course_id)

    return render(request, 'payment-success.html', {'course': course})

def paymentFailed(request, course_id):

    course = Course.objects.get(id=course_id)

    return render(request, 'payment-failed.html', {'course': course})



# def Checkout(request, course_id):
#     course = get_object_or_404(Course, id=course_id)  # Get course details

#     # PayPal Payment Details
#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,  # PayPal account
#         "amount": course.price,  # Amount for the course
#         "item_name": course.title,  # Item being purchased (course)
#         "invoice": f"course-{course.id}-{request.user.id}",  # Unique invoice number
#         "currency_code": "USD",  # Currency code
#         # "return_url": settings.PAYPAL_RETURN_URL,  # URL for successful payment
#         # "cancel_return": settings.PAYPAL_CANCEL_URL,  # URL for canceled payment
#     }

#     # Create PayPal form
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     form.is_valid()  # Ensure the form is valid

#     return render(request, "core/chectout.html", {'form': form, 'course': course})


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender  # This is the IPN object
    if ipn_obj.payment_status == 'Completed':
        # Process the payment, update user’s course enrollment, etc.
        course_id = ipn_obj.invoice.split('-')[1]
        user_id = ipn_obj.invoice.split('-')[2]
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        # Enroll the user in the course
        course.users.add(user)
        course.save()