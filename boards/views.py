from urllib.parse import urlencode
from django import apps
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .predict import predictdata, preprocess_input
from django.contrib.auth import authenticate
import datetime
import calendar
import random
from django.http import JsonResponse

new=None
newone=None
show=None
status=None

def home(request):
    return render(request,'home.html')


def func(value):
    if value=="yes":
        return 1
    else:
        return 0


    
def current_day_view(day):
    current_day = datetime.datetime.now().strftime('%A')
    return current_day    
def crt(Appointment_Day):
    current_day1 = datetime.datetime.strptime(Appointment_Day, '%Y-%m-%d').weekday()
    return (calendar.day_name[current_day1])         
        
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session["username"]=username
        request.session["password"]=password
        print('username',username)
        print('password',password)
        user = authenticate(username=username, password=password)
        print('user',user)
        if user is not None:
            if user.is_active:
                return redirect('form')
    return render(request, 'home.html')

def register(request):
    return render(request, 'form.html')
def chart(request):
    return render(request, 'chart.html')


def form(request):
    global new
    global newone
    global show
    global status
    print("request")
    if request.method == 'POST':
        name = str(request.POST.get("name"))
        age = (request.POST.get("age"))
        age1 = (request.POST.get("age"))
        gender = str(request.POST.get("gender"))[0]
        gender1 = str(request.POST.get("gender"))
        hypertension = (request.POST.get("hypertension"))
        hypertension1 = (request.POST.get("hypertension"))
        diabetes = (request.POST.get("diabetes"))
        diabetes1 = (request.POST.get("diabetes"))
        alcoholism = (request.POST.get("alcoholism"))
        alcoholism1 = (request.POST.get("alcoholism"))
        handicap = (request.POST.get("handicap"))
        handicap1 = (request.POST.get("handicap"))
        day =  crt(request.POST.get("Appointment_Day"))
        day1 =  crt(request.POST.get("Appointment_Day"))
        date= str(request.POST.get("Appointment_Day"))
        Clinic_Location = str(request.POST.get("Clinic_Location"))
        Clinic_Location1 = str(request.POST.get("Clinic_Location"))
        scheduled_day = current_day_view(day)
        scheduled_day1 = current_day_view(day)
        
        print('Name:',name)
        print('Age:',age)
        print('Gender:',gender[0])
        print('Hypertension:',hypertension)
        print('Diabetes:',diabetes)
        print('Alcoholism:',alcoholism)
        print('Handicap:',handicap)
        print('Appointment_Day:',(day))
        print('Appointment_Date:',(date))
        print('schedule:',scheduled_day)
        print('Clinic_Location:',Clinic_Location)
        newone = [name,gender1, age1, hypertension1, diabetes1, alcoholism1, handicap1, scheduled_day1, day1, Clinic_Location1]
        print(newone)
        new = [[gender, age, hypertension, diabetes, alcoholism, handicap, scheduled_day, day, Clinic_Location]]
        result,show,status= predictdata(new)       
        print(result)
        if result == 1:
            message  = f"The Patient {name} will not show on {date} at {Clinic_Location}"
        else:
            message  = result
        
        return render(request, 'form.html', {'result': message,'success': True})
    else:
        print("failed")
        return render(request, 'form.html')



from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@require_http_methods(["POST"])
@csrf_exempt
def registersuperuser(request):
    if request.method == 'POST':
        name = request.POST["username1"]
        password = request.POST['password1']
        print(name,password)
        from django.contrib.auth.models import User
        try:
            User.objects.create_superuser(name,name,password)
           
            return render(request, 'home.html')
        except:
            response = HttpResponse(json.dumps({'message': 'Error'}), content_type='application/json')
            response.status_code = 500
            return response 


from django.shortcuts import render
import shap
import pandas as pd
# from .models import MyModel 
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# def shap_summary_chart(request):
#     # data = MyModel.objects.all().values('field1', 'field2') 

#     # Convert data to a DataFrame
#     # df = pd.DataFrame(data)

#     # Fit your machine learning model here or load a pre-trained one
#     # Example:
#     # model = YourModel()
#     # model.fit(df[['field1', 'field2']], target)
#     # explainer = shap.Explainer(model, df[['field1', 'field2']])
#     # shap_values = explainer.shap_values(df[['field1', 'field2']])
#     shap_values=[1,21,1,1,1,1,1,1,1]
#     # Create SHAP summary plot as an image
#     shap.summary_plot(shap_values, ['gender','age','h','a','d','h','sd','ad','cl'])
#     # plt.tight_layout()

#     # Save the SHAP summary plot as an image
#     chart_image_path = "boards/static/css/shap_summary_chart.png"
#     plt.savefig(chart_image_path)

#     return render(request, 'shap_summary_chart.html', {'chart_image_path': chart_image_path})
# def get_graph():
#     # Create a new figure and plot some data
#     plt.figure()
#     x = [1,21,1,1,1,1,1,1,1]
#     y = ['gender','age','h','a','d','h','sd','ad','cl']
#     plt.plot(x, y)

#     # Save the figure to a BytesIO object
#     byte = BytesIO()
#     plt.savefig(byte, format='png')
#     byte.seek(0)
#     string = base64.b64encode(byte.read())
#     # print("encode:",string)
#     # print("decode:",string.decode('utf-8'))

#     return string.decode('utf-8')

# from django.shortcuts import render
# def graph_view(request):
  
#     graph = get_graph()

    
#     return render(request, 'graph.html', {'graph': graph})
   




def preprocess_input1(input_data):
    gender_mapping = {
        'M': 1,
        'F': 0
    }
    input_data[0] = gender_mapping.get(input_data[0], -1)

    input_data[1] = int(input_data[1])  # Convert age to integer

    day_mapping = {
        'Monday': 3,
        'Tuesday': 4,
        'Wednesday': 5,
        'Thursday': 6,
        'Friday': 0,
        'Saturday': 1,
        'Sunday': 2
    }
    input_data[6] = day_mapping.get(input_data[6], -1) 
    input_data[7] = day_mapping.get(input_data[7], -1)

    loc_mapping = {
        'Noida': 3,
        'Bengaluru': 0,
        'Chennai': 1,
        'Pune': 4,
        'Coimbatore': 2,
    }
    input_data[8] = loc_mapping.get(input_data[8], -1) 

    return input_data



# from django.shortcuts import render

# # Create your views here.
# from django.views.generic import TemplateView
# import numpy as np
# import joblib
# import shap

# # Creating views
# class EditorChartView(TemplateView):
#     template_name = 'chart.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         model = joblib.load('C:\\Users\\PAVI\\Downloads\\rf_model.pkl')
#         print("pass")
#         new=['M','21',1,0,0,0,'Sunday','Sunday','Bengaluru']
#         print("pass1")
#         new_data=preprocess_input1(new)
#         print(new_data)
#         sample_data = np.array(new_data)
#         print("pass3")
#         explainer = shap.Explainer(model)
#         shap_values = explainer.shap_values(sample_data)

#         categories = ['gender', 'age', 'Hypertension', 'Diabetes', 'Alcoholism', 'Handicap', 'Scheduleday', 'Appoinmentday', 'cliniclocation']
#         values= [shap_value.tolist() for shap_value in shap_values]    
#         shap_data = {
#             'categories': categories,
#             'values': values
#         }
#         context['shap']=shap
#         return context

from django.shortcuts import render
from django.views.generic import TemplateView
import shap
import joblib
import numpy as np
import lime
class EditorChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global new
        global newone
        global show
        global status
        model = joblib.load('C:\\Users\\PAVI\\Downloads\\rf_model.pkl')
        print("pass1")
        new_data = preprocess_input1(new[0])
        sample_data = np.array(new_data)
        print(sample_data)
        explainer = shap.Explainer(model)
        shap_values = explainer.shap_values(sample_data)

        categories = ['gender', 'age', 'Hypertension', 'Diabetes', 'Alcoholism', 'Handicap', 'Scheduleday', 'Appoinmentday', 'cliniclocation']
        values = [shap_value.tolist() for shap_value in shap_values]
        print(newone)
        lst1=[]
        lst3=[]
        if show=="will show":
            values1=values[0]
            for i in range (0,len(values1)):
                if(values1[i]>=0):
                    lst1.append(i)
                    lst3.append(values1[i])
        else:
            values1=values[1]
            for i in range (0,len(values1)):
                if(values1[i]>0):
                    lst1.append(i) 
                    lst3.append(values1[i])         
        lst2=[]
        index1=[]
        categories1=[]
        for i in range (0,len(lst1)):
            for j in range (0,len(categories)):
                if(lst1[i]==j):
                    lst2.append(categories[j])
        print("lst3",lst3)
        max = sorted(lst3, reverse=True)[:3]
        print(max) 
        for i in range (0,len(max)):
         for j in range(0,len(values1)):
            if(max[i]==values1[j]):
                index1.append(j)
        print(index1)
        for i in range (0,len(index1)):
            for j in range(0,len(categories)):
                if(index1[i]==j):
                    categories1.append(categories[j]) 
        print(categories1)               
        shap_data = {
            'categories': categories,
            'values': values,
            'newone':f'''   The Patient {newone[0]}  <b>{show}</b>  for the appointment as,<br>
                               &#11162<b>{categories1[0]}</b> ({max[0]}),<br>
                               &#11162<b>{categories1[1]} </b>({max[1]}),<br>
                               &#11162<b>{categories1[2]}</b> ({max[2]}) <br>
                            validate that the Patients <b>{status}</b> is <b>highly influenced</b> by these features.'''
        }
       
        context['shap'] = shap_data
        print(shap_data)
        print(context)
        return context






