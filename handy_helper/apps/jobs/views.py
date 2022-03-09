from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User, Job
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.urlresolvers import reverse
import bcrypt

def welcome(request):
    return render(request, 'jobs/welcome.html')

def process_signup(request):
    if request.method == 'POST':
        errors =  User.objects.registration_validations(request.POST)
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect(reverse('jobs:welcome'))
        else:
            user_password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'], 
                email=request.POST['email'], password_hash=user_password_hash
            )
            user.save()
            messages.success(request, f'Successful registration', extra_tags='registration_success')
            request.session['user_id'] = str(user.id)
            return redirect(reverse('jobs:dashboard'))
    return redirect(reverse('jobs:welcome'))

def process_signin(request):
    if request.method == 'POST':
        errors =  User.objects.signin_validations(request.POST)
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags=k)
            return redirect(reverse('jobs:welcome'))
        else:
            user = User.objects.filter(email=request.POST['signin_email'])[0]
            request.session['user_id'] = str(user.id)
            messages.success(request, f'Successful Log In', extra_tags='login_success')
            return redirect(reverse('jobs:dashboard'))
    return redirect(reverse('jobs:welcome'))

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            user_jobs = Job.objects.filter(added_by=user)
            everyone_jobs = Job.objects.filter(added_by=None)
            context = {
                'user': user,
                'everyone_jobs': everyone_jobs,
                'user_jobs': user_jobs
            }
            return render(request, 'jobs/dashboard.html', context)
    return redirect(reverse('jobs:welcome'))

def new_job(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            context = {
                'user': user
            }
            return render(request, 'jobs/new_job.html', context)
    return redirect(reverse('jobs:welcome'))

def process_new_job(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors =  Job.objects.job_validations(request.POST)
            if len(errors):
                for k, v in errors.items():
                    messages.error(request, v, extra_tags=k)
                return redirect(reverse('jobs:new_job'))
            else:
                category = request.POST['category']
                if len(request.POST['other_category']) > 0: 
                    category = request.POST['other_category']
                created_by = User.objects.filter(id=request.session['user_id'])[0]
                job = Job(created_by=created_by, title=request.POST['title'], category=category,
                    description=request.POST['description'], location=request.POST['location']
                )
                job.save()
                messages.success(request, f'Successful job creation', extra_tags='new_job_success')
                return redirect(reverse('jobs:dashboard'))
    return redirect(reverse('jobs:welcome'))

@csrf_exempt
def add_job_to_user(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user = User.objects.filter(id=request.session['user_id'])
            if len(user) > 0: 
                user = user[0]
                for k, v in request.POST.items():
                    job = Job.objects.filter(id=v)[0]
                    job.added_by = user
                    job.save()
                everyone_jobs = Job.objects.filter(added_by=None)
                user_jobs = Job.objects.filter(added_by__id=request.session['user_id'])
                context = {
                    'user': user,
                    'everyone_jobs': everyone_jobs,
                    'user_jobs': user_jobs
                }
                return render(request, 'jobs/job_tables.html', context)
    return redirect(reverse('jobs:welcome'))

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect(reverse('jobs:welcome'))

@csrf_exempt
def remove_job(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            for k, v in request.POST.items():
                Job.objects.filter(id=v)[0].delete()
            everyone_jobs = Job.objects.filter(added_by=None)
            user_jobs = Job.objects.filter(added_by__id=request.session['user_id'])
            context = {
                'user': user,
                'everyone_jobs': everyone_jobs,
                'user_jobs': user_jobs
            }
            return render(request, 'jobs/job_tables.html', context)
    return redirect(reverse('jobs:welcome'))

def edit_job(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            job = Job.objects.filter(id=id)
            if len(job) > 0: 
                job = job[0]
                if job.created_by == user:
                    context = {
                        'user': user,
                        'job': job
                    }
                    return render(request, 'jobs/edit_job.html', context)
            return redirect(reverse('jobs:dashboard'))
    return redirect(reverse('jobs:welcome'))

def process_job_edit(request, id):
    if 'user_id' in request.session:
        if request.method == 'POST':
            errors =  Job.objects.job_validations(request.POST)
            if len(errors):
                for k, v in errors.items():
                    messages.error(request, v, extra_tags=k)
                return redirect(reverse('jobs:edit_job', kwargs={'id':id}))
            else:
                job = Job.objects.filter(id=id)
                if len(job) > 0: 
                    job = job[0]
                    job.title = request.POST['title']
                    job.description = request.POST['description']
                    job.location = request.POST['location']
                    job.save()
                    messages.success(request, f'Successful job edit', extra_tags='edit_job_success')
                    return redirect(reverse('jobs:dashboard'))
    return redirect(reverse('jobs:welcome'))

def view_job(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            job = Job.objects.filter(id=id)
            if len(job) > 0: 
                job = job[0]
                context = {
                    'user': user,
                    'job': job
                }
                return render(request, 'jobs/view_job.html', context)
            return redirect(reverse('jobs:dashboard'))
    return redirect(reverse('jobs:welcome'))

def add_user_job(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            job = Job.objects.filter(id=id)
            if len(job) > 0: 
                job = job[0]
                if job.added_by == None:
                    job.added_by = user
                    job.save()
                    return redirect(reverse('jobs:view_job', kwargs={'id':id}))
    return redirect(reverse('jobs:welcome'))

@csrf_exempt
def giveup_job(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            for k, v in request.POST.items():
                job = Job.objects.filter(id=v)[0]
                job.added_by = None
                job.save()
            everyone_jobs = Job.objects.filter(added_by=None)
            user_jobs = Job.objects.filter(added_by__id=request.session['user_id'])
            context = {
                'user': user,
                'everyone_jobs': everyone_jobs,
                'user_jobs': user_jobs
            }
            return render(request, 'jobs/job_tables.html', context)
    return redirect(reverse('jobs:welcome'))

def giveup_the_job(request, id):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if len(user) > 0: 
            user = user[0]
            job = Job.objects.filter(id=id)
            if len(job) > 0: 
                job = job[0]
                job.added_by = None
                job.save()
                return redirect(reverse('jobs:view_job', kwargs={'id':id}))
    return redirect(reverse('jobs:welcome'))