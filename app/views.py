from django.shortcuts import render,redirect
from .models import Employee ,Department as dep,AddEmployee as new
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Query


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
        #  req.session.flush()
         req.session.pop('msg', None)
         req.session.pop('xyz', None)
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
    if req.method == 'POST':
        e = req.POST.get('email')
        p = req.POST.get('password')

        if e == 'tanishkagupta241@gmail.com' and p == 'gupta':
            req.session['admin'] = {
                'name': 'Tanishka',
                'email': e
            }
            return redirect('dashboard')

        
        user = new.objects.filter(email=e)

        if not user:
            req.session['signup'] = f'Given email {e} is not registered'
            return redirect('login')

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

#     if req.session.get('user_id',None):
#         id = req.session['user_id']
#         userdata= Employee.objects.get(id=id)
#         return render(req,'dashboard.html',{'data':userdata})
#     else:
#        return redirect('login')


# def dashboard(req):

#     if req.session.get('admin', None):
#         data = req.session.get('admin')
#         return render(req, 'admindashboard.html', {'data': data})

#     elif req.session.get('user_id', None):
#         data = req.session.get('user_id')
#         userdata = Employee.objects.get(id=data)
#         return render(req, 'userdashboard.html', {'data': userdata})
    
# newh

def dashboard(req):
    if req.session.get('admin',None):
        
        data=req.session.get('admin')
        return render(req,'admindashboard.html',{'data':data})
    
    elif req.session.get('user_id',None):    
        id = req.session['user_id']
        userdata = new.objects.get(id=id)
        return render(req, 'userdashboard.html', {'data': userdata})
    else:
        return redirect('login')

# newh
    

def add_emp(req):

    if 'admin' in req.session:
        print('admin is here')

        data = req.session.get('admin')

        if req.method == 'POST':

            n = req.POST.get('name')
            e = req.POST.get('email')
            c = req.POST.get('contact')
            p = req.POST.get('password')
            cp = req.POST.get('cpassword')
            img = req.FILES.get('image')
            dept = req.POST.get('department')
            dept_data=dep.objects.get(id=dept)
            d_name=dept_data.name
            d_code=dept_data.code
            d_des=dept_data.description



            print(n, e, c, p, dept,dept_data, d_name, d_code, d_des)

            user = new.objects.filter(email=e)

            if user:
                req.session['msg'] = f'{e} Email already exists'
                return redirect('add_emp')
            else:
                if p == cp:
                    new.objects.create(
                        name=n,
                        email=e,
                        contact=c,
                        password=p,
                        image=img,
                        department=d_name,
                        d_code=d_code,
                        d_des=d_des
                    )
                    send_mail("User id and Password from admin",
                              f'your user_id is {e} and password is {p}',
                              'tanishkagupta241@gmail.com',
                              [e],
                              fail_silently=False)
                    req.session['message'] = 'employee added successfully and user_id sent to mail'
                    return redirect('add_emp')
                
                else:
                    req.session['msg'] = 'Password did not match'
                    return redirect('add_emp')
        
        msg = req.session.pop('msg', None)
        message = req.session.pop('message', None)
        all_dep = dep.objects.all()
        return render(req, 'admindashboard.html', {
            'data': data,
            'add_emp': True,
            'msg': msg,
            'message': message,
            'dep_list':all_dep
        
        })
    

def add_dep(req):
    if 'admin' in req.session:
        print("Dept")
        if req.method=='POST':
            n=req.POST.get('name')
            c=req.POST.get('code')
            d=req.POST.get('description')
            print(n,c,d)
            depart=dep.objects.filter(code=c)
            if depart:
                req.session['msg']='department already exists'
            else:
                dep.objects.create(
                    name=n,
                    code=c,
                    description=d
                )
                req.session['data']='Department created successfully'
                return redirect('add_dep')
        msg = req.session.pop('msg', None)
        # all_dep=dep.objects.all()
        data = req.session.pop('data', None)
            
        return render(req,'admindashboard.html',{'add_dep':True,
                                                 'msg':msg,
                                                 'data':data,
                                                
                                                 })
    

def all_dep(req):
    if 'admin' not in req.session:
        return redirect('login')

    data = req.session.get('admin')

    departments = dep.objects.all()

    return render(req,'admindashboard.html', {
        'data': data,
        'all_dep': True,
        'departments': departments
    })
    

def all_emp(req):
    if 'admin' not in req.session:
        return redirect('login')
    data = req.session.get('admin')
    employees = new.objects.all()
    return render(req,'admindashboard.html', {
        'data': data,
        'all_emp': True,
        'employees': employees
    })
    
    
def logout(req):
    # if req.session.get('user_id',None):
    req.session.flush()
    return redirect('login')



def show_query(req):
     if 'admin' not in req.session:
          return redirect('login')
     else:
          queries = Query.objects.all()
          return render(req,'admindashboard.html',{
                'show_query':True,
                'queries':queries,
                'data':req.session.get('admin')
          })


def delete(req,pk):
    data = Query.objects.get(id=pk)
    data.delete()
    all_query = Query.objects.all()
    return render(req,'admindashboard.html',{'queries':all_query})



def userdashboard(req):
    if 'user_id' in req.session:
        id=req.session['user_id']
        userdata=new.objects.get(id=id)
        return render(req,'userdashboard.html',{'data':userdata})
    

def profile(req):
    if 'user_id' in req.session:
        id=req.session['user_id']
        userdata=new.objects.get(id=id)
        return render(req,'userdashboard.html',{'data':userdata,'profile':True})
    else:
        return redirect('login')
    
    
def query(req):
    if 'user_id' in req.session:
        id=req.session['user_id']
        userdata=new.objects.get(id=id)
        return render(req,'userdashboard.html',{'data':userdata,'query':True})
    else:
        return redirect('login')


def query_status(req):
    if 'user_id' in req.session:
        id=req.session['user_id']
        userdata=new.objects.get(id=id)
        query_data=Query.objects.filter(email=userdata.email)

        return render(req,'userdashboard.html',{'data':userdata,'query_status':query_data})
    else:
        return redirect('login')


# def all_query(req):
#     if 'user_id' in req.session:
#         id=req.session['user_id']
#         userdata=new.objects.get(id=id)
#         queries = Query.objects.filter(email=userdata.email)
#         return render(req,'userdashboard.html',{'data':userdata,'all_query':True,'queries': queries})
#     else:
#         return redirect('login')

def all_query(req):
    if 'user_id' in req.session:
        id = req.session['user_id']
        userdata = new.objects.get(id=id)

        order = req.GET.get('order')  

        if order == 'oldest':    
            queries = Query.objects.filter(
                email=userdata.email
            ).order_by('created_at')      
        else:
            queries = Query.objects.filter(
                email=userdata.email
            ).order_by('-created_at')     

        return render(req, 'userdashboard.html', {
            'data': userdata,
            'all_query': True,
            'queries': queries
        })
    else:
        return redirect('login')

    
def query_data(req):
      if 'user_id' in req.session:
          id=req.session['user_id']
          userdata=new.objects.get(id=id)
          if req.method=='POST':
               n=req.POST.get('name')
               e=req.POST.get('email')
               s=req.POST.get('subject')
               q=req.POST.get('query')
               solu=req.POST.get('reply','panding')
               
               print(n,e,s,q,solu,sep=',')
               Query.objects.create(name=n,email=e,subject=s,query=q,solution=solu)
            #    return render (req,'userdashboard.html',{'data':userdata})
               msg = "Query sent successfully"
               return render (req,'userdashboard.html',{'data':userdata,'query':True,'msg':msg})
      else:
          return redirect('login')

def reply_query(req,pk):
     if 'admin' in req.session:
        data = req.session.get('admin')
        if req.method=='POST':
             r = req.POST.get('reply')
             querydata = Query.objects.get(id=pk)
             if len(r)>1:
               querydata.solution = r
               querydata.status="Done"
               querydata.save()
               queries = Query.objects.all().order_by('created_at')
               return render(req,'admindashboard.html',{
                'all_query':True,
                'queries':queries,
                'data':req.session.get('admin')  
               })
     

        else:
             return render(req, 'admindashboard.html', {'data': data,'reply':True,'id':pk})
        

def edit(req,pk):
    if 'user_id' in req.session:
        id=req.session.get('user_id')
        userdata=new.objects.get(id=id)
        query=Query.objects.get(id=pk)
        return render(req,'userdashboard.html',{'data':userdata,'e_query':query})
    
    
def update(req,pk):
    if 'user_id' in req.session:
        id=req.session.get('user_id')
        query=Query.objects.get(id=pk)
        query.name=req.POST.get('name')
        query.email=req.POST.get('email')
        query.subject=req.POST.get('subject')
        query.query=req.POST.get('query')
        query.save()
        userdata=new.objects.get(id=id)
        queries = Query.objects.filter(email=userdata.email)
        return render(req,'userdashboard.html',{'data':userdata,'all_query':True,'queries': queries})
    

# def delete_query(req, pk):
#     query = Query.objects.get(id=pk)
#     query.delete()
#     # return redirect(req,'all_query') 
#     # return render(req,'userdashboard.html',{'queries':all_query})
#     return redirect('all_query')
 
def delete_query(req, pk):
    if 'user_id' not in req.session:
        return redirect('login')
    u_id=req.session.get('user_id')
    user=new.objects.get(id=u_id)
    data=Query.objects.get(id=pk)
    data.delete()
    all_query=Query.objects.filter(email=user.email)
    return redirect ('all_query')

def search(req):
    # if not 'user_id' in req.session:
    #     redirect ('login')
    # user_id=req.session.get('user_id')
    # data=new.objects.get(id=user_id)
    # s=req.POST.get('search')
    # f_qdata = Query.objects.filter(name=s, query=s, status=s)
    if 'user_id' in req.session:
        id=req.session['user_id']
        userdata=new.objects.get(id=id)
        s=req.POST.get('search')
        # queries = Query.objects.filter(email=userdata.email,name=s)
        # queries = Query.objects.filter(email=userdata.email,name=s,query=s)
        queries = Query.objects.filter(email=userdata.email,name__contains=s,query__contains=s)


        return render(req,'userdashboard.html',{'data':userdata,'all_query':True,'queries': queries})
    else:
        return redirect('login')
    

def reset(req):
    if 'user_id' in req.session:
        id=req.session['user_id']
        userdata=new.objects.get(id=id)
        s=req.POST.get('search')
        queries = Query.objects.filter(email=userdata.email)
        return render(req,'userdashboard.html',{'data':userdata,'all_query':True,'queries': queries})
    else:
        return redirect('login')


