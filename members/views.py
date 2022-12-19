from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from members.models import Members
from members.models import Members_3
from members.models import Members_4
from members.models import Members_5
from members.models import Members_6

from members.models import user_table
from members.models import history
from django.urls import reverse
import pandas as pd
import numpy as np
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def add_table(request):
    user_id_request = get_user_id()
    feature = request.POST['table']  # create
    table_name = request.POST['table_name']
    max=0
    try:
        if feature=='0' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            df = pd.read_csv(myfile)
            feature = str(len(df.columns)-1)
    except:
        if feature=='0':
            feature = '2'
    for i in user_table.objects.filter(user_id=user_id_request):
        if max < i.table_id:
            max = i.table_id
    table_id = int(max)+1
    User_table = user_table(
        table_id=table_id, user_id=user_id_request, feature=feature, table_name=table_name)
    User_table.save()
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            user_id_request = get_user_id()
            t_id = user_table.objects.get(user_id=user_id_request, table_id=table_id)
            feature = t_id.feature
            t_id = t_id.id
            if feature == 2:
                for i in range(len(df)):
                    print('here')
                    print(df.iloc[i,0],df.iloc[i,1])
                    member = Members(x1=df.iloc[i,0], x2=df.iloc[i,1], y=df.iloc[i,2], table_id=t_id)
                    member.save()
            elif feature == 3:
                for i in range(len(df)):
                    member = Members_3(x1=df.iloc[i,0], x2=df.iloc[i,1], x3=df.iloc[i,2], y=df.iloc[i,3], table_id=t_id)
                    member.save()
            elif feature == 4:
                for i in range(len(df)):
                    member = Members_4(x1=df.iloc[i,0], x2=df.iloc[i,1], x3=df.iloc[i,2], x4=df.iloc[i,3], y=df.iloc[i,4], table_id=t_id)
                    member.save()
            elif feature == 5:
                for i in range(len(df)):
                    member = Members_5(x1=df.iloc[i,0], x2=df.iloc[i,1], x3=df.iloc[i,2], x4=df.iloc[i,3], x5=df.iloc[i,4], y=df.iloc[i,5], table_id=t_id)
                    member.save()
            elif feature == 6:
                for i in range(len(df)):
                    member = Members_6(x1=df.iloc[i,0], x2=df.iloc[i,1], x3=df.iloc[i,2], x4=df.iloc[i,3], x5=df.iloc[i,4], x6=df.iloc[i,5], y=df.iloc[i,6], table_id=t_id)
                    member.save()

    except:
        pass

    return HttpResponseRedirect('../../main')

def save_user_id(user_id_get):
    global user_id 
    user_id = user_id_get

def get_user_id():
    return user_id


def delete_table(request,table_id):
    user_id_request = get_user_id()
    id = user_table.objects.get(user_id=user_id_request, table_id=table_id).id
    User_table = user_table.objects.get(id=id)
    User_table.delete()
    return HttpResponseRedirect('../../main')




def register_request(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if (form.is_valid()):
                user = form.save()
                auth_login(request, user)
                messages.success(
                    request, f'Your account has been registered successfully!')
                return redirect('main')
        else:
            form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        if (request.user.is_authenticated):
            return redirect('main')
        else:
            form = AuthenticationForm(request, data=request.POST)
            if (form.is_valid()):
                username_check = form['username'].value()
                password_check = form['password'].value()
                user = authenticate(request, username=username_check,
                                    password=password_check)
                if user is not None:
                    auth_login(request, user)
                    messages.info(
                        request, f"You are now logged in as {username_check}")
                    return redirect('main/')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_request(request):
    auth_logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('main')


def main(request):
    user_id_request = 0
    if request.user.is_authenticated:
        user_id_request = request.user.id
    else:
        return redirect('..')
    save_user_id(user_id_request)
    tem = loader.get_template('main.html')
    number_table = len(user_table.objects.filter(user_id=user_id_request))

    table_name = user_table.objects.filter(user_id=user_id_request)
    context = {
        'number_table': number_table,
        'table_name' : table_name
    }
    return HttpResponse(tem.render(context, request))



def index(request, table_id, predict=0, epoch=100, learning_rate='0.001', hd='20'):
    user_id_request = get_user_id()
    tem = loader.get_template('index.html')
    t_id = user_table.objects.get(user_id=user_id_request, table_id=table_id)
    feature = t_id.feature
    if feature == 2:
        member = Members.objects.filter(table_id=t_id.id)
    if feature == 3:
        member = Members_3.objects.filter(table_id=t_id.id)
    if feature == 4:
        member = Members_4.objects.filter(table_id=t_id.id)
    if feature == 5:
        member = Members_5.objects.filter(table_id=t_id.id)
    if feature == 6:
        member = Members_6.objects.filter(table_id=t_id.id)
    history_ = history.objects.filter(table_id=t_id.id)
    context = {
        'mymember': member,
        'history': history_,
        'predict': predict,
        'table_id': table_id,
        'number_fe': t_id.feature,
        'epoch': epoch,
        'learning_rate': learning_rate,
        'hd': str(hd)+'x'+str(hd)+'x'+str(hd),
        'hd_show': hd,
    }

    return HttpResponse(tem.render(context, request))


def add(request, table_id):
    user_id_request = get_user_id()
    t_id = user_table.objects.get(user_id=user_id_request, table_id=table_id)
    feature = t_id.feature
    t_id = t_id.id
    if feature == 2:
        x1 = request.POST['x1']
        x2 = request.POST['x2']
        y = request.POST['y']
        member = Members(x1=x1, x2=x2, y=y, table_id=t_id)
        member.save()
    elif feature == 3:
        x1 = request.POST['x1']
        x2 = request.POST['x2']
        x3 = request.POST['x3']
        y = request.POST['y']
        member = Members_3(x1=x1, x2=x2, x3=x3, y=y, table_id=t_id)
        member.save()
    elif feature == 4:
        x1 = request.POST['x1']
        x2 = request.POST['x2']
        x3 = request.POST['x3']
        x4 = request.POST['x4']
        y = request.POST['y']
        member = Members_4(x1=x1, x2=x2, x3=x3, x4=x4, y=y, table_id=t_id)
        member.save()
    elif feature == 5:
        x1 = request.POST['x1']
        x2 = request.POST['x2']
        x3 = request.POST['x3']
        x4 = request.POST['x4']
        x5 = request.POST['x5']
        y = request.POST['y']
        member = Members_5(x1=x1, x2=x2, x3=x3, x4=x4,
                           x5=x5, y=y, table_id=t_id)
        member.save()
    elif feature == 6:
        x1 = request.POST['x1']
        x2 = request.POST['x2']
        x3 = request.POST['x3']
        x4 = request.POST['x4']
        x5 = request.POST['x5']
        x6 = request.POST['x6']
        y = request.POST['y']
        member = Members_6(x1=x1, x2=x2, x3=x3, x4=x4, x5=x5,
                           x6=x6, y=y, table_id=t_id)
        member.save()
    return HttpResponseRedirect('../../'+str(table_id))


def delete(request, table_id, id):
    user_id_request = get_user_id()
    feature = user_table.objects.get(
        user_id=user_id_request, table_id=table_id).feature
    if feature == 2:
        member = Members.objects.get(id=id)
    if feature == 3:
        member = Members_3.objects.get(id=id)
    if feature == 4:
        member = Members_4.objects.get(id=id)
    if feature == 5:
        member = Members_5.objects.get(id=id)
    if feature == 6:
        member = Members_6.objects.get(id=id)

    member.delete()
    return HttpResponseRedirect('../../'+str(table_id))


def edit(request, table_id):
    user_id_request = get_user_id()
    tem = loader.get_template('edit.html')
    t_id = user_table.objects.get(user_id=user_id_request, table_id=table_id)
    feature = t_id.feature
    if feature == 2:
        member = Members.objects.filter(table_id=t_id.id)
    if feature == 3:
        member = Members_3.objects.filter(table_id=t_id.id)
    if feature == 4:
        member = Members_4.objects.filter(table_id=t_id.id)
    if feature == 5:
        member = Members_5.objects.filter(table_id=t_id.id)
    if feature == 6:
        member = Members_6.objects.filter(table_id=t_id.id)
    context = {
        'mymember': member,
        'number_fe': feature,
        'table_id': table_id
    }

    return HttpResponse(tem.render(context, request))


def submit_edit(request, table_id):
    user_id_request = get_user_id()
    t_id = user_table.objects.get(user_id=user_id_request, table_id=table_id)
    feature = t_id.feature
    if feature == 2:
        member = Members.objects.filter(table_id=t_id.id)
    if feature == 3:
        member = Members_3.objects.filter(table_id=t_id.id)
    if feature == 4:
        member = Members_4.objects.filter(table_id=t_id.id)
    if feature == 5:
        member = Members_5.objects.filter(table_id=t_id.id)
    if feature == 6:
        member = Members_6.objects.filter(table_id=t_id.id)
    memall = member

    for i, item in enumerate(memall):
        if feature == 2:
            member = Members.objects.get(id=item.id, table_id=t_id.id)
        if feature == 3:
            member = Members_3.objects.get(id=item.id, table_id=t_id.id)
        if feature == 4:
            member = Members_4.objects.get(id=item.id, table_id=t_id.id)
        if feature == 5:
            member = Members_5.objects.get(id=item.id, table_id=t_id.id)
        if feature == 6:
            member = Members_6.objects.get(id=item.id, table_id=t_id.id)
        x1 = request.POST['x1_'+str(i)]
        x2 = request.POST['x2_'+str(i)]
        member.x1 = x1
        member.x2 = x2
        if feature >= 3:
            x3 = request.POST['x3_'+str(i)]
            member.x3 = x3
        if feature >= 4:
            x4 = request.POST['x4_'+str(i)]
            member.x4 = x4
        if feature >= 5:
            x5 = request.POST['x5_'+str(i)]
            member.x5 = x5
        if feature >= 6:
            x6 = request.POST['x6_'+str(i)]
            member.x6 = x6
        y = request.POST['y_'+str(i)]
        member.y = y
        member.save()
    return HttpResponseRedirect('../../../'+str(table_id))
