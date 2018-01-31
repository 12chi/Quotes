from django.shortcuts import render, redirect
from time import gmtime, strftime
import re
import random
import bcrypt
from django.contrib import messages
from models import *

def index(request):

    return render(request, "quotes/index.html")

def quotes(request):
    print "----QUOTE HOME"
 
    usr = User.objects.get(id=request.session['uid'])

    all_quotes = Quote.objects.exclude(favorite_of_users=usr)
    all_fav = usr.favorite_quotes.all()

    all_cnt = all_quotes.count()
    fav_cnt = all_fav.count()

    print all_cnt
    print fav_cnt
    context = {
        'all_quotes': all_quotes,
        'favs': all_fav,
        'all_cnt': all_cnt,
        'fav_cnt': fav_cnt,
    }
    print context
    return render(request, "quotes/quotes.html", context)

def add_fav(request, qid):
    print ('--- add to favorit ---')
    print request.session.values()
    usr = User.objects.get(id = request.session['uid'])

    qt = Quote.objects.get(id = qid)

    usr.favorite_quotes.add(qt)
    usr.save()

    print usr.favorite_quotes.all()

    return redirect('/quotes')

def add_quote(request):
    print ('--- add to favorit ---')
    print request.POST

    usr = User.objects.get(id = request.session['uid'])

    errors = Quote.objects.validate_quote(request.POST['quote'])

    print errors
    if (errors):
        print "==== errror "
        print errors
        for error in errors:
            messages.error(request, errors[error])
        print messages
        return redirect("/quotes")
    print "===== no errors ==="

    qt = Quote.objects.create(quote=request.POST['quote'], author=request.POST['author'], creator=usr)

    print qt

    return redirect('/quotes')

def del_fav(request, qid):
    usr = User.objects.get(id = request.session['uid'])

    qt = Quote.objects.get(id = qid)

    usr.favorite_quotes.remove(qt)

    return redirect('/quotes')

def show_user(request, uid):
    usr = User.objects.get(id = request.session['uid'])

    qt = usr.quotes.all()
    cnt = usr.quotes.count()
    nm = usr.name

    context = {
        'all_quotes': qt,
        'count': cnt,
        'name': nm,
    }

    return render(request, "quotes/show_user.html", context)

def register(request):
    if request.method == 'POST':
        print " Post "
        #validate data

        print request.POST
        print "---validate data ---"
        errors = User.objects.validate(request.POST)

        print errors
        if (errors):
            print "==== errror "
            for error in errors:
                messages.error(request, errors[error])
            print messages
            return render(request, "quotes/index.html")
        print "===== no errors ==="
        
        print "====  create user ===="
        # hash password
        hashPWD = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())

        # check to see if email has been used
        usr = ''
        try:
            usr = User.objects.get(email=request.POST['email'])
        except Exception as e:
            print e, str(type(e))
            # no user in db, register user
    
            # create new user
            newUser = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], pwd = hashPWD, dob=request.POST['dob'])
            print " newUser: ", newUser
            request.session['user'] = newUser.name
            request.session['uid'] = newUser.id

        if usr:
            messages.error(request, "Error: Email has previously used to register another user.  Please use another email.")
            return render(request, "quotes/register.html")
        
        return redirect('/success')
    return render(request, "quotes/index.html")

def login(request):
    if request.method == 'POST':
        print "---sign in validate data ---"
        print request.POST
        errors = User.objects.validate(request.POST)
        print "-- error: ", errors
        if (errors):
            print "==== errror "
            for error in errors:
                messages.error(request, errors[error])
            print messages
            return redirect("/login")
        print "===== no errors ==="
        
        usr = ''

        try:
            usr = User.objects.get(email = request.POST['email'])
        except Exception as e:
            print e, str(type(e))
            messages.error(request, "Error: Invalid User")
            return render(request, "quotes/login.html")

        if usr:
            print usr
            valid = bcrypt.checkpw(request.POST['pwd'].encode(), usr.pwd.encode())
            if (valid):
                print "password match"
                request.session['uid'] = usr.id
                request.session['user'] = usr.name
            else:
                messages.error(request, "Error: Invalid Password")
                return redirect('/login')
                # return render(request, "quotes/login.html")    
        print request.session.values()
        return redirect('/quotes')
    return render(request, "quotes/index.html")

def success(request):
    return render(request, 'quotes/success.html')

def reset(request):
    request.session.clear()
    return redirect('/main')