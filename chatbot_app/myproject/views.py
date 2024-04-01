from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from myproject.my_swag_bot import SwagBot  # import your chatbot module

def index(request):
    """Render the index page"""
    return render(request, 'index.html')



def chatbot_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        swag_bot = SwagBot()  # initialize your chatbot
        response = swag_bot.process_message(message)  # process user message with your chatbot
        data = {'response': response}
        return JsonResponse(data)
    else:
        return render(request, 'chat.html')  # render a chat page with a form for user input
