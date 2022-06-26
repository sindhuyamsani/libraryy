from django.shortcuts import render
from django.http import HttpResponse
from library.models import user,books,transaction
from django.contrib import messages
from django.db.models import Q

# Create your views here.
# Home page
def home(request):
    request.session['loggedin'] = False
    return render(request,"login.html")

#this func renders signup page
def signup(request):
    return render(request,"signup.html")

#this func add the uname and pword to db from signup page
def add(request):
    if request.method=='POST':
        if request.POST.get('sroll') and (request.POST.get('spwd')==request.POST.get('oldpwd')):
            user_obj=user()
            user_obj.sroll=request.POST.get('sroll')
            user_obj.spwd=request.POST.get('spwd')
            user_obj.save()
            messages.success(request,"The user "+user_obj.sroll+" has been created successfully")
            return render(request,"login.html")
    else:
        messages.error(request,"Please enter correct credentials")
        return render(request,"login.html")


#Login Page for student and admin
#admin credentials
#username :1000
#password:admin
def check(request):
    if(request.method=='POST'):
        if request.POST.get('sroll') and request.POST.get('spwd'):
            if(request.POST.get('sroll')=="1000" and request.POST.get('spwd')=="admin"):
                request.session['username']='1000'
                request.session['type']='admin'
                request.session['loggedin']=True
                return render(request,"admin.html")
            else:
                myobj=user.objects.get(Q(sroll=request.POST.get('sroll')))
                if(request.POST.get('spwd')==myobj.spwd):
                    request.session['username']=request.POST.get('sroll')
                    request.session['type']='student'
                    request.session['loggedin']=True
                    return render(request,"student.html",{'sroll':myobj.sroll})
                else:
                    return HttpResponse('incorrect inputs')
    else:
        request.session['loggedin']=False
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
    if(request.session['loggedin'] and request.session['username'] and request.session['type']=='student'):
        book_obj=books.objects.filter(sbookcount__gt=0)
        return render(request,"display.html",{'books':book_obj})
    if(request.session['loggedin'] and request.session['username'] and request.session['type']=='admin'):
        book_obj=books.objects.all()
        return render(request,"display.html",{'books':book_obj})
    else:
        return render(request,"login.html")

# for admin page wt all books are requested
def requested_books(request):
    if(request.session['loggedin'] and request.session['username'] and request.session['type']=='admin'):
        req_book_obj = transaction.objects.filter(Q(sstatus="requested"))
        return render(request,"requested.hmtl",{'req':req_book_obj})
    else:
        return render(request,"login.html")

#when student requests a book
def requesting_book(request):
    if request.method=='POST':
        trans_obj=transaction()
        trans_obj.sroll=request.session['username']
        trans_obj.sbookname=request.POST.get('sbookname')
        trans_obj.sstatus='requested'
        trans_obj.save()
        return render(request,"student.html")
    else:
        messages.error(request,"Please enter correct credentials")
        return render(request,"student.html")