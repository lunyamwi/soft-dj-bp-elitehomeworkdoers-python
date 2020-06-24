from django.shortcuts import render

# Create your views here.
def Review(request):
    return render(request,'blog-home.html')


def ReviewDetail(request):
    return render(request,'blog-details.html')

def ChatBot(request):
    return render(request, 'chatbot.html')

def ChatRoom(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })