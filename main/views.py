from django.shortcuts import render,redirect,get_object_or_404
from main.forms import RenterForm
from main.models import Renter
from datetime import datetime

def sendPayment(request,id):
    renter = get_object_or_404(Renter,id=id)
    renter.sms()
    return redirect('list')

def newRenter(request):
    if not request.user.is_authenticated:
        return redirect('list')
    if request.method == "POST":
        form = RenterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.landlord = request.user
            post.save()
            return redirect('/')
    else:
        form = RenterForm()
    return render(request, 'renter/add.html', {'form': form})

def listRenters(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    user = request.user
    renters = Renter.objects.filter(landlord=user)
    now = datetime.now()
    year, month, *args = now.timetuple()
    last_paid = "{0}-{1}".format(year,month)
    context = {
        'renters': renters,
        'last_paid': last_paid
    }
    return render(request, 'renter/list.html', context)

def detailRenter(request,id):
    renter = Renter.objects.get(id=id)
    if request.user != renter.landlord:
        return redirect('list')
    return render(request,'renter/details.html', {'renter': renter})

def deleteRenter(request,id):
    renter = Renter.objects.get(id=id)
    if request.user != renter.landlord:
        return redirect('list')
    renter.delete()
    return redirect('list')

def editRenter(request,id):
    renter = get_object_or_404(Renter, id=id)
    if request.user != renter.landlord:
        return redirect('list')
    if request.method == "POST":
        form = RenterForm(request.POST,instance=renter)
        if form.is_valid():
            renter = form.save(commit=False)
            renter.landlord = request.user
            renter.save()
            return redirect('details', id=renter.id)
    else:
        form = RenterForm(instance=renter)
    return render(request, 'renter/edit.html', {'form': form})