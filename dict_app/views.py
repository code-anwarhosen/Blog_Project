from django.shortcuts import render, resolve_url
from django.http import JsonResponse
from difflib import get_close_matches
import json

try:
    data = json.load(open('static/bangla_dict.json', encoding='utf8'))
except FileNotFoundError as err:
    print(err)
    
def translateThis(word):
    word = word.lower()
    word_list = []
    for key in range(len(data)):
        word_list.append(data[key]['dictionary'])
    
    if word in word_list:
        for i in range(len(data)):
            if word == data[i]['dictionary']:
                return data[i]['mean']
        

# Create your views here.
def home(request):
    return render(request, 'dictionary/dict_home.html')

def translate(request):
    word = ''
    if request.method == 'POST':
        word = request.POST.get('word')
    word = word.lower()
        
    word_list = []
    for key in range(len(data)):
        word_list.append(data[key]['dictionary'])
    recommand = ''
    try:
        word_list = filter(None.__ne__, word_list)
        recommand = get_close_matches(word, word_list)[0]
    except IndexError as err:
        print(err)
        
    if word == recommand:
        recommand = ""
        
    result = translateThis(word)
    if result == None or len(result) == 0 or result == '':
        result = ''
    if recommand == None or len(recommand) == 0:
        recommand = ''
        
    context = {
        'word': word,
        'result': result,
        'recommand': recommand,
    }
    return JsonResponse(context)

def recommand(request):
    word = ''
    if request.method == 'POST':
        word = request.POST.get('word')
    word = word.lower()
    
    result = ""
    for i in range(len(data)):
        if word == data[i]['dictionary']:
            result = data[i]['mean']
    
    context = {
        'word': word,
        'result': result,
        'recommand': "",
    }
    return JsonResponse(context)