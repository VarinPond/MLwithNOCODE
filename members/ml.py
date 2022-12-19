import tensorflow as tf
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from members.models import Members
from members.models import Members_3
from members.models import Members_4
from members.models import Members_5
from members.models import Members_6
from members.models import history
from members.models import user_table
from django.urls import reverse
from . import views
from tensorflow import keras
from django.contrib import messages
from django.shortcuts import render, redirect
import tensorflowjs as tfjs
import os
import mimetypes

def download_file(request,table_id):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'model.json'
    # Define the full file path
    filepath = BASE_DIR + '/model_JS/'+filename
    #
    if os.path.exists(filepath):
        os.remove(filepath)
    filepath = BASE_DIR + '/model_JS/'
    tfjs.converters.save_keras_model(model, filepath)
    # Open the file for reading content
    filepath = BASE_DIR + '/model_JS/'+filename

    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

def train(request,table_id,epoch=100,learning_rate='0.001',hd='20'):
    user_id_request = 0
    if request.user.is_authenticated:
        user_id_request = request.user.id
    else:
        return redirect('main')
    t_id = user_table.objects.get(user_id=user_id_request,table_id=table_id)
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

    x=[]
    y=[]
    for o in member:
        if feature == 2:
            x  += [[o.x1,o.x2]]
        if feature == 3:
            x  += [[o.x1,o.x2,o.x3]]
        if feature == 4:
            x  += [[o.x1,o.x2,o.x3,o.x4]]
        if feature == 5:
            x  += [[o.x1,o.x2,o.x3,o.x4,o.x5]]
        if feature == 6:
            x  += [[o.x1,o.x2,o.x3,o.x4,o.x5,o.x6]]
        y  += [o.y]
    x = tf.convert_to_tensor(x)
    y = tf.convert_to_tensor(y)
    dense = int(request.POST['dense'])
    global model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(dense, activation='relu'),
        tf.keras.layers.Dense(dense, activation='relu'),
        tf.keras.layers.Dense(dense, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    lr = float(request.POST['learning_rate'])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                loss='mae',
                metrics=['mae'])

    e = int(request.POST['epoch'])
    class LossHistory(keras.callbacks.Callback):
        def on_train_begin(self, logs={}):
            self.losses = []

        def on_batch_end(self, batch, logs={}):
            self.losses.append(logs.get('loss'))
    global history_callback 
    history_callback  = LossHistory()
    model.fit(x,y,epochs=e,verbose=0, callbacks=[history_callback ])
    
    #add to history database
    global loss 
    loss = history_callback.losses[-1]
    history__ = history(epoch=e,layers=dense,lr=lr,loss=loss,table_id=t_id.id)
    history__.save()
    
    tem = loader.get_template('index.html')
    history_ = history.objects.filter(table_id=t_id.id)
    t_id = user_table.objects.get(user_id=user_id_request,table_id=table_id)
    
    context={
        'mymember': member,
        'history': history_,
        'loss' : loss,
        'table_id':table_id,
        'epoch':epoch,
        'learning_rate':learning_rate,
        'number_fe':t_id.feature,
        'hd':str(hd)+'x'+str(hd)+'x'+str(hd),
        'hd_show':hd,
    }
    messages.success(request, epoch)
    return HttpResponse(tem.render(context,request))

def predict(request,table_id,epoch=100,learning_rate='0.001',hd='20'):
    user_id_request = 0
    if request.user.is_authenticated:
        user_id_request = request.user.id
    else:
        return redirect('main')
    t_id = user_table.objects.get(user_id=user_id_request,table_id=table_id)
    feature = t_id.feature
    x_pred=[]
    if feature >= 2:
        x1_p = float(request.POST['p1'])
        x2_p = float(request.POST['p2'])
        x_pred+=[x1_p]
        x_pred+=[x2_p]
    if feature >= 3:
        x3_p = float(request.POST['p3'])
        x_pred+=[x3_p]
    if feature >= 4:
        x4_p = float(request.POST['p4'])
        x_pred+=[x4_p]
    if feature >= 5:
        x5_p = float(request.POST['p5'])
        x_pred+=[x5_p]
    if feature >= 6:
        x6_p = float(request.POST['p6'])
        x_pred+=[x6_p]
    
    x_pred = [[x_pred]]
    predict = model.predict(x_pred)[-1][-1]
    
    #tem = loader.get_template('predict.html')
    tem = loader.get_template('index.html')
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
    context={
        'predict' : predict,
        'mymember': member,
        'history': history_,
        'loss' : loss,
        'number_fe':t_id.feature,
        'table_id':table_id,
        'epoch':epoch,
        'learning_rate':learning_rate,
        'hd':str(hd)+'x'+str(hd)+'x'+str(hd),
        'hd_show':hd,
    }
    return HttpResponse(tem.render(context,request))

def delete(request,table_id):
    user_id_request = 0
    if request.user.is_authenticated:
        user_id_request = request.user.id
    else:
        return redirect('main')
    t_id = user_table.objects.get(user_id=user_id_request,table_id=table_id)
    history.objects.filter(table_id=t_id.id).delete()
    return HttpResponseRedirect('../../'+str(table_id))
