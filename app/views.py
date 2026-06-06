from django.shortcuts import render,redirect
from .models import Employee ,Department as dep,AddEmployee as new ,Task,ProjectGroup, New
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Query
from django.db.models import Q

from django.contrib import messages
from datetime import date
from django.db import IntegrityError
from .models import Attendance

from django.template.loader import get_template
from xhtml2pdf import pisa
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
                     req.session['login_msg'] = "Registration Done"
                    
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
            req.session['pqr'] = f'Given email {e} is not registered'
            return redirect('login')

        userdata = user.first()
        if p == userdata.password:
            req.session['user_id'] = userdata.id
            return redirect('dashboard')
        else:
            req.session['pqr'] = 'Wrong password'
            return redirect('login')

    msg = req.session.pop('pqr', None)  
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
    if req.session.get('admin', None):
        data = req.session.get('admin')
        
        total_emp = new.objects.count()
        total_dep = dep.objects.count()
        total_query = Query.objects.count()
        total_tasks = Task.objects.count() # 🔥 Naya task count
        
        today = date.today()
        today_attendance = Attendance.objects.filter(date=today).count()
        
        return render(req, 'admindashboard.html', {
            'data': data,
            'total_emp': total_emp,
            'total_dep': total_dep,
            'total_query': total_query,
            'today_attendance': today_attendance,
            'total_tasks': total_tasks # 🔥 Template me bheja
        })
    
    elif req.session.get('user_id', None):    
        id = req.session['user_id']
        userdata = new.objects.get(id=id)
        # Employee ke apne saare tasks userdashboard par dikhane ke liye
        my_tasks = Task.objects.filter(assigned_to=userdata).order_by('-created_at')
        return render(req, 'userdashboard.html', {'data': userdata, 'my_tasks': my_tasks})
        
    else:
        return redirect('login')

# newh
def add_emp(req):

    if 'admin' in req.session:

        data = req.session.get('admin')

        if req.method == 'POST':

            n = req.POST.get('name')
            e = req.POST.get('email')
            c = req.POST.get('contact')
            p = req.POST.get('password')
            cp = req.POST.get('cpassword')
            img = req.FILES.get('image')
            dept = req.POST.get('department')
            joining_date = req.POST.get('joining_date')
            salary = req.POST.get('salary')

            # FORM DATA SAVE
            form_data = {
                'name': n,
                'email': e,
                'contact': c,
                'joining_date': joining_date,
                'salary': salary,
                'department': dept,
            }

            all_dep = dep.objects.all()

            # =========================
            # VALIDATION
            # =========================

            if not n:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Name is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not e:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Email is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not c:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Contact is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not c.isdigit():
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Contact must contain numbers only',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if len(c) != 10:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Contact must be exactly 10 digits',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not dept:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Department is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not joining_date:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Joining date is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not salary:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Salary is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not p:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Password is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if not cp:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Confirm password is required',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            if p != cp:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': 'Password did not match',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            # EMAIL CHECK
            user = new.objects.filter(email=e)

            if user:
                return render(req, 'admindashboard.html', {
                    'data': data,
                    'add_emp': True,
                    'msg': f'{e} Email already exists',
                    'dep_list': all_dep,
                    'form_data': form_data
                })

            # DEPARTMENT DATA
            dept_data = dep.objects.get(id=dept)

            d_name = dept_data.name
            d_code = dept_data.code
            d_des = dept_data.description

            # SAVE EMPLOYEE
            new.objects.create(
                name=n,
                email=e,
                contact=c,
                password=p,
                image=img,
                department=d_name,
                d_code=d_code,
                d_des=d_des,
                joining_date=joining_date,
                salary=salary
            )

            send_mail(
                "User id and Password from admin",
                f'your user_id is {e} and password is {p}',
                'tanishkagupta241@gmail.com',
                [e],
                fail_silently=False
            )

            # SUCCESS MESSAGE
            req.session['success'] = 'Employee added successfully'

            # REDIRECT FOR FORM REFRESH
            return redirect('add_emp')

        # GET REQUEST
        all_dep = dep.objects.all()

        success = req.session.pop('success', None)

        return render(req, 'admindashboard.html', {
            'data': data,
            'add_emp': True,
            'dep_list': all_dep,
            'message': success
        })

    else:
        return redirect('login')    


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
        
    # Aapka purana code line 1 aur 2 (waise ka waise hi hai)
    data = req.session.get('admin')
    employees = new.objects.all()
    
    # 🔥 YE NAYA CODE HAI: Jo aapke purane code ke sath jud rha hai
    search_value = req.POST.get('search', '').strip()
    if search_value:
        employees = employees.filter(
            Q(name__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(contact__icontains=search_value) |
            Q(department__icontains=search_value)
        )
    # 🔥 NAYE CODE KA KHATAM
    
    # Aapka purana return statement (bas isme search_query ko extra bheja hai)
    return render(req,'admindashboard.html', {
        'data': data,
        'all_emp': True,
        'employees': employees,
        'search_query': search_value  # Taaki search ke baad naam box me hi rahe
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
     
    #  office
def admin_query_search(req):

    if 'admin' not in req.session:
        return redirect('login')

    search = req.POST.get('search', '').strip()

    queries = Query.objects.all()

    if search:
        queries = queries.filter(
            name__icontains=search
        ) | queries.filter(
            email__icontains=search
        ) | queries.filter(
            subject__icontains=search
        ) | queries.filter(
            query__icontains=search
        ) | queries.filter(
            status__icontains=search
        ) | queries.filter(
            solution__icontains=search
        )

    return render(req, 'admindashboard.html', {
        'show_query': True,
        'queries': queries,
        'data': req.session.get('admin')
    })
    # office


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

        return render(req,'userdashboard.html',{'data':userdata,'query_status':True,'queries':query_data})
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
        print(s,type(s))
        # queries = Query.objects.filter(email=userdata.email,name=s)
        # queries = Query.objects.filter(email=userdata.email,name=s,query=s)
        # queries = Query.objects.filter(email=userdata.email,name__contains=s,query__contains=s)
        queries = Query.objects.filter(Q(email__contains=userdata.email)&(Q(name__contains=s)|Q(query__contains=s)))
        # queries = Query.objects.filter(Q(name__contains=s)|Q(query__contains=s)) #for admin use only


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
    
from django.db.models import Q

def user_search(req):
    if 'user_id' in req.session:
        id = req.session['user_id']
        userdata = new.objects.get(id=id)

        # 🔥 SINGLE SEARCH BOX VALUE
        search = req.POST.get('search', '').strip()

        queries = Query.objects.filter(email=userdata.email)

        # ✔ SINGLE CONDITION FOR ALL FIELDS
        if search:
            queries = queries.filter(
                Q(name__icontains=search) |
                Q(status__icontains=search) |
                Q(subject__icontains=search) |
                Q(query__icontains=search) |
                Q(solution__icontains=search)
            )

        return render(req, 'userdashboard.html', {
            'data': userdata,
            'query_status': True,
            'queries': queries
        })

    else:
        return redirect('login')


def user_reset(req):
    if 'user_id' in req.session:
        id = req.session['user_id']
        userdata = new.objects.get(id=id)
        queries = Query.objects.filter(email=userdata.email)

        return render(req, 'userdashboard.html', {'data': userdata,'query_status': True,'queries': queries
        })
    else:
        return redirect('login')


# new

from django.shortcuts import render, redirect
from .forms import AttendanceForm
from django.contrib import messages
from datetime import date
from .models import Attendance
from .forms import AttendanceForm


def mark_attendance(request):

    # purane messages clear karega
    storage = messages.get_messages(request)
    for i in storage:
        pass

    form = AttendanceForm()

    if request.method == 'POST':

        form = AttendanceForm(request.POST)

        if form.is_valid():

            employee = form.cleaned_data['employee']

            today = date.today()

            already_marked = Attendance.objects.filter(
                employee=employee,
                date=today
            ).exists()

            if already_marked:

                messages.error(
                    request,
                    f"Attendance already marked for {employee.name} today."
                )

                return redirect('mark_attendance')

            else:

                attendance = form.save(commit=False)

                from datetime import time

                # default fine
                attendance.late_fine = 0

                # employee monthly salary
                emp_salary = attendance.employee.salary

                # =========================
                # SALARY VALIDATION
                # =========================
                if emp_salary is None or emp_salary == '':

                    messages.error(
                        request,
                        f"Please add salary for {employee.name} before marking attendance."
                    )

                    return redirect('mark_attendance')

                # 1 day salary
                per_day_salary = emp_salary / 30

                # default final salary
                attendance.final_salary = per_day_salary

                # default status
                if not attendance.status:
                    attendance.status = "Present"

                if attendance.check_in_time:

                    # office timing
                    office_time = time(9, 30)

                    # 10 baje limit
                    late_limit = time(10, 0)

                    # 9:30 ke baad aur 10 ke andar
                    if (
                        attendance.check_in_time > office_time
                        and
                        attendance.check_in_time <= late_limit
                    ):

                        attendance.late_fine = 50

                        attendance.final_salary = (
                            per_day_salary - 50
                        )

                    # 10 ke baad
                    elif attendance.check_in_time > late_limit:

                        attendance.status = "Half Day"

                        # half salary cut
                        attendance.late_fine = (
                            per_day_salary / 2
                        )

                        attendance.final_salary = (
                            per_day_salary / 2
                        )

                # absent
                if attendance.status and attendance.status == "Absent":

                    attendance.final_salary = 0

                attendance.save()

                messages.success(
                    request,
                    "Attendance marked successfully."
                )

                return redirect('show_attendance')

    context = {
        'form': form,
        'attendance': True,
        'data': request.session.get('admin')
    }

    return render(
        request,
        'admindashboard.html',
        context
    )
from .models import Attendance

from datetime import date
from .models import Attendance

def show_attendance(request):

    today = date.today()

    # =========================
    # FILTERS
    # =========================

    month = request.GET.get('month')

    if month:
        month = int(month)
    else:
        month = today.month

    emp_id = request.GET.get('emp')

    search = request.GET.get('search', '').strip()

    date_filter = request.GET.get('date')

    # =========================
    # BASE QUERY
    # =========================

    base_qs = Attendance.objects.filter(
        date__month=month,
        date__year=today.year
    )

    # =========================
    # EMPLOYEE FILTER
    # =========================

    if emp_id:
        base_qs = base_qs.filter(employee_id=emp_id)

    # =========================
    # SEARCH FILTER (NEW 🔥)
    # =========================

    if search:
        base_qs = base_qs.filter(
            employee__name__icontains=search
        )

    # =========================
    # DATE FILTER (NEW 🔥)
    # =========================

    if date_filter:
        base_qs = base_qs.filter(date=date_filter)

    # =========================
    # FINAL DATA
    # =========================

    attendance = base_qs.order_by('-date')

    # =========================
    # TOTAL SALARY
    # =========================

    total_salary = sum(i.final_salary for i in attendance)

    # =========================
    # SUMMARY
    # =========================

    total_present = base_qs.filter(status="Present").count()
    total_absent = base_qs.filter(status="Absent").count()
    total_half = base_qs.filter(status="Half Day").count()
    total = base_qs.count()

    # =========================
    # PERCENTAGE
    # =========================

    percentage = 0

    if total > 0:
        percentage = (
            (total_present + (total_half * 0.5)) / total
        ) * 100

    # =========================
    # EMPLOYEE LIST
    # =========================

    employees = Attendance.objects.select_related(
        'employee'
    ).values(
        'employee__id',
        'employee__name'
    ).distinct()

    # =========================
    # CONTEXT
    # =========================

    context = {
        'attendance': attendance,
        'employees': employees,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_half': total_half,
        'percentage': round(percentage, 2),
        'month': month,
        'total_salary': round(total_salary, 2),
        'search': search,
        'date_filter': date_filter,
        'emp_id': emp_id,
    }

    return render(request, 'show_attendance.html', context)

def my_attendance(request):

    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')

    userdata = new.objects.get(id=user_id)

    attendance = Attendance.objects.filter(
        employee__email=userdata.email
    ).order_by('-date')

    total_present = attendance.filter(
        status='Present'
    ).count()

    total_absent = attendance.filter(
        status='Absent'
    ).count()

    total_half = attendance.filter(
        status='Half Day'
    ).count()

    total = attendance.count()

    percentage = 0

    if total > 0:

        percentage = (
            (total_present + (total_half * 0.5))
            / total
        ) * 100

    context = {

        'data': userdata,

        'my_attendance': True,

        'attendance': attendance,

        'total_present': total_present,

        'total_absent': total_absent,

        'total_half': total_half,

        'percentage': round(percentage, 2),

        'section': 'attendance'
    }

    return render(
        request,
        'userdashboard.html',
        context
    )


def attendance_pdf(request, emp_id):

    employee = new.objects.get(id=emp_id)

    attendance = Attendance.objects.filter(employee=employee)

    total_present = attendance.filter(status="Present").count()
    total_absent = attendance.filter(status="Absent").count()
    total_half = attendance.filter(status="Half Day").count()

    total_days = attendance.count()

    if total_days > 0:
        percentage = round((total_present / total_days) * 100, 2)
    else:
        percentage = 0

    total_salary = sum([i.final_salary for i in attendance])

    template = get_template('attendance_pdf.html')

    context = {
        'employee': employee,
        'attendance': attendance,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_half': total_half,
        'percentage': percentage,
        'total_salary': total_salary,
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'filename="{employee.name}_attendance.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

def assign_task(req):
    if 'admin' not in req.session:
        return redirect('login')
        
    admin_data = req.session.get('admin')
    all_emp = new.objects.all()
    all_tasks = Task.objects.all().order_by('-created_at')
    task_search_value = ""
    
    if req.method == 'POST':
        if 'task_search' in req.POST:
            task_search_value = req.POST.get('task_search', '').strip()
            if task_search_value:
                all_tasks = all_tasks.filter(
                    Q(title__icontains=task_search_value) |
                    Q(description__icontains=task_search_value) |
                    Q(assigned_to__name__icontains=task_search_value) |
                    Q(status__icontains=task_search_value)
                )
        else:
            title = req.POST.get('title')
            desc = req.POST.get('description')
            emp_id = req.POST.get('employee_id')
            due_date = req.POST.get('due_date')
            
            employee = new.objects.get(id=emp_id)
            
            Task.objects.create(
                title=title,
                description=desc,
                assigned_to=employee,
                due_date=due_date
            )
            
            messages.success(req, "Task Assigned Successfully!")
            return redirect('assign_task')
        
    return render(req, 'admindashboard.html', {
        'assign_task_page': True,
        'employees': all_emp,
        'tasks': all_tasks,
        'data': admin_data,
        'today': date.today(),
        'task_search_query': task_search_value 
    })

def update_task_status(req, pk):
    if 'user_id' not in req.session:
        return redirect('login')
        
    task = Task.objects.get(id=pk)
    if req.method == 'POST':
        # 1. Tumhara purana dropdown status pakadne ka logic (Waise ka waisa hi)
        new_status = req.POST.get('status')
        
        # 2. Teeno boxes se data uthaya (Waise ka waisa hi)
        completed = req.POST.get('completed_tasks', '').strip()
        pending = req.POST.get('pending_tasks', '').strip()
        issues = req.POST.get('issues_tasks', '').strip()
        
        # 3. Aaj ki live Date aur Time nikalenge string format me
        from datetime import datetime
        current_time = datetime.now().strftime("%d %b %Y | %I:%M %p")
        
        # 4. Naya report layout taiyar kiya
        new_report = f"📅 REPORT DATE: {current_time}\nStatus: {new_status}\n- Done: {completed}\n- Pending: {pending}\n- Blockers: {issues}"
        
        # 🔥 SAFEST REVERSE LOG: Naya report sabse upar dikhega, aur purana data uske NEECHE automatic khisakh jayega (Kuch delete nahi hoga)
        if task.progress_note:
            task.progress_note = f"{new_report}\n\n------\n\n{task.progress_note}"
        else:
            task.progress_note = new_report

        task.status = new_status
        task.save()
        
        messages.success(req, "Task status and progress report updated successfully!")
        
    return redirect('dashboard')

def mark_bulk_attendance(req):
    if 'admin' not in req.session:
        return redirect('login')
        
    admin_data = req.session.get('admin')
    today = date.today()
    
    # 1. Database se saare employees ki list nikalenge
    employees_list = new.objects.all().order_by('name')
    
    if req.method == 'POST':
        from datetime import time
        
        # 2. Loop chalakar har ek employee ka submitted data check karenge
        for emp in employees_list:
            status = req.POST.get(f'status_{emp.id}')
            check_in_str = req.POST.get(f'check_in_{emp.id}')
            
            # Agar us employee ke inputs form se mile hain
            if status:
                # get_or_create use karenge taaki agar aaj ki attendance pehle se bani ho toh error na aaye, update ho jaye
                attendance, created = Attendance.objects.get_or_create(
                    employee=emp,
                    date=today,
                    defaults={'status': status, 'late_fine': 0, 'final_salary': 0}
                )
                
                # Status set kiya
                attendance.status = status
                
                # Monthly salary se 1 day salary nikalne ka logic
                emp_salary = emp.salary if emp.salary else 0
                per_day_salary = emp_salary / 30
                attendance.final_salary = per_day_salary
                attendance.late_fine = 0
                
                # Check-in time parse aur late fine calculations
                if check_in_str:
                    try:
                        t_parts = check_in_str.split(':')
                        attendance.check_in_time = time(int(t_parts[0]), int(t_parts[1]))
                        
                        office_time = time(9, 30)
                        late_limit = time(10, 0)
                        
                        # 9:30 se 10:00 ke beech me ₹50 fine
                        if attendance.check_in_time > office_time and attendance.check_in_time <= late_limit:
                            attendance.late_fine = 50
                            attendance.final_salary = per_day_salary - 50
                        # 10:00 baje ke baad Half Day
                        elif attendance.check_in_time > late_limit:
                            attendance.status = "Half Day"
                            attendance.late_fine = per_day_salary / 2
                            attendance.final_salary = per_day_salary / 2
                    except ValueError:
                        pass
                
                # Absent hone par salary 0
                if attendance.status == "Absent":
                    attendance.final_salary = 0
                    
                attendance.save()
                
        messages.success(req, "Bulk attendance processed successfully for today!")
        return redirect('show_attendance')

    return render(req, 'admindashboard.html', {
        'bulk_attendance_page': True,
        'employees_list': employees_list,
        'today': today,
        'data': admin_data
    })


# from django.db.models import Q
# from django.contrib import messages

# def manage_teams(req):
#     if 'admin' not in req.session:
#         return redirect('login')
        
#     admin_data = req.session.get('admin')
    
#     # 1. Groups fetch karo
#     all_groups = ProjectGroup.objects.all().order_by('-created_at')
    
#     # 🔥 PROGRESS CALCULATION LOGIC
#     for group in all_groups:
#         tasks = Task.objects.filter(assigned_team=group)
#         total = tasks.count()
#         done = tasks.filter(status='DONE').count()
#         group.progress = (done / total * 100) if total > 0 else 0
#         # Members ke updates bhi fetch karo
#         group.recent_updates = tasks.exclude(progress_note__isnull=True).exclude(progress_note='').order_by('-created_at')[:3]

#     # Initial state
#     leader_employees = new.objects.all().order_by('name')
#     member_employees = new.objects.all().order_by('name')
#     leader_search = ""
#     member_search = ""
    
#     if req.method == 'POST':
#         # LEADER FILTER
#         if 'search_leader_btn' in req.POST:
#             leader_search = req.POST.get('search_leader', '').strip()
#             leader_employees = leader_employees.filter(name__icontains=leader_search)
            
#         # MEMBER FILTER
#         elif 'search_member_btn' in req.POST:
#             member_search = req.POST.get('search_member', '').strip()
#             member_employees = member_employees.filter(name__icontains=member_search)
            
#         # FINAL LAUNCH
#         elif 'launch_team_btn' in req.POST:
#             p_name = req.POST.get('project_name')
#             leader_id = req.POST.get('team_leader_id')
#             member_ids = req.POST.getlist('member_ids')
            
#             if p_name and leader_id:
#                 leader_emp = new.objects.get(id=leader_id)
#                 new_group = ProjectGroup.objects.create(project_name=p_name, team_leader=leader_emp)
#                 for m_id in member_ids:
#                     member_emp = new.objects.get(id=m_id)
#                     new_group.members.add(member_emp)
#                 messages.success(req, "Team Created Successfully!")
#                 return redirect('manage_teams')
            
#     return render(req, 'admindashboard.html', {
#         'manage_teams_page': True,
#         'leader_employees': leader_employees,
#         'member_employees': member_employees,
#         'groups': all_groups,
#         'leader_search_query': leader_search,
#         'member_search_query': member_search,
#         'data': admin_data,
#     })


# def user_team_workspace(req):
#     # Agar login nahi hai toh login pe bhejo
#     if 'user_id' not in req.session:
#         return redirect('login')
    
#     # User object nikalo
#     user = New.objects.filter(id=req.session['user_id']).first()
#     if not user:
#         return redirect('login')

#     # Team nikalo
#     my_team = ProjectGroup.objects.filter(members=user).first()
    
#     # User ke apne tasks
#     my_tasks = Task.objects.filter(assigned_to=user)

#     return render(req, 'user_team_workspace.html', {
#         'my_team': my_team, 
#         'data': user, 
#         'my_tasks': my_tasks, 
#         'section': 'team_workspace'
#     })

# def update_task_status(req, task_id):
#     # Try block ka use karo taaki error na aaye
#     try:
#         task = Task.objects.get(id=task_id)
#         if req.method == 'POST':
#             task.progress_note = req.POST.get('progress_note')
#             task.status = req.POST.get('status')
#             task.save()
#             messages.success(req, "Task update ho gaya!")
#     except Task.DoesNotExist:
#         messages.error(req, "Task nahi mila!")
        
#     return redirect('user_team_workspace')

# new
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from geopy.distance import geodesic
from .models import Attendance, New

def mark_attendance_page(request):
    user_id = request.session.get('user_id')
    
    # 1. Agar user login nahi hai
    if not user_id:
        return redirect('login')
    
    # 2. Safety: get() ki jagah filter().first() use karo
    # Ye crash nahi hoga agar ID nahi mili
    userdata = New.objects.filter(id=user_id).first()
    
    # 3. Agar database mein user nahi hai
    if not userdata:
        request.session.flush() # Purani session saaf karo
        return redirect('login')

    return render(request, 'userdashboard.html', {
        'section': 'mark_attendance', 
        'data': userdata
    })

def submit_attendance(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        try:
            userdata = New.objects.get(id=user_id)
            today = timezone.now().date()
            
            if Attendance.objects.filter(employee=userdata, date=today).exists():
                messages.error(request, "Aapki aaj ki attendance pehle hi lag chuki hai!")
            else:
                lat = float(request.POST.get('latitude'))
                lon = float(request.POST.get('longitude'))
                OFFICE_LOC = (22.7533, 77.7499) 
                
                distance = geodesic(OFFICE_LOC, (lat, lon)).meters
                
                if distance <= 30:
                    Attendance.objects.create(employee=userdata, date=today, status="Present")
                    messages.success(request, f"Success! Attendance marked.")
                else:
                    messages.error(request, f"Attendance failed! Office se door hain.")
        except Exception:
            messages.error(request, "Error: Location nahi mili.")
            
    return redirect('mark_my_attendance_page')