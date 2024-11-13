from django.shortcuts import render
import pickle
import numpy as np
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, FunctionTransformer
from django.shortcuts import render
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
global scaler
df = pd.read_csv("Herpes_Outbreak.csv")
X = df.drop(['Next_Outbreak_Days'], axis=1)
y = df['Next_Outbreak_Days']
le = LabelEncoder()
X['Gender'] = le.fit_transform(X['Gender'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
from keras.models import load_model
loaded_model = load_model('lstm_model.h5')

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def getPredictions(a,b,c,d,e,f,g,h,i,j,k,l):
    new_data = np.array([[a,b,c,d,e,f,g,h,i,j,k,l]])
    new_data_scaled = scaler.transform(new_data) 
    new_data_reshaped = np.reshape(new_data_scaled.astype(np.float32), (new_data_scaled.shape[0], 1, new_data_scaled.shape[1]))
    predicted_outcome = loaded_model.predict(new_data_reshaped)
    return int(predicted_outcome[0][0].round())


def result(request):
    email = request.GET.get('email')
    a = request.GET.get('age')
    b = request.GET.get('gender')
    c = request.GET.get('years_since_diagnosis')
    d = request.GET.get('outbreak_flag')
    e = request.GET.get('severity')
    f = request.GET.get('stress_level')
    g = request.GET.get('fatigue_level')
    h = request.GET.get('illness_flag')
    i = request.GET.get('medication_flag')
    j = request.GET.get('temperature')
    k = request.GET.get('sleep_hours')
    l = request.GET.get('days_since_last_outbreak')
    result = getPredictions(a,b,c,d,e,f,g,h,i,j,k,l)
    subject = 'HERPES OUTBREAK PREDICTION'
    message = f'Based On your Herpes Outbreak Data, The Estimated Next Outbreak Time Is {result} Days'
    from_email = 'akshithavuyyuru1@gmail.com'
    recipient_list = [email] 
    email=EmailMessage(subject, message, from_email, recipient_list)
    email.send()

    return render(request, 'result.html', {'result': result})
