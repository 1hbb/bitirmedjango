from django.shortcuts import render
from django.http import HttpResponse
import json

import random
from math import radians, cos, sin, asin, sqrt
from textwrap import indent
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Create your views here.

USER_LAT=0
USER_LNG= 0

def index(request):
    lat = request.GET["lat"]
    lng = request.GET["lng"]
    USER_LAT = lat
    USER_LNG = lng
    print(f'user lat = {lat} user lang = {lng}')
    
    x = randomCoordinates(float(lat), float(lng)) 
    

    response = HttpResponse(json.dumps(x), content_type="application/json")
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response;


cred=credentials.Certificate('service.json')

firebase_admin.initialize_app(cred,{

    'databaseURL':'https://python-72e0a-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref=db.reference('py/')



PARKS=5
latArray=[]
lngArray=[]
traficJam=[]
distance_Array=[]
capcityArray=[]
bestParkingSpots=[]
enMantikliArray=[]
def randomCoordinates(usr_lat, usr_lng):
    latArray.clear()
    lngArray.clear()

    lat=0
    cpcity=0
    lng=0
    for i in range(0,PARKS):
        yon=random.random()/2
        lat=random.random()/2
        lng= random.random()
        jam=random.randint(1,100)
        cpcity=random.randint(1,50)
        if(yon<0.5):
            yon=2
        else:
            yon=-2
        
        latArray.append(usr_lat+lat/yon)
        lngArray.append(usr_lng+lng/yon)
        traficJam.append(jam)
        capcityArray.append(cpcity)
       
        ref.child(f'{i+1}').set({       
            "lat":latArray[i],
            "lng":lngArray[i],
            'capacity':capcityArray[i],
            "trafficJam":traficJam[i],
            "yakinlik":0,
        })
        
      
     
      
    
    print(latArray)
    print(lngArray)
    print(f'jam={traficJam}')
    print(f'kapasite={capcityArray}')

    res = []
    calculateDistanceArray(float(usr_lat), float(usr_lng))
    findBestParkingSpot()

    for (lat,lng,cap,bestValue) in zip(latArray, lngArray,capcityArray,bestParkingSpots):
        res.append({"lat": lat, "lng": lng,"cap":cap,"best":bestValue})

    return res
    
   
   
def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def calculateDistanceArray(usr_lat, usr_lng):
    distance_Array.clear()
    for i in range (0,PARKS):
        print(i)
        distance_Array.append(distance(usr_lat,latArray[i],usr_lng,lngArray[i]))
    
    print(f'km={distance_Array}')
    

def findBestParkingSpot():
        bestParkingSpots.clear()
        for i in range (0,PARKS):
            bestParkingSpots.append(calculateBestSpot(distance_Array[i],traficJam[i],capcityArray[i]))
        print(f'best={bestParkingSpots}')
        return bestParkingSpots
  

def calculateBestSpot(km,jam,cpcty):
## km düşük jam düşük kapasite yüksek olmalı bize bir değer üretmeli
    sonuc=0
    sonuc=((cpcty)/(jam))+((cpcty)/(km))
    return sonuc