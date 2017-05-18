# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import reco_engine.reco as engine
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def dummy_json(request):
    user_id = request.GET.get('id','V_4GSrSg7AK_5wXs9TrBbg')
    lat = float(request.GET.get('lat', 43.673971))
    lon = float(request.GET.get('lon', 43.673971))
    return JsonResponse(engine.give_reco(user_id,lat,lon))
