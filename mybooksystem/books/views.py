from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext,render
from .models import Book
from .forms import SubmitForm
import time,datetime

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def publish(request):
	books = Book.objects.all()
	return render(request,'index.html',{'books':books})

@csrf_exempt
def borrow(request,offset):
	booknum = str(int(offset))
	booksinfo = Book.objects.get(Number = booknum)
#	book = booksinfo.Isbn
	book = booksinfo.Number
	if request.method == 'POST':
		form = SubmitForm(request.POST)
		if form.is_valid():
			usrid = form.cleaned_data['usrid']
			borrow_time = form.cleaned_data['borrow_time']
			phone_number = form.cleaned_data['phone_number']
			timenow = datetime.datetime.now()
			time_endtime = str(timenow + datetime.timedelta(days=int(borrow_time)+2))
#			selectbook = Book.objects.get(Isbn=book)
			selectbook = Book.objects.get(Number=book)
			selectbook.Ordered = True
			selectbook.Keeper = usrid
			selectbook.Endtime = time_endtime[0:10]
			selectbook.Keepertel = phone_number
			selectbook.save()
			return HttpResponseRedirect('/')
	else:
		form = SubmitForm()
	return render_to_response('borrow.html',
			{'booksinfo':booksinfo,'book':book,'form':form})