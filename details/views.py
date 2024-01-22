from django.shortcuts import render
# from .models import details

def home(request):
    # boards = Board.objects.all()
    # return render(request, 'home.html', {'boards': boards})
        # name=chr(request.GET["name"])
        age=int(request.GET["age"])
        gender=str(request.GET["gender"])
        # print('Name:',name)
        print('Age:',age)
        print('Gender:',gender)
        return render(request, 'form.html')
