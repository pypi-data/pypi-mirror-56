#Radiosondes classes and functions

import numpy as np
import os
os.chdir('..')
os.chdir('..')
import PyKeller.atmos_sci.atmos_refractivity as ar

class Radiosonde: #class to store the radiosonde data
    
    def __init__(self,station,year,month,day,time,PRES,HGHT,TEMP,DWPT,RELH,MIXR,DRCT,SKNT,THTA,THTE,THTV):
        self.station = station
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.PRES = PRES #Atomspheric Pressure; hPa
        self.HGHT = HGHT #Geopotential Height; m
        self.TEMP = TEMP #Temperature; C
        self.DWPT = DWPT #Dewpoint Temperature; C
        self.RELH = RELH #Relative Humidity; %
        self.MIXR = MIXR #Mixing Ratio; g/kg
        self.DRCT = DRCT #Wind Direction; degrees true
        self.SKNT = SKNT #Wind Speed; knot
        self.THTA = THTA #Potential Temperature; K
        self.THTE = THTE #Equivalent Potential Temperature; K
        self.THTV = THTV #Virtual Potential Temperature; K
        self.layers = [] #creating empty list for adding the layers object
        self.inversions = [] #creating empty list for adding the inversions object
        self.refractivity = [] #creating empty list for adding the refractivity object
    
    def add_layers(self,layers):
        self.layers = layers
    
    def add_inversions(self,inversions):
        self.inversions = inversions
        
    def add_index(self):
        self.index = self.year*10**6 + self.month*10**4 + self.day*10**2 + self.time #index is YYYYMMDDTT format
    
    def add_refractivity(self,refractivity):
        self.refractivity = refractivity
        
class Layer: #class to store a compressed layer from radiosonde
    
    def __init__(self,z_bottom,z_top,T_bottom,T_top,dwpT_bottom,dwpT_top,slope,intercept):
        self.z_bottom = z_bottom #layer bottom height
        self.z_top = z_top #layer top height
        self.T_bottom = T_bottom #temperature at layer bottom
        self.T_top = T_top #temperature at layer top
        self.dwpT_bottom = dwpT_bottom #dew point temperature at the layer bottom
        self.dwpT_top = dwpT_top #dew point temperature at the layer top
        self.slope = slope #slope of the compressed layer linear fit
        self.intercept = intercept #intercept point of the compressed layer linear fit
        
class Inversion: #class to store temperature inversion information

    def __init__(self,inv_bottom,inv_top,temp_bottom,temp_top,dwptemp_bottom,dwptemp_top,layer):
        self.inv_bottom = inv_bottom #inversion bottom
        self.inv_top = inv_top #inversion top
        self.temp_bottom = temp_bottom #temperature at the inversion bottom
        self.temp_top = temp_top #temperature at the inversion top
        self.dwptemp_bottom = dwptemp_bottom #dew point temperature at the inversion bottom
        self.dwptemp_top = dwptemp_top #dew point temperature at the inversion top
        self.layer = layer #elevated or surface based inversion
        
class Refractivity: #class to store the refractivity calculated from the radiosonde variables
    
    def __init__(self,N,M,z):
        self.N = N #refractivity, N, equals (n - 1)*10**-6, where n is the refractive index; N units (dimensionless)
        self.M = M #modified refractivity, M, assumes earth is flat; N units (dimensionless)
        self.z = z #height in relation to the refractivity, as the function is only good to 200 mb; m
        
def readtxt(fname):

    def pull_title(line): #pulling the date and time of the radiosonde
        year = int(line.split()[8])
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month = months.index(line.split()[7])+1
        day = int(line.split()[6])
        time = int(line.split()[5][0:len(line.split()[5])-1])
        return year,month,day,time
    
    def push_data(line_list,data_list,n):
        if n == 2: #the case of high pressure at the radiosonde launch point
            for j in range(0,2):
                data_list[j] = np.append(data_list[j],float(line_list[j]))
            for j in range(2,11):
                data_list[j] = np.append(data_list[j],np.nan)
        if n == 9: #if wind isn't present in the collection (speed and direction)
            k = 0
            for j in [0,1,2,3,4,5,8,9,10]:
                data_list[j] = np.append(data_list[j],float(line_list[k]))
                k = k + 1
            for j in [6,7]:
                data_list[j] = np.append(data_list[j],np.nan)
        if n == 11: #all values are tabulated
            for j in range(0,11):
                data_list[j] = np.append(data_list[j],float(line_list[j]))
        return data_list

    station = fname[len(fname)-8:len(fname)-4].upper() #retrieving the station name; note the station name must be at the end of the text file name
    file = open(fname,'r')
    lines = file.readlines()
    file.close()
    radiosondes = []
    i = 0
    while i < len(lines):
        while len(lines[i].split()) < 2:
            i = i + 1
        if lines[i].split()[1] == station: #starting the data extraction when the station name is detected; this is based on text file structure
            year,month,day,time = pull_title(lines[i])
            data_list = [[] for j in range(11)]
            i = i + 6
            while len(lines[i].split()) == 2:
                data_list = push_data(lines[i].split(),data_list,2)
                i = i + 1
            while len(lines[i].split()) == 9 or len(lines[i].split()) == 11:
                if len(lines[i].split()) == 9:
                    data_list = push_data(lines[i].split(),data_list,9)
                if len(lines[i].split()) == 11:
                    data_list = push_data(lines[i].split(),data_list,11)
                i = i + 1
            if lines[i].split()[0] == 'Station': #ending the extraction when the keyword 'Station' is detected
                radiosondeinst = Radiosonde(station,year,month,day,time,data_list[0],data_list[1],data_list[2],data_list[3],data_list[4],data_list[5],data_list[6],data_list[7],data_list[8],data_list[9],data_list[10])
                radiosondes.append(radiosondeinst)
        i = i + 1
    return radiosondes
    
def layer_fitting(z,T,dwpT,error):

    def layer_fit(z,T,beg,end,error):

        def temp_fit(x,y):
            p = np.polyfit(np.array([x[0],x[x.size-1]]),np.array([y[0],y[y.size-1]]),1)
            y_fit = np.poly1d(p)(x)
            e_fit = np.linalg.norm(y_fit-y)
            return e_fit,p
            
        e = 1
        l = end+1
        while e >= error and l-beg > 1:
            l -= 1
            e,p = temp_fit(z[beg:l+1],T[beg:l+1])
        return p,l
        
    layers = []
    z = z[~np.isnan(T)] #removing nans
    T = T[~np.isnan(T)] #removing nans
    beg = 0
    end = z.size-1
    while end-beg >= 1:
        z_bottom = z[beg]
        T_bottom = T[beg]
        dwpT_bottom = dwpT[beg]
        poly,beg = layer_fit(z,T,beg,end,error) #beg is now the returned endpoint
        z_top = z[beg]
        T_top = T[beg]
        dwpT_top = dwpT[beg]
        slope = poly[0]
        intercept = poly[1]
        layer = Layer(z_bottom,z_top,T_bottom,T_top,dwpT_bottom,dwpT_top,slope,intercept)
        layers.append(layer)
    return layers
    
def get_inversions(layers):
    
    inversions = []
    n = 0
    m = 1
    for i in range(0,len(layers)-1):
        if np.sign(layers[i].slope) == -1:
            n = n + 1
        if np.sign(layers[i].slope) == 1 and np.sign(layers[i+1].slope) == -1:
            inv_bottom = layers[n].z_bottom
            inv_top = layers[i].z_top
            temp_bottom = layers[n].T_bottom
            temp_top = layers[i].T_top
            dwptemp_bottom = layers[n].dwpT_bottom
            dwptemp_top = layers[i].dwpT_top
            if n == 0:
                layer = 'surfased based inversion'
            else:
                layer = 'elevated inversion ' + str(m)
                m += 1
            n = i + 1
            inversion = Inversion(inv_bottom,inv_top,temp_bottom,temp_top,dwptemp_bottom,dwptemp_top,layer)
            inversions.append(inversion)
    return inversions

def get_refractivity(P,z,T,w):
    N = np.zeros_like(P)
    M = np.zeros_like(P)
    T += 273.15
    w /= 1000
    for i in range(P.size):
        N[i] = ar.N_eq(P[i],T[i],w[i]*P[i]/(0.622 + w[i]))
        M[i] = ar.M_eq(N[i],z[i])
    refractivity = Refractivity(N,M,z)
    return refractivity
    
def get_radiosonde_from_text():
    file_list = []
    for file in os.listdir():
        if file.endswith('.txt'):
            file_list.append(file)
    radiosondes = []
    for file in file_list:
        radiosonde_list = readtxt(file)
        for i in radiosonde_list:
            z_flag = np.where(i.HGHT<=8000)[0]
            P_flag = np.where(i.PRES>=200)[0]
            i.add_layers(layer_fitting(i.HGHT[z_flag],i.TEMP[z_flag],i.DWPT[z_flag],0.1))
            i.add_inversions(get_inversions(i.layers))
            i.add_index()
            i.add_refractivity(get_refractivity(i.PRES[P_flag],i.HGHT[P_flag],i.TEMP[P_flag],i.MIXR[P_flag]))
            radiosondes.append(i)
    radiosondes = sorted(radiosondes, key = lambda ri: ri.index)
    return radiosondes