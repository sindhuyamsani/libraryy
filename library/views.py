from django.shortcuts import render
from django.http import HttpResponse
from library.models import user,books
from django.contrib import messages
from django.db.models import Q

# Create your views here.
# Home page
def home(request):
    return HttpResponse("Hello World!")


#Register page  for student
def register(request):
    if request.method=='POST':

        if request.POST.get('sroll') and (request.POST.get('spwd')==request.POST.get('oldpwd')):

            user_obj=user()
            user_obj.sroll=request.POST.get('sroll')
            user_obj.spwd=request.POST.get('spwd')
            user_obj.save()
            messages.success(request,"The user "+user_obj.sroll+" has been created successfully")
            return render(request,"home.html")

    else:
        messages.error(request,"Please enter correct credentials")
        return render(request,"home.html")


#Login Page for student and admin
#admin credentials
#username :1000
#password:admin
def login(request):
    if(request.method=='POST'):
        if request.POST.get('sroll') and request.POST.get('spwd'):
            if(request.POST.get('sroll')=="1000" and request.POST.get('spwd')=="admin"):
                return render(request,"admin.html")

            elif(user.objects.get(Q(sroll=request.POST.get('sroll')) & Q(spwd=request.POST.get('spwd')))):
                return render(request,"student.html",{'sroll':request.POST.get('sroll')})
    else:
        return render(request,"login.html")



#To add books by the librarian
def addbooks(request):
    if(request.method=='POST'):

        if request.POST.get('bname') and request.POST.get('bcount'):
            books_obj=books()
            books_obj.sbookname=request.POST.get('bname')
            books_obj.sbookcount=request.POST.get('bcount')
            books_obj.save()
            messages.success(request,"Book inserted successfully")
            return render(request,"admin.html")


    else:
        return render(request,"addpage.html")

#To display the existing books from the library
def display(request):
    book_obj=books.objects.all()
    return render(request,"display.html",{'books':book_obj})
