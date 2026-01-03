from django.shortcuts import render,redirect
from .models import Employee
from django.http import HttpResponse

# Create your views here.

def landing(req):
    return render(req,'landing.html')

def registration(req):
        # print(req.method)
        # print(req.POST)
        # print(req.FILES)

        if req.method =='POST':
            n=req.POST.get('name')
            e=req.POST.get('email')
            c=req.POST.get('contact')
            g=req.POST.get('gender')
            q=req.POST.getlist('qualification[]')
            s=req.POST.get('state')
            i=req.FILES.get('image')
            a=req.FILES.get('audio')
            v=req.FILES.get('video')
            r=req.FILES.get('resume')
            p=req.POST.get('password')
            cp=req.POST.get('cpassword')

            # print(n,e,c,g,q,s,i,a,v,r,p,cp,sep='\n')

            user = Employee.objects.filter(email=e)
            if user:
                req.session['msg']=f"{e} Email already exist"
                return redirect('registration')
            else:
                if p==cp:
                     Employee.objects.create(name=n,email=e,contact=c,gender=g,qualification=','.join(q),
                                state=s,image=i,audio=a,video=v,resume=r,password=p)
                     req.session['pqr']="Registration Done"
                    
                     return redirect('login')
                else:
                     req.session['xyz']="password and confirm password not matched"
                     return redirect('registration')

    

        else:
        #  msg = req.session['msg']
         msg = req.session.get('msg','')
         xyz = req.session.get('xyz','')
         signup = req.session.get('signup','')
        #  del req.session['msg']
         req.session.flush()
         return render(req,'registration.html',{'msg':msg,'xyz':xyz,'signup':signup})
        
def show_data(req):
    # query that work on single object
    # data = Employee.objects.get(id=1)
    # data = Employee.objects.first()
    # data = Employee.objects.last()
    # data = Employee.objects.latest('name')
    # data = Employee.objects.earliest('name')
    # data = Employee.objects.create()
    # print(data.name,data.email,data.contact)


    # query that work on multiple objects

    # data = Employee.objects.all()
    # data = Employee.objects.filter(gender='Female')
    # data = Employee.objects.exclude(gender='Female')
    # data = Employee.objects.order_by('gender')
    # data = Employee.objects.order_by('name')
    # data = Employee.objects.order_by('-name')
    # data = Employee.objects.values()
    data = Employee.objects.values('name','email','contact','gender','qualification','state')
    # data = Employee.objects.values_list()
    # data = Employee.objects.values_list(
    # 'name','email','contact','gender','qualification','state')

    print(data)


    # Composite query
    # Employee.objects.filter(email='tanishkagupta241@gmail.com').delete()
    # Employee.objects.update_or_create(name='rashi',email='rashi123@gmail.com',defaults={'gender':'female'})
    # Employee.objects.filter(gender='on').update(gender='female')
    # data,created = Employee.objects.get_or_create(name='yashi',email='yashi123@gmail.com')
    # data = Employee.objects.all()

    # data = Employee.objects.order_by('email').first()
    

    

    for i in data:
        # print(i.name,i.email,i.contact)
        print(i['name'],i['email'],i['contact'],i['gender'],i['qualification'],i['state'])
        # print(i[0],i[1],i[2],i[3],i[4],i[5])         
    return render(req,'show_data.html',{'data':data})


def login(req):
    req.session.flush()  
    if req.method == 'POST':
        e = req.POST.get('email')
        p = req.POST.get('password')

        if e == 'rashi@gmail.com' and p == 'gupta':
            req.session['admin'] = {
                'name': 'Rashi',
                'email': e
            }
            return redirect('dashboard')

        
        user = Employee.objects.filter(email=e)

        if not user:
            req.session['signup'] = f'Given email {e} is not registered'
            return redirect('registration')

        userdata = user.first()
        if p == userdata.password:
            req.session['user_id'] = userdata.id
            return redirect('dashboard')
        else:
            req.session['signup'] = 'Wrong password'
            return redirect('login')

    msg = req.session.get('pqr')
    return render(req, 'login.html', {'pqr': msg})


# def dashboard(req):
#     if req.session.get('user_id'):
#         id = req.session['user_id']
#         userdata= Employee.objects.get(id=id)
#         return render(req,'dashboard.html',{'data':userdata})
#     else:
#        return redirect('login')


def dashboard(req):

    if req.session.get('admin', None):
        data = req.session.get('admin')
        return render(req, 'admindashboard.html', {'data': data})

    elif req.session.get('user_id', None):
        data = req.session.get('user_id')
        userdata = Employee.objects.get(id=data)
        return render(req, 'userdashboard.html', {'data': userdata})
    

def add_emp(req):
    if 'admin' in req.session:
        print ('hello')
        data = req.session.get('admin')
        return render(req, 'admindashboard.html', {'data': data,'add_emp':True})

# def add_emp(req):
#     if 'admin' in req.session:
#         data = req.session.get('admin')
#         message = ""

#         if req.method == 'POST':
#             name = req.POST.get('name')
#             email = req.POST.get('email')
#             contact = req.POST.get('contact')
#             password = req.POST.get('password')
#             cpassword = req.POST.get('cpassword')

#             if password != cpassword:
#                 message = "Passwords do not match"

#             elif Employee.objects.filter(email=email).exists():
#                 message = "Employee already exists"
#             else:
                
#                 Employee.objects.create(
#                     name=name,
#                     email=email,
#                     contact=contact,
#                     password=password
#                 )
#                 message = "Employee added successfully"

#         return render(req, 'admindashboard.html', {'data': data, 'add_emp': True, 'message': message})

#     else:
#         return redirect('login')

    
def add_dep(req):
    if 'admin' in req.session:
        data = req.session.get('admin')
        return render(req, 'admindashboard.html', {'data': data,'add_dep':True})

def all_dep(req):
    if 'admin' in req.session:
        data = req.session.get('admin')
        return render(req, 'admindashboard.html', {'data': data,'all_dep':True})
    
def all_emp(req):
    if 'admin' in req.session:
        data = req.session.get('admin')
        return render(req, 'admindashboard.html', {'data': data,'all_emp':True})

# def all_emp(req):
#     if 'admin' in req.session:
#         data = req.session.get('admin')
#         employees = Employee.objects.all() 
#         return render(req, 'admindashboard.html', {
#             'data': data,
#             'all_emp': True,
#             'employees': employees
#         })
#     else:
#         return redirect('login')


    
def logout(req):
    # if req.session.get('user_id',None):
    req.session.flush()
    return redirect('login')