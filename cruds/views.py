from django.shortcuts import render,redirect
from . models import Becholer,Wedding,Reception
from . forms import *
from django.shortcuts import HttpResponse
from . import renderes 
import io
import csv
from django.views.generic import ListView
from datetime import datetime
from django.contrib.auth.decorators import login_required

# BECHOLER.


def success(request):
    return render(request, 'success.html')

def becholerFormView(request):
    # Initialize the form with GET parameters if present
    theme = request.GET.get('theme', '')
    price = request.GET.get('price', '')
    
    # Create a form instance with initial data if GET request
    if request.method == 'GET':
        form = BecholerForm(initial={'theme_name': theme, 'max_budget': price})
    else:
        # Handle POST request
        form = BecholerForm(request.POST, request.FILES)
        if form.is_valid():
            becholer_order = form.save(commit=False)  # Don't commit yet
            becholer_order.user = request.user  # Assign the logged-in user
            becholer_order.save()
            return redirect('success') 
    return render(request, "cruds/bechform.html", {'form': form})


def bechshow(request):
    obj=Becholer.objects.all()
    return render(request,"cruds/bechshow.html",{'obj':obj})

def bechUpdate(request, f_oid):
    obj = Becholer.objects.get(oid=f_oid)
    form = BecholerForm(instance=obj)
    if request.method == 'POST':
        form = BecholerForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('bechshow')
    return render(request, "cruds/bechform.html", {'form':form})

#update from db
def bechDelete(request, f_oid):
    obj = Becholer.objects.get(oid=f_oid)
    form = BecholerForm(instance=obj)
    if request.method == 'GET':
        obj.delete()
        return redirect('bechshow')
    return render(request, "cruds/bechshow.html", {'form':form})

def bechpdf(request,id):
    obj = Becholer.objects.get(oid=id)
    data = {
        "custFirstName" : obj.fname,
        "custLastName" : obj.lname,
        "max_budget" : obj.max_budget,
        "invoice" :"41251",
        "dateoforder" : "17/12/2024"
    }
    return renderes.render_to_pdf("cruds/bechinvoice.html",data)

def bechbulkupload(request):
    if request.method == 'POST':
        data=io.TextIOWrapper(request.FILES["csvfile"].file)
        list=csv.DictReader(data)
        dataObjs = []
        for i in list:
            booked_at_str = i.get("booked_at", None)
            if booked_at_str:
                try:
                    booked_at = datetime.strptime(booked_at_str, "%d-%m-%Y %H:%M")
                except ValueError:
                    booked_at = None  
            else:
                booked_at = None  

            dataObjs.append(
                Becholer(
                    fname=i["fname"],lname=i["lname"],gender=i["gender"],mail=i["mail"],max_budget=i["max_budget"],theme_name=i["theme_name"],addr=i["address"],sugg=i["suggestion"],status=i.get("status", "Pending"),invoice_sent=i.get("invoice_sent", False),booked_at=booked_at 
                )
            )
        Becholer.objects.bulk_create(dataObjs)
        return HttpResponse("success    ````")


def bechbulkuploadview(request):
    return render(request,"bechbulkupload.html")

class BechSearchView(ListView):
    model = Becholer
    template_name = 'cruds/bechshow.html'
    context_object_name = 'obj'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Becholer.objects.filter(fname__icontains=query).order_by('fname')

# WEDDING


def weddingFormView(request):
    venue = request.GET.get('theme', '')
    price = request.GET.get('price', '')
    if request.method == 'GET':
        form = WeddingForm(initial={'venue': venue, 'max_budget': price})
    else:
        form =WeddingForm(request.POST,request.FILES)
        if form.is_valid():
            wedding_order = form.save(commit=False)
            wedding_order.user = request.user 
            wedding_order.save()
            return redirect('success') 
            # return render('crud/show.html')
    return render(request,"cruds/wedform.html",{'form':form})

def wedshow(request):
    obj=Wedding.objects.all()
    return render(request,"cruds/wedshow.html",{'obj':obj})

def wedUpdate(request, f_oid):
    obj = Wedding.objects.get(oid=f_oid)
    form = WeddingForm(instance=obj)
    if request.method == 'POST':
        form = WeddingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('wedshow')
    return render(request, "cruds/wedform.html", {'form':form})

def wedDelete(request, f_oid):
    obj = Wedding.objects.get(oid=f_oid)
    form = WeddingForm(instance=obj)
    if request.method == 'GET':
        obj.delete()
        return redirect('wedshow')
    return render(request, "cruds/wedshow.html", {'form':form})

def wedpdf(request,id):
    obj = Wedding.objects.get(oid=id)
    data = {
    "gname": obj.gname,
    "bname": obj.bname,
    "max_budget": obj.max_budget,
    "venue": obj.venue,
    "mail": obj.mail,
    "mobile_number": obj.mobile_number,
    "date": obj.date.strftime("%d/%m/%Y"),  # Format the date as needed
    "time": obj.time.strftime("%H:%M"),     # Format the time as needed
    "sugg": obj.sugg,
    "groom_image_url": obj.gimage.url if obj.gimage else '',  # URL of groom's image
    "bride_image_url": obj.bimage.url if obj.bimage else '',  # URL of bride's image
    "invoice": "41251",  # Example static invoice number
    "dateoforder": "17/12/2024"  # Example static order date
}
    return renderes.render_to_pdf("cruds/wedinvoice.html",data)

def wedbulkupload(request):
    if request.method == 'POST':
        data=io.TextIOWrapper(request.FILES["csvfile"].file)
        list=csv.DictReader(data)
        dataObjs = []
        for i in list:
            booked_at_str = i.get("booked_at", None)
            if booked_at_str:
                try:
                    booked_at = datetime.strptime(booked_at_str, "%d-%m-%Y %H:%M")
                except ValueError:
                    booked_at = None 
            else:
                booked_at = None

            date_str = i.get("date", None)
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%d-%m-%Y").date()
                except ValueError:
                    date = None  
            else:
                date = None

            dataObjs.append(
                Wedding(
                    gname=i["gname"],bname=i["bname"],mail=i["mail"],mobile_number=i["mobile_number"],date=date,  time=i.get("time"),  max_budget=i["max_budget"],venue=i["venue"],sugg=i["suggestion"],status=i.get("status", "Pending"),invoice_sent=i.get("invoice_sent", False),booked_at=booked_at  
                )
            )
        Wedding.objects.bulk_create(dataObjs)
        return HttpResponse("success    ````")

def wedbulkuploadview(request):
    return render(request,"wedbulkupload.html")

class WedSearchView(ListView):
    model = Wedding
    template_name = 'cruds/wedshow.html'
    context_object_name = 'obj'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Wedding.objects.filter(gname__icontains=query).order_by('gname')

#RECEPTION

def receptionFormView(request):
    venue = request.GET.get('theme', '')
    price = request.GET.get('price', '')
    if request.method == 'GET':
        form = ReceptionForm(initial={'venue': venue, 'max_budget': price})
    else:
        form =ReceptionForm(request.POST,request.FILES)
        if form.is_valid():
            reception_order = form.save(commit=False)  # Do not save to the database yet
            reception_order.user = request.user  # Assign the logged-in user
            reception_order.save()
            return redirect('success') 
            # return render('crud/show.html')
    return render(request,"cruds/recform.html",{'form':form})

def recshow(request):
    obj=Reception.objects.all()
    return render(request,"cruds/recshow.html",{'obj':obj})

def recUpdate(request, f_oid):
    obj = Reception.objects.get(oid=f_oid)
    form = ReceptionForm(instance=obj)
    if request.method == 'POST':
        form = ReceptionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('recshow')
    return render(request, "cruds/recform.html", {'form':form})

def recDelete(request, f_oid):
    obj = Reception.objects.get(oid=f_oid)
    form = ReceptionForm(instance=obj)
    if request.method == 'GET':
        obj.delete()
        return redirect('recshow')
    return render(request, "cruds/recshow.html", {'form':form})

def recpdf(request,id):
    obj = Reception.objects.get(oid=id)
    data = {
    "gname": obj.gname,
    "bname": obj.bname,
    "max_budget": obj.max_budget,
    "venue": obj.venue,
    "mail": obj.mail,
    "mobile_number": obj.mobile_number,
    "date": obj.date.strftime("%d/%m/%Y"),  # Format the date as needed
    "time": obj.time.strftime("%H:%M"),     # Format the time as needed
    "sugg": obj.sugg,
    "groom_image_url": obj.gimage.url if obj.gimage else '',  # URL of groom's image
    "bride_image_url": obj.bimage.url if obj.bimage else '',  # URL of bride's image
    "invoice": "41251",  # Example static invoice number
    "dateoforder": "17/12/2024"  # Example static order date
}
    return renderes.render_to_pdf("cruds/recinvoice.html",data)

def recbulkupload(request):
    if request.method == 'POST':
        data=io.TextIOWrapper(request.FILES["csvfile"].file)
        list=csv.DictReader(data)
        dataObjs = []
        for i in list:
            booked_at_str = i.get("booked_at", None)
            if booked_at_str:
                try:
                    booked_at = datetime.strptime(booked_at_str, "%d-%m-%Y %H:%M")
                except ValueError:
                    booked_at = None 
            else:
                booked_at = None

            date_str = i.get("date", None)
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%d-%m-%Y").date()
                except ValueError:
                    date = None  
            else:
                date = None

            dataObjs.append(
                Wedding(
                    gname=i["gname"],bname=i["bname"],mail=i["mail"],mobile_number=i["mobile_number"],date=date,  time=i.get("time"),  max_budget=i["max_budget"],venue=i["venue"],sugg=i["suggestion"],status=i.get("status", "Pending"),invoice_sent=i.get("invoice_sent", False),booked_at=booked_at  
                )
            )
        Reception.objects.bulk_create(dataObjs)
        return HttpResponse("success    ````")

def recbulkuploadview(request):
    return render(request,"recbulkuploadview.html")

class RecSearchView(ListView):
    model = Reception
    template_name = 'cruds/recshow.html'
    context_object_name = 'obj'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Reception.objects.filter(gname__icontains=query).order_by('gname')


