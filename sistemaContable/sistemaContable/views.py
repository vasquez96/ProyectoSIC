from django.shortcuts import render

def index(requestContext):
    modulo="index"
    return render(requestContext,"inicio.html",{"modulo":modulo})