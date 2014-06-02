import math
from chutiyapp import app

d = app.config['SEARCH_RADIUS']
R = 6378.1 #Radius of the Earth in km

def deg2rad(dlat, dlon):
    return math.radians(dlat), math.radians(dlon)

def rad2deg(rlat, rlon):
    return math.degrees(rlat), math.degrees(rlon)

def deltas(rlat, rlon):
    deltalon = d/(R*math.cos(rlat))
    deltalat = d/R
    return deltalat, deltalon

def normalize(dlat, dlon):
    dlon = dlon if dlon > -180 else 360 + dlon
    dlon = dlon if dlon <= 180 else dlon - 360
    dlat = dlat if dlat > -90 else -180 - dlat
    dlat = dlat if dlat <= 90 else 180 - dlat
    return dlat, dlon

def bounds(loc):
    rlat, rlon = deg2rad(loc['lat'], loc['lon'])
    latdelta, londelta = deltas(rlat, rlon)
    dlatlower, dlonlower = rad2deg(rlat-latdelta, rlon-londelta)
    dlatlower, dlonlower = normalize(dlatlower, dlonlower)
    dlatupper, dlonupper = rad2deg(rlat+latdelta, rlon+londelta)
    dlatupper, dlonupper = normalize(dlatupper, dlonupper)
    return {'lower': {'lat':dlatlower, 'lon':dlonlower},
            'upper': {'lat':dlatupper, 'lon':dlonupper}}
