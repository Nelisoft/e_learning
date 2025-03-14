from .models import Contactinfo

def default(request):
    contact = Contactinfo.objects.order_by('-id')[0:1]
    return {
        'contact':contact
    }