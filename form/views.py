from django.shortcuts import render
from .models import form 

def form(request):
    # boards = Board.objects.all()
    # return render(request, 'home.html', {'boards': boards})
        # name=chr(request.GET["name"])
        # age=int(request.GET["age"])
        #gender=str(request.GET["gender"])
        # print('Name:',name)
        # print('Age:',age)
        #print('Gender:',Gender)
        return render(request, 'form.html')
