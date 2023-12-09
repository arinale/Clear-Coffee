from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re
# Create your views here.

def signin(requset):
    if requset.method == 'POST' and 'btnlogin' in requset.POST :
        username=requset.POST['user']
        password=requset.POST['pass']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if'rememberme' not in requset.POST:
                requset.session.set_expiry(0)
            auth.login(requset,user)
            #messages.success(requset,'You are now logged in')
        else:
            messages.error(requset,'Username or password invalid')
        return redirect('signin')
    else:
        return render(requset,'accounts/signin.html')

def signup(requset):
    if requset.method == 'POST' and 'btnsignup' in requset.POST:

        #variables for fields
        fname = None
        lname = None
        address = None
        address2 = None
        city = None
        state = None
        email = None
        username = None
        password = None
        terms = "on"
        is_added=None

        #Get values from the form
        if 'fname' in requset.POST : fname = requset.POST['fname']
        else:messages.error(requset,'Error in first name')

        if 'lname' in requset.POST: lname = requset.POST['lname']
        else: messages.error(requset, 'Error in last name')

        if 'address' in requset.POST: address = requset.POST['address']
        else:messages.error(requset, 'Error in first address')

        if 'address2' in requset.POST: address2 = requset.POST['address2']
        else: messages.error(requset, 'Error in address2')

        if 'city' in requset.POST: city = requset.POST['city']
        else:messages.error(requset, 'Error in city')

        if 'state' in requset.POST: state = requset.POST['state']
        else:messages.error(requset, 'Error in state')

        if 'email' in requset.POST: email = requset.POST['email']
        else:messages.error(requset, 'Error in email')

        if 'user' in requset.POST: username = requset.POST['user']
        else:messages.error(requset, 'Error in username')

        if 'pass' in requset.POST: password=requset.POST['pass']
        else:messages.error(requset, 'Error in password')
        if 'terms' in requset.POST: terms = requset.POST['terms']

        if fname and lname and address and address2 and city and state and email and username and password:
            if terms == 'on':
                #Check if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(requset,'This username is taken')
                else:
                     #Check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(requset,'This email is taken')
                    else:
                        patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt,email):
                            #add user
                            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
                            user.save()
                            #add user profile
                            userprofile=UserProfile(user=user,address=address,address2=address2,city=city,state=state)
                            userprofile.save()
                            #clear fields
                            fname=''
                            lname=''
                            address=''
                            address2=''
                            city=''
                            state=''
                            email=''
                            username=''
                            password=''
                            terms=None

                            #Success Message
                            messages.success(requset,'Your account is created')
                            is_added=True
                        else:
                            messages.error(requset,'Invalid email')
            else:
                messages.error(requset,'You must agree to the terms')
        else:
            messages.error(requset,'Check empty fields')
        return render(requset,'accounts/signup.html',{
            'fname':fname,
            'lname':lname,
            'address':address,
            'address2':address2,
            'city':city,
            'state':state,
            'email':email,
            'user':username,
            'pass':password,
            'is_added':is_added

        })
    else:
        return render(requset,'accounts/signup.html')

def profile(requset):
    if requset.method == 'POST'  and 'btnsave' in requset.POST:
        if requset.user is not None and requset.user.id != None:
            userprofile=UserProfile.objects.get(user=requset.user)

            if requset.POST['fname'] and requset.POST['lname'] and requset.POST['address'] and  requset.POST['address2'] and requset.POST['city'] and requset.POST['state'] and requset.POST['email'] and requset.POST['user'] and requset.POST['pass'] :
                requset.user.first_name=requset.POST['fname']
                requset.user.last_name = requset.POST['lname']
                userprofile.address = requset.POST['address']
                userprofile.address2 = requset.POST['address2']
                userprofile.city = requset.POST['city']
                userprofile.state = requset.POST['state']
                #requset.user.email= requset.POST['email']
                #requset.user.username = requset.POST['user']
                if not requset.POST['pass'].startswith('pbkdf2_sha256$'):
                    requset.user.set_password(requset.POST['pass'])
                requset.user.save()
                userprofile.save()
                auth.login(requset,requset.user)
                messages.success(requset,'Your data has been saved ')
            else:
                messages.error(requset,'Check your values and elements')


        return redirect('profile')
    else:
        #if requset.user.is_anonymous:return redirect('index')
       #if requset.user.id== None:return redirect('index')

       if requset.user is not None:
           context=None
           if not requset.user.is_anonymous:
                userprofile=UserProfile.objects.get(user=requset.user)

                context = {
                   'fname': requset.user.first_name,
                   'lname': requset.user.first_name,
                   'address': userprofile.address,
                   'address2': userprofile.address2,
                   'city': userprofile.city,
                   'state': userprofile.state,
                   'email': requset.user.email,
                   'user': requset.user.username,
                   'pass': requset.user.password,

               }
           return render(requset,'accounts/profile.html',context)




def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

def product_favorite(requset,pro_id):
    if  requset.user.is_authenticated and not requset.user.is_anonymous:
       pro_fav =Product.objects.get(pk=pro_id)
       if UserProfile.objects.filter(user=requset.user,product_favorites=pro_fav).exists():
           messages.success(requset,'Already product in the favorite list')
       else:
           userprofile=UserProfile.objects.get(user=requset.user)
           userprofile.product_favorites.add(pro_fav)
           messages.success(requset,'Product has been favorited')

    else:
        messages.error(requset,'You must be logged in')

    return redirect('/products/'+str(pro_id))

def show_product_favorite(requset):
    context=None
    if requset.user.is_authenticated and not requset.user.is_anonymous:
        userInfo=UserProfile.objects.get(user=requset.user)
        pro=userInfo.product_favorites.all()
        context={'products':pro }

    return render(requset,'products/products.html',context)