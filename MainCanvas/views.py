from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Drawing
import json
import numpy as np
from .gmnV0 import *


# Create your views here.

def index(request):
    """Function to return the main page of the drawing application."""

    # Editing response headers and returning the same
    response = modifiedResponseHeaders(render(request, 'MainCanvas/index.html'))
    return response


def predictDrawing(request):
    """Function to save drawing in JSON Format on POST request of the same."""

    # Saving drawing if POST request is received
    if request.method == "POST":

        # Retrieving drawing JSON Data and saving the same
        drawing = Drawing(drawingJSONText=request.POST['JSONData'])
        drawing.save()
        drawingJSON = Drawing.objects.get(id=drawing.id).drawingJSONText
        if drawingJSON != '{"points":[]}':
            drawing.image = reformatJSON(drawingJSON)
            #drawingJSONData.save('MainCanvas/static/MainCanvas/images/sketch.png')

            #image_path = 'MainCanvas/static/MainCanvas/images/sketch.png'
            prediction = predictwithkeras(drawing.image)
            # Sending context with message regarding saved location
            context = {
                "message": "Results: I think you drew a : " + str(prediction[0]) + " with a probability of : " + str(prediction[1]) + "."
            }
        else:
            # Sending context with message regarding saved location
            context = {
                "message": "Please, draw a number."
            }

        # Editing response headers and returning the same
        response = modifiedResponseHeaders(render(request, 'MainCanvas/index.html', context))
        return response

    # Returning index page if not a POST request
    else:

        # Editing response headers and returning the same
        response = modifiedResponseHeaders(render(request, 'MainCanvas/index.html'))
        return response


def modifiedResponseHeaders(response):
    """Function to modify request headers so as to allow no cached versions of web pages."""

    # Editing response headers
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    # Returning response
    return response
