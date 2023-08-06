#https://packaging.python.org/tutorials/packaging-projects/
#https://truveris.github.io/articles/configuring-pypirc/


#python3 setup.py sdist bdist_wheel
#twine upload --repository pypi dist/*

import pandas as pd
from PIL import Image
import geopandas as gpd
import base64
import progressbar
import numpy as np
from io import BytesIO
from io import StringIO
import time
import requests
import rasterio
import math
import threading
import multiprocessing
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from rasterio.features import rasterize
from geopy.distance import geodesic
import json
from skimage.transform import resize

__version__ = '0.2.2'
url = 'https://api.ellipsis-earth.com/v2'
s = requests.Session()


def logIn(username, password):
        r =s.post(url + '/account/login/',
                         json = {'username':username, 'password':password} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)



def myMaps(token = None):
    if token == None:
        r = s.get(url + '/account/mymaps')
    else:
        r = s.get(url + '/account/mymaps', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = r.json()
    return(r)

def getMapId(name, token = None):
    
    if token == None:
        r = s.get(url + '/account/mymaps')        
    else:
        r = s.get(url + '/account/mymaps', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    mapId = [map['id'] for map in r.json() if map['name'] == name]
    if len(mapId)>0:
        mapId = mapId[0]
    else:
        raise ValueError('Map not found')

    return(mapId)

    
    
def metadata(mapId, Type, token = None):

    if Type == 'mapInfo':
        if token == None:
            r = s.get(url + '/account/mymaps')
        else:
            r = s.get(url + '/account/mymaps', headers = {"Authorization":token})
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
                
        r = r.json()
        mapData = [mapData for mapData in r if mapData['id'] == mapId]
        if len(mapData)==0:
            raise ValueError('mapId not found')
        else:
            r = mapData[0]
    else:
        if token == None:
            r = s.post(url + '/metadata',
                             json = {"mapId":  mapId, 'type':Type})
        else:
            r = s.post(url + '/metadata', headers = {"Authorization":token},
                             json = {"mapId":  mapId, 'type':Type})
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
                
        r = r.json()
        
    
    return(r)



def dataTimestamps(mapId, element, dataType, className = 'all classes', token = None):
    
    if str(type(element)) == "<class 'int'>":
        Type = 'polygon'
        element = int(element)
    if str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
        element['tileX'] = int(element['tileX'])
        element['tileY'] = int(element['tileY'])
        element['zoom'] = int(element['zoom'])
    if str(type(element)) == "<class 'shapely.geometry.polygon.Polygon'>":
        Type = 'customPolygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
            
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'element': element, 'className': className}
    body = json.dumps(body)
    body = json.loads(body)

    if token == None:
        r = s.post(url + '/data/timestamps',
                         json = body)
    else:
        r = s.post(url + '/data/timestamps', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = pd.read_csv(StringIO(r.text))
    return(r)


def dataIds(mapId, elementIds, dataType, timestamp, className = 'all classes', token = None):
    timestamp = int(timestamp)
    if len(elementIds) ==0:
            raise ValueError('elementIds has length 0')
    if str(type(elementIds[0])) == "<class 'int'>":
        Type = 'polygon'
        for i in np.arange(len(elementIds)):
            elementIds[i] = int(elementIds[i])
    if str(type(elementIds[0])) ==  "<class 'dict'>":
        Type = 'tile'
        for i in np.arange(len(elementIds)):
            elementIds[i]['tileX'] = int(elementIds[i]['tileX'])
            elementIds[i]['tileY'] = int(elementIds[i]['tileY'])
            elementIds[i]['zoom'] = int(elementIds[i]['zoom'])
        
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestamp': timestamp, 'elementIds': elementIds, 'className':className}
    if token == None:
        r = s.post(url + '/data/ids',
                         json = body)
    else:
        r = s.post(url + '/data/ids', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = pd.read_csv(StringIO(r.text))
    return(r)


def dataTiles(mapId, timestamp, element, dataType, className = 'all classes', token = None):
    timestamp = int(timestamp)
    if str(type(element)) == "<class 'int'>":
        Type = 'polygon'
        element = int(element)
    if str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
        element['tileX'] = int(element['tileX'])
        element['tileY'] = int(element['tileY'])
        element['zoom'] = int(element['zoom'])
    if str(type(element)) == "<class 'shapely.geometry.polygon.Polygon'>":
        Type = 'customPolygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestamp':timestamp , 'element': element, 'className':className}
    body = json.dumps(body)
    body = json.loads(body)

    if token == None:
        r = s.post(url + '/data/tiles',
                         json = body)
    else:
        r = s.post(url + '/data/tiles', headers = {"Authorization":token},
                         json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    r = pd.read_csv(StringIO(r.text))
    return(r)



def geometryIds(mapId, layer, limit = None, xMin = None, xMax = None, yMin=None, yMax=None,  token = None):

    body = {"mapId":  mapId}

    if xMin != None:
        body['xMin'] = float(xMin)
    if xMax != None:
        body['xMax'] = float(xMax)
    if yMin != None:
        body['yMin'] = float(yMin)
    if yMax != None:
        body['yMax'] = float(yMax)
    if limit != None:
        limit = int(limit)
        body['limit'] = layer
    if layer == 'tile':
        body['type'] = 'tile'
    else:
        body['type'] = 'polygon'
        body['layer'] = layer
            
    if token == None:
        r = s.post(url + '/geometry/ids',
                         json = body)    
    else:
        r = s.post(url + '/geometry/ids', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    ids = r.json()
    return(ids)



def geometryGet(mapId, elementIds, token = None):
    
    if len(elementIds) ==0:
            raise ValueError('elementIds has length 0')
    if str(type(elementIds[0])) == "<class 'int'>":
        Type = 'polygon'
        for i in np.arange(len(elementIds)):
            elementIds[i] = int(elementIds[i])
    if str(type(elementIds[0])) ==  "<class 'dict'>":
        Type = 'tile'
        for i in np.arange(len(elementIds)):
            elementIds[i]['tileX'] = int(elementIds[i]['tileX'])
            elementIds[i]['tileY'] = int(elementIds[i]['tileY'])
            elementIds[i]['zoom'] = int(elementIds[i]['zoom'])

    if token == None:
        r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'type':Type, 'elementIds':elementIds})
    else:
        r = s.post(url + '/geometry/get',
                         json = {"mapId":  mapId, 'type':Type, 'elementIds':elementIds})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r  = gpd.GeoDataFrame.from_features(r.json()['features'])
    return(r)


def geometryDelete(mapId, polygonId, token):
    polygonId = int(polygonId)
    r= s.post(url + '/geometry/delete', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def geometryAlter(mapId, polygonId, properties, newLayerName, token):
    r = s.post(url + '/geometry/alter', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId, 'newLayerName':newLayerName, 'properties':properties})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def geometryAdd(mapId, layer, feature, token, properties = None):
    feature = gpd.GeoSeries([feature]).__geo_interface__['features'][0]
    if properties != None:
        feature['properties'] = properties
    body = {"mapId":  mapId, 'layer': layer,  'feature': feature}
    body = json.dumps(body)
    body = json.loads(body)
    r = s.post(url + '/geometry/add', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
def geoMessageIds( mapId, Type, filters = None, limit = None, token = None):
    body = {'mapId':mapId, 'type':Type}
    if limit != None:
        limit = int(limit)
        body['limit'] = limit
    if filters != None:
        body['filters'] = filters
    

    if token == None:
        r = s.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = s.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    ids = r.json()
    return(ids)
    
def geoMessageGet(mapId, Type, messageIds, token = None):    

    body = {'mapId':mapId, 'type':Type, 'messageIds':messageIds}
    if token == None:
        r = s.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = s.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    return( r.json())

def geoMessageAdd(mapId, elementId,token, replyTo = None, message = None, private= None, form = None, image=None, lon=None, lat=None, timestamp = 0): 
    
    if str(type(elementId)) == "<class 'int'>":
        Type = 'polygon'
        elementId = int(elementId)
    if str(type(elementId)) ==  "<class 'dict'>":
        Type = 'tile'
        elementId['tileX'] = int(elementId['tileX'])
        elementId['tileY'] = int(elementId['tileY'])
        elementId['zoom'] = int(elementId['zoom'])


    body = {'mapId':mapId, 'type':Type, 'elementId':elementId, 'timestamp':timestamp}
    if lon != None:
        lon = float(lon)
    if lat != None:
        lat = float(lat)
    if replyTo != None:
        body['replyTo'] = replyTo
    if message != None:
        body['message'] = message
    if private != None:
        body['private'] = private
    if form != None:
        body['form'] = form
    if image != None:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = str(base64.b64encode(buffered.getvalue()))
        img_str = 'data:image/jpeg;base64,' + img_str[2:-1]
        body['image'] = img_str
    if lon != None:
        body['x'] = lon
    if lat != None:
        body['y'] = lat
        
    r = s.post(url + '/geomessage/add', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    

def geoMessageDelete(mapId, Type, messageId, token):    
    body = {'mapId':mapId, 'type':Type, 'messageId':messageId}
    r = s.post(url + '/geomessage/delete', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    


def geoMessageImage(mapId, Type, geoMessageId, token = None):
    body = {'mapId':mapId, 'type':Type, 'geoMessageId':geoMessageId}
    if token ==None:
        r = s.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = s.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    im = Image.open(BytesIO(r.content))    
    return(im)



def rasterRaw(mapId, channels, timestamp, tileId = None, xMin = None, xMax = None, yMin = None, yMax = None, token = None):
    timestamp = int(timestamp)
    if str(type(tileId)) !=  "<class 'NoneType'>":
        tileId['tileX'] = int(tileId['tileX'])
        tileId['tileY'] = int(tileId['tileY'])
        tileId['zoom'] = int(tileId['zoom'])
        body = {'mapId':mapId, 'tileId':tileId , 'channels':channels, 'timestamp':timestamp}

        if token ==None:
            r = s.post(url + '/raster/get',
                         json = body )        
        else:
            r = s.post(url + '/raster/get', headers = {"Authorization":token},
                         json = body )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
    
        r = r.json()
        crs = r['projection']
        bounds = r['bounds']
        r_total = np.array(r['data'])
        transform = rasterio.transform.from_bounds(bounds['x1'], bounds['y1'], bounds['x2'], bounds['y2'], r_total.shape[1], r_total.shape[0])

    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either bounding box coordinates or tileId is required')
    else:
            xMin = float(xMin)
            xMax = float(xMax)
            yMin = float(yMin)
            yMax = float(yMax)

            timestamp = int(timestamp)
            if token == None:
               zoom = int(metadata(mapId, 'mapInfo')['zoom'])
            else:
               zoom = int(metadata(mapId, 'mapInfo', token = token)['zoom'])               

            
            min_x_osm_precise =  (xMin +180 ) * 2**zoom / 360 
            max_x_osm_precise =   (xMax +180 ) * 2**zoom / 360
            max_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMin/360 * math.pi  ) ) ) 
            min_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMax/360 * math.pi  ) ) )
        
            min_x_osm =  math.floor(min_x_osm_precise )
            max_x_osm =  math.floor( max_x_osm_precise)
            max_y_osm = math.floor( max_y_osm_precise)
            min_y_osm = math.floor( min_y_osm_precise)
        
            x_tiles = np.arange(min_x_osm, max_x_osm+1)
            y_tiles = np.arange(min_y_osm, max_y_osm +1)

            bar = progressbar.ProgressBar(max_value = len(x_tiles)* len(y_tiles))

            r_total = np.zeros((256*(max_y_osm - min_y_osm + 1) ,256*(max_x_osm - min_x_osm + 1),len(channels)+1))
            
            for tileX in x_tiles:
                for tileY in y_tiles:
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm
                    bar.update(x_index * len(y_tiles) + y_index)
                    tileId = {'tileX':float(tileX), 'tileY':float(tileY),'zoom':float(zoom)}
                    body = {'mapId':mapId, 'tileId':tileId , 'channels':channels, 'timestamp':timestamp}
                    if token ==None:
                        r = s.post(url + '/raster/get',
                                     json = body )        
                    else:
                        r = s.post(url + '/raster/get', headers = {"Authorization":token},
                                     json = body )
                    if int(str(r).split('[')[1].split(']')[0]) != 200:
                        raise ValueError(r.text)
            
                    r = r.json()
                    r = np.array(r['data'])
                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = r
        
            min_x_index = int(round((min_x_osm_precise - min_x_osm)*256))
            max_x_index = int(round((max_x_osm_precise- min_x_osm)*256))
            min_y_index = int(round((min_y_osm_precise - min_y_osm)*256))
            max_y_index = int(round((max_y_osm_precise- min_y_osm)*256))
            
            r_total = r_total[min_y_index:max_y_index,min_x_index:max_x_index,:]
 
            transform = rasterio.transform.from_bounds(xMin, yMin, xMax, yMax, r_total.shape[1], r_total.shape[0])
            crs = "EPSG:3857"
            bounds = {"x1":xMin,"x2":xMax,"y1":yMin,"y2":yMax} 
    


    return({'data':r_total, 'projection':crs, 'bounds':bounds, 'transform':transform})


def rasterVisual(mapId, timestampMin, timestampMax, layerName, xMin= None,xMax= None,yMin=None, yMax=None , tileId=None, downsampled = True, token = None):
    if token != None:
        token_inurl = token.replace('Bearer ', '')
    if str(type(tileId)) == "<class 'dict'>":
        tileX = int(tileId['tileX'])
        tileY = int(tileId['tileY'])
        zoom = int(tileId['zoom'])
        location = 'https://api.ellipsis-earth.com/v2/tileService/' + mapId
        im = np.zeros((256,256,4))
        timestamps = list(np.arange(timestampMin, timestampMax +1))
        timestamps.reverse()
        for timestamp in timestamps:
           if token == None:
                r = s.get(location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY))
           else:
                r = s.get( url = location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + '?token=' + token_inurl)

           if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)

           im_new = np.array(Image.open(BytesIO(r.content)))
           im[im[:,:,3] == 0,:] = im_new[im[:,:,3] == 0,:]
    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either bounding box coordinates or tileId is required')
    elif downsampled:
        xMin = float(xMin)
        xMax = float(xMax)
        yMin = float(yMin)
        yMax = float(yMax)
        body = {'mapId':mapId, 'timestampMin':timestampMin, 'timestampMax':timestampMax, 'layerName':layerName, 'xMin':float(xMin), 'xMax':float(xMax), 'yMin':float(yMin), 'yMax':float(yMax)}
        if token ==None:
            r = s.post(url + '/visual/bounds',
                         json = body )        
        else:
            r = s.post(url + '/visual/bounds', headers = {"Authorization":token},
                         json = body )
    
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        im = np.array(Image.open(BytesIO(r.content)))
    else:
            xMin = float(xMin)
            xMax = float(xMax)
            yMin = float(yMin)
            yMax = float(yMax)
            location = 'https://api.ellipsis-earth.com/v2/tileService/' + mapId

            if token == None:
               zoom = int(metadata(mapId, 'mapInfo')['zoom'])
            else:
               zoom = int(metadata(mapId, 'mapInfo', token = token)['zoom'])               
            
            min_x_osm_precise =  (xMin +180 ) * 2**zoom / 360 
            max_x_osm_precise =   (xMax +180 ) * 2**zoom / 360
            max_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMin/360 * math.pi  ) ) )
            min_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMax/360 * math.pi  ) ) )
        
            min_x_osm =  math.floor(min_x_osm_precise )
            max_x_osm =  math.floor( max_x_osm_precise)
            max_y_osm = math.floor( max_y_osm_precise)
            min_y_osm = math.floor( min_y_osm_precise)
        
            x_tiles = np.arange(min_x_osm, max_x_osm+1)
            y_tiles = np.arange(min_y_osm, max_y_osm +1)

            bar = progressbar.ProgressBar(max_value = len(x_tiles)* len(y_tiles))

            r_total = np.zeros((256*(max_y_osm - min_y_osm + 1) ,256*(max_x_osm - min_x_osm + 1),4))
            timestamps = list(np.arange(timestampMin, timestampMax +1))
            timestamps.reverse()
            
            for tileX in x_tiles:
                for tileY in y_tiles:
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm
                    bar.update(x_index * len(y_tiles) + y_index)
                    im = np.zeros((256,256,4))
                    for timestamp in timestamps:
                       if token == None:
                            r = s.get(location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY))
                       else:
                            r = s.get( url = location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + '?token=' + token_inurl)
            
                       if int(str(r).split('[')[1].split(']')[0]) != 200:
                            raise ValueError(r.text)
            
                       im_new = np.array(Image.open(BytesIO(r.content)))
                       im[im[:,:,3] == 0,:] = im_new[im[:,:,3] == 0,:]
            
                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = im
        
            min_x_index = int(round((min_x_osm_precise - min_x_osm)*256))
            max_x_index = int(round((max_x_osm_precise- min_x_osm)*256))
            min_y_index = int(round((min_y_osm_precise - min_y_osm)*256))
            max_y_index = int(round((max_y_osm_precise- min_y_osm)*256))
            
            im = r_total[min_y_index:max_y_index,min_x_index:max_x_index,:]
    
    return(im)
    
def rasterSubmit(mapId, r,  channels, timestamp, xMin = None, xMax = None, yMin = None, yMax= None, tileId = None, mask = None, token = None):
    
    if len(channels) != r.shape[2]:
        raise ValueError('length of bands must be same as channels of r')        

    if str(type(mask)) == "<class 'NoneType'>":
        mask = np.ones((r.shape[0],r.shape[1]))

    if str(type(tileId)) == "<class 'dict'>":
            tileX = int(tileId['tileX'])
            tileY = int(tileId['tileY'])
            zoom = int(tileId['zoom'])

            for j in np.arange(len(channels)):
                if channels[j] == 'label':
                    body = {'mapId':mapId, 'tileId':{'tileX':tileX, 'tileY':tileY, 'zoom':zoom}, 'timestamp':timestamp, 'Type':channels[j], 'newLabel': r[:,:,j].tolist() }
                else:
                    body = {'mapId':mapId, 'tileId':{'tileX':tileX, 'tileY':tileY, 'zoom':zoom}, 'timestamp':timestamp, 'Type':channels[j], 'newLabel': mask.tolist(), 'newData':r[:,:,j].tolist() }
            
                body = json.dumps(body)
                body = json.loads(body)
    
                if token ==None:
                    r = s.post(url + '/raster/submit',
                                 json = body )        
                else:
                    r = s.post(url + '/raster/submit', headers = {"Authorization":token},
                                 json = body )
                if int(str(r).split('[')[1].split(']')[0]) != 200:
                    raise ValueError(r.text)
    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either bounding box coordinates or tileId is required')
    else:
        xMin = float(xMin)
        xMax = float(xMax)
        yMin = float(yMin)
        yMax = float(yMax)

        if token == None:
           zoom = int(metadata(mapId, 'mapInfo')['zoom'])
        else:
           zoom = int(metadata(mapId, 'mapInfo', token = token)['zoom'])               
        
        min_x_osm_precise =  (xMin +180 ) * 2**zoom / 360 
        max_x_osm_precise =   (xMax +180 ) * 2**zoom / 360
        max_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMin/360 * math.pi  ) ) )
        min_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMax/360 * math.pi  ) ) )
    
        min_x_osm =  math.floor(min_x_osm_precise )
        max_x_osm =  math.floor( max_x_osm_precise)
        max_y_osm = math.floor( max_y_osm_precise)
        min_y_osm = math.floor( min_y_osm_precise)
    
        x_tiles = np.arange(min_x_osm, max_x_osm+1)
        y_tiles = np.arange(min_y_osm, max_y_osm +1)

        bar = progressbar.ProgressBar(max_value = len(x_tiles)* len(y_tiles))
        
        r_new = np.zeros(( (max_y_osm - min_y_osm+1)*256, (max_x_osm - min_x_osm+1)*256 ,len(channels)))
        mask_new = np.zeros(( (max_y_osm - min_y_osm+1)*256, (max_x_osm - min_x_osm+1)*256 ))
        
        min_pixy =  round((min_y_osm_precise - min_y_osm)*256)
        max_pixy = round((max_y_osm_precise - min_y_osm)*256)
        min_pixx = round((min_x_osm_precise - min_x_osm)*256)
        max_pixx = round((max_x_osm_precise - min_x_osm)*256)
        
        max_pixx = min(max_pixx, max_x_osm * 256 - 1)
        max_pixy = min(max_pixy, max_y_osm * 256 - 1)
        
        r = resize(r, (max_pixy - min_pixy,max_pixx - min_pixx), order = 0, mode = 'edge', preserve_range=True)
        mask = resize(mask, (max_pixy - min_pixy,max_pixx - min_pixx), order = 0, mode = 'edge', preserve_range=True)        
        
        r_new[ min_pixy : max_pixy , min_pixx : max_pixx , :] = r
        mask_new[ min_pixy : max_pixy , min_pixx : max_pixx ] = mask
        
        r = r_new
        mask = mask_new
        del r_new
        del mask_new
        
        for tileX in x_tiles:
            for tileY in y_tiles:
                x_index = tileX - min_x_osm
                y_index = tileY - min_y_osm
                
                bar.update(x_index * len(y_tiles) + y_index)
                
                r_sub = r[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ]
                mask_sub = mask[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ]
                
                for j in np.arange(r_sub.shape[1]):
                    if channels[j] == 'label':
                        body = {'mapId':mapId, 'tileId':{'tileX':tileX, 'tileY':tileY, 'zoom':zoom}, 'timestamp':timestamp, 'Type':channels[j], 'newLabel': r_sub[:,:,j].tolist() }
                    else:
                        body = {'mapId':mapId, 'tileId':{'tileX':tileX, 'tileY':tileY, 'zoom':zoom}, 'timestamp':timestamp, 'Type':channels[j], 'newData':r_sub[:,:,j].tolist(), 'newLabel':mask_sub.tolist() }
                    body = json.dumps(body)
                    body = json.loads(body)
                    
                    if token ==None:
                        r = s.post(url + '/raster/submit',
                                     json = body )        
                    else:
                        r = s.post(url + '/raster/submit', headers = {"Authorization":token},
                                     json = body )
                    if int(str(r).split('[')[1].split(']')[0]) != 200:
                        raise ValueError(r.text)
                


##################################################################################################################

def plotPolys(polys, xMin,xMax,yMin,yMax, alpha = None, image = None, colors = {0:(0,0,1)} , column= None):
    polys.crs = {'init': 'epsg:4326'}
    polys = polys.to_crs({'init': 'epsg:3785'})
    
    bbox = gpd.GeoDataFrame( {'geometry': [Polygon([(xMin,yMin), (xMax, yMin), (xMax, yMax), (xMin, yMax)])]} )
    bbox.crs = {'init': 'epsg:4326'}
    bbox = bbox.to_crs({'init': 'epsg:3785'})

    if str(type(image)) == "<class 'NoneType'>":
        image = np.zeros((1024,1024,4))
    image = image/255
    if column == None:
        column = 'extra'
        polys[column] = 0
    
    transform = rasterio.transform.from_bounds(bbox.bounds['minx'], bbox.bounds['miny'], bbox.bounds['maxx'], bbox.bounds['maxy'], image.shape[1], image.shape[0])
    rasters = np.zeros(image.shape)
    for key in colors.keys():
        sub_polys = polys.loc[polys[column] == key]
        if sub_polys.shape[0] >0:
            raster = rasterize( shapes = [ (sub_polys['geometry'].values[m], 1) for m in np.arange(sub_polys.shape[0]) ] , fill = 0, transform = transform, out_shape = (image.shape[0], image.shape[1]), all_touched = True )
            raster = np.stack([raster * colors[key][0], raster*colors[key][1],raster*colors[key][2], raster ], axis = 2)
            rasters = np.add(rasters, raster)
     
    rasters = np.clip(rasters, 0,1)

    image_out = rasters
    image_out[image_out[:,:,3] == 0, :] = image [image_out[:,:,3] == 0, :]
    if alpha != None:
        image_out = image * (1 - alpha) + image_out*alpha 

    image_out = image_out *255
    image_out = image_out.astype('uint8')
    return(image_out)


def chunks(l, n = 3000):
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i:i+n])
    return(result)
    
    

def parallel(function, args, callsPerMinute):
       
    
    q_result = multiprocessing.Queue()
    q_todo = multiprocessing.Queue()

    for i in np.arange(len(args)):
        q_todo.put({'args':args[i], 'key':i})

    bar = progressbar.ProgressBar(max_value = len(args))


    def single_request(function, wait):
        time.sleep(wait)
        args_new = q_todo.get()
        while args_new != 'done_and_exit':
            key = args_new['key']
            args_new = args_new['args']
            r = function(*args_new)
            q_result.put({'result':r, 'key':key})
            args_new = q_todo.get()
            if args_new != 'done_and_exit':
                time.sleep(60)

    trs = []
    for n in np.arange(callsPerMinute):
        wait =  60/callsPerMinute * n
        tr = threading.Thread(target = single_request, args = (function, wait) )
        trs = trs + [tr]
        tr.start()
        
    while q_result.qsize() != len(args):
        time.sleep(1)
        bar.update(q_result.qsize())


    for n in np.arange(callsPerMinute):
        q_todo.put('done_and_exit')
    
    for tr in trs:
        tr.join()
    
    print('joining results')
    
    result = [1 for j in np.arange(q_result.qsize())]
    for j in np.arange(q_result.qsize()):
        new = q_result.get()
        key = new['key']
        value = new['result']
        result[key] = value
        
    return(result)




def OSMcover(area, zoom ):
    def cover(area, zoom):
        if len(area) == 0:
            return(gpd.GeoDataFrame())
        x1, y1, x2, y2  = area.bounds
    
        #find the x osm tiles involved   
        x1_osm =  math.floor((x1 +180 ) * 2**zoom / 360 )
        x2_osm =  math.floor( (x2 +180 ) * 2**zoom / 360 +1)
        y2_osm = math.floor( 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y1/360 * math.pi  ) ) ) + 1)
        y1_osm = math.floor( 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y2/360 * math.pi  ) ) ))
        
        parts_x =  (x2_osm - x1_osm) + 1
        xosm_vec = [i for i in range(x1_osm, x2_osm + 1) ]
        parts_y = y2_osm - y1_osm + 1
        yosm_vec = [i for i in range(y1_osm, y2_osm + 1) ]
    
        #calculate the boundingbox coordinates of the tiles
        x1_vec = [ i * 360/2**zoom - 180  for i in np.arange( x1_osm, x2_osm +1 )  ]
        x2_vec = [i * 360/2**zoom - 180 for i in np.arange( x1_osm +1, x2_osm+2 )  ]
    
        y2_vec = [ (2* math.atan( math.e**(math.pi - (i) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)     for i in np.arange(y1_osm, y2_osm+1) ]
        y1_vec = [ (2* math.atan( math.e**(math.pi - (i) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)     for i in np.arange(y1_osm+1, y2_osm +2) ]
    
        #make a dataframe out of these boundingbox coordinates
        coords = pd.DataFrame()
        for n in np.arange( parts_y ):
           y1_sq = np.repeat(y1_vec[n], parts_x )
           y2_sq = np.repeat(y2_vec[n], parts_x )
           x1_sq = x1_vec
           x2_sq = x2_vec
           yosm_sq = np.repeat(yosm_vec[n], parts_x)
           xosm_sq = xosm_vec
           coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_sq, 'y2':y2_sq, 'xosm': xosm_sq, 'yosm': yosm_sq }
           coords = coords.append(pd.DataFrame(coords_temp))
    
        #make a geopandas out of this dataframe    
        covering = []
        for i in np.arange(coords.shape[0]):
            covering.append(Polygon([ (coords['x1'].iloc[i] , coords['y1'].iloc[i]), (coords['x2'].iloc[i], coords['y1'].iloc[i]), (coords['x2'].iloc[i], coords['y2'].iloc[i]), (coords['x1'].iloc[i], coords['y2'].iloc[i])]))
        covering = MultiPolygon(covering)    
        
        coords = gpd.GeoDataFrame({'geometry': covering, 'tileX': coords['xosm'].values, 'tileY':coords['yosm'].values})
    
        #remove all tiles that do not intersect with the orgingal area    
        keep = [area.intersects(covering[j]) for j in np.arange(len(covering))]    
        coords = coords[pd.Series(keep, name = 'bools').values]
        
        
        return(coords)

    total_covering = gpd.GeoDataFrame()
    for i in np.arange(area.shape[0]):
        area = area['geometry'].values[i]
    
        #convert to multipolygon in case of a polygon
        if str(type(area)) == "<class 'shapely.geometry.polygon.Polygon'>":
            area = MultiPolygon([area])
    
        covering = gpd.GeoDataFrame()
        
        #split the area in a western and eastern halve 
        west = Polygon([ (-180, -90), (0,-90), (0,90), (-180,90)])
        east = Polygon([ (180, -90), (0,-90), (0,90), (180,90)])
        eastern = MultiPolygon([poly.difference(west) for poly in area])
        western = MultiPolygon([poly.difference(east) for poly in area])
    
        #cover the area with tiles
        covering = covering.append(cover( western, zoom ))
        covering = covering.append(cover( eastern, zoom))               
        covering['zoom'] = zoom    

        total_covering = total_covering.append(covering)        

    total_covering = total_covering.drop_duplicates(['tileX','tileY'])
    total_covering['id'] = np.arange(total_covering.shape[0])

    return(total_covering)

def cover(area,  w):
    
    if area.shape[0] == 0:
        return(gpd.GeoDataFrame())
    
    x1 = area.bounds['minx'].min()
    x2 = area.bounds['maxx'].max()
    y1 = area.bounds['miny'].min()
    y2 = area.bounds['maxy'].max()
         
    #calculate the y1 and y2 of all squares
    step_y =  w/geodesic((y1,x1), (y1 + 1,x1)).meters
    
    parts_y = math.floor((y2 - y1)/ step_y + 1)
    
    y1_vec = y1 + np.arange(0, parts_y )*step_y
    y2_vec = y1 + np.arange(1, parts_y +1 )*step_y
    
    #make a dataframe of these bounding boxes
    steps_x = [    w/geodesic((y,x1), (y,x1+1)).meters  for y in y1_vec  ]
    parts_x = [math.floor( (x2-x1) /step +1 ) for step in steps_x ]      
    coords = pd.DataFrame()
    for n in np.arange(len(parts_x)):
        x1_sq = [ x1 + j*steps_x[n] for j in np.arange(0,parts_x[n]) ]
        x2_sq = [ x1 + j*steps_x[n] for j in np.arange(1, parts_x[n]+1) ]
        coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_vec[n], 'y2':y2_vec[n]}
        coords = coords.append(pd.DataFrame(coords_temp))
    
    #make a geopandas of this covering dataframe
    cover = [Polygon([ (coords['x1'].iloc[j] , coords['y1'].iloc[j]) , (coords['x2'].iloc[j] , coords['y1'].iloc[j]), (coords['x2'].iloc[j] , coords['y2'].iloc[j]), (coords['x1'].iloc[j] , coords['y2'].iloc[j]) ]) for j in np.arange(coords.shape[0])]
    
    coords = gpd.GeoDataFrame({'geometry': cover, 'x1':coords['x1'], 'x2':coords['x2'], 'y1':coords['y1'], 'y2':coords['y2'] })

    #remove all tiles that do not intersect the area that needed covering    
    keep = [area.intersects(coords['geometry'].values[j]) for j in np.arange(coords.shape[0])]
    coords = coords[keep]
    coords['id'] = np.arange(coords.shape[0])
        
    return(coords)


def coverBounds(xMin, xMax,yMin, yMax, zoom):
    def cover(area, zoom):
        if len(area) == 0:
            return(gpd.GeoDataFrame())
        x1, y1, x2, y2  = area.bounds
    
        #find the x osm tiles involved   
        x1_osm =  math.floor((x1 +180 ) * 2**zoom / 360 )
        x2_osm =  math.floor( (x2 +180 ) * 2**zoom / 360 +1)
        y2_osm = math.floor( 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y1/360 * math.pi  ) ) ) + 1)
        y1_osm = math.floor( 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y2/360 * math.pi  ) ) ))
        
        parts_x =  (x2_osm - x1_osm) + 1
        xosm_vec = [i for i in range(x1_osm, x2_osm + 1) ]
        parts_y = y2_osm - y1_osm + 1
        yosm_vec = [i for i in range(y1_osm, y2_osm + 1) ]
    
        #calculate the boundingbox coordinates of the tiles
        x1_vec = [ i * 360/2**zoom - 180  for i in np.arange( x1_osm, x2_osm +1 )  ]
        x2_vec = [i * 360/2**zoom - 180 for i in np.arange( x1_osm +1, x2_osm+2 )  ]
    
        y2_vec = [ (2* math.atan( math.e**(math.pi - (i) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)     for i in np.arange(y1_osm, y2_osm+1) ]
        y1_vec = [ (2* math.atan( math.e**(math.pi - (i) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)     for i in np.arange(y1_osm+1, y2_osm +2) ]
    
        #make a dataframe out of these boundingbox coordinates
        coords = pd.DataFrame()
        for n in np.arange( parts_y ):
           y1_sq = np.repeat(y1_vec[n], parts_x )
           y2_sq = np.repeat(y2_vec[n], parts_x )
           x1_sq = x1_vec
           x2_sq = x2_vec
           yosm_sq = np.repeat(yosm_vec[n], parts_x)
           xosm_sq = xosm_vec
           coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_sq, 'y2':y2_sq, 'xosm': xosm_sq, 'yosm': yosm_sq }
           coords = coords.append(pd.DataFrame(coords_temp))
    
        #make a geopandas out of this dataframe    
        covering = []
        for i in np.arange(coords.shape[0]):
            covering.append(Polygon([ (coords['x1'].iloc[i] , coords['y1'].iloc[i]), (coords['x2'].iloc[i], coords['y1'].iloc[i]), (coords['x2'].iloc[i], coords['y2'].iloc[i]), (coords['x1'].iloc[i], coords['y2'].iloc[i])]))
        covering = MultiPolygon(covering)    
        
        coords = gpd.GeoDataFrame({'geometry': covering, 'tileX': coords['xosm'].values, 'tileY':coords['yosm'].values})        
        
        return(coords)



    area = gpd.GeoDataFrame( {'geometry': [Polygon([(xMin,yMin), (xMax, yMin), (xMax, yMax), (xMin, yMax)])]} )

    total_covering = gpd.GeoDataFrame()
    for i in np.arange(area.shape[0]):
        area = area['geometry'].values[i]
    
        #convert to multipolygon in case of a polygon
        if str(type(area)) == "<class 'shapely.geometry.polygon.Polygon'>":
            area = MultiPolygon([area])
    
        covering = gpd.GeoDataFrame()
        
        #split the area in a western and eastern halve 
        west = Polygon([ (-180, -90), (0,-90), (0,90), (-180,90)])
        east = Polygon([ (180, -90), (0,-90), (0,90), (180,90)])
        eastern = MultiPolygon([poly.difference(west) for poly in area])
        western = MultiPolygon([poly.difference(east) for poly in area])
    
        #cover the area with tiles
        covering = covering.append(cover( western, zoom ))
        covering = covering.append(cover( eastern, zoom))               
        covering['zoom'] = zoom    

        total_covering = total_covering.append(covering)        

    total_covering = total_covering.drop_duplicates(['tileX','tileY'])
    total_covering['id'] = np.arange(total_covering.shape[0])

    return(total_covering)







