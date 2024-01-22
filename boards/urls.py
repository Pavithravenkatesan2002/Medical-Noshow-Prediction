from django.urls import path
from boards import views
from boards.views import EditorChartView

urlpatterns=[
 path('',views.home,name='home'),

 path('login',views.login,name='login'),
 
#  path('register',views.register,name='register'),

 path('form',views.form,name='form'),
 path("registersuperuser",views.registersuperuser,name='registersuperuser'),
#  path('graph', views.graph_view, name='graph'),
path('chart', EditorChartView.as_view(), name='index')# path('/',views.get_context_data,name=''),
#  path('chart',views.chart,name='chart'),
#  path('predict',views.predictdata,name='predictdata'),

]
