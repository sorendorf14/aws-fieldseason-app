#!/usr/bin/python
#
########################################################################
# FILENAME: cal_file_setup.py                                  Nov. 2024
#
# PURPOSE: Code has dictionary of information about the iridium stations
# and extracts information from the cal file  and makes it readable to 
# to use in other code.
#
# AUTHOR: Sophie Orendorf
#         Antarctic Meteorological Research and Data Center
#         Space Science and Engineering Center
#         University of Wisconsin-Madison
#
########################################################################
# MODIFICATION HISTORY
#
# Created
# S. Orendorf Nov 2024
# Edited to add battery meteorogram information 
# S. Orendorf Oct 2025
# Added Siple Dome
# S. Orendorf Nov 2025
#
########################################################################

from datetime import datetime, timedelta
import pandas as pd
import numpy as np 
import csv
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
mpl.use('Agg')

cal_file = '/home/amrc/aws/aws_calibration/cal_file/calib2010.txt'
#cal_file = '/Users/sorendorf/Desktop/calib2010.txt'


stn_dict = {'Minna Bluff':{'bat_cols':[1,23],'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)  LAT(deg)  LON(deg)','Column_Names':['time', 'temperature', 'humidity', 'pressure', 'windspeed','winddir','voltage'],"Columns":[1,2,4,8,6,9,11,23] ,'volt_ind':7,'space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----  --------  --------', 'tlo_bool':1, 'tup_bool':1 ,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1,'rh_ind':3,'spd_ind':5,'wdir_ind':6,'p_ind':4,'temp_bool':1,'temp_ind':1,'time_ind':0,'tup_ind':1,'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            'Cape Bird':{'bat_cols':[1,23],'HEADER': 'STATION JulianDate Time(HHMMSS)      T(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)  LAT(deg)  LON(deg)','Column_Names':['time', 'temperature', 'humidity', 'pressure', 'windspeed','winddir','panel_temp','voltage'],"Columns":[1,7,8,6,9,11,23] ,'volt_ind':6,'space':'------- ---------- ------------      ----     -----  --------  --------     -----  --------  --------', 'temp_bool':1 ,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1,'rh_ind':2,'spd_ind':4,'wdir_ind':5,'p_ind':3,'time_ind':0,'temp_ind':2, 'panelt_bool':1,'panelt_ind':6,'wind_mfactor':1.0, 'volt_bool':1},
            'Cape Hallett': {'bat_cols':[1,25],'HEADER':'STATION JulianDay Time(HHMMSS)  T(C)  P(MB)  SPD(MPS) DIR(DEG) RH(%) LAT(deg) LON(deg)', 'Column_Names': ['time', 'temperature', 'humidity',' pressure', 'windspeed','winddir','voltage'], 'space':'------- ---------- -----------  ------ ------ -------- -------- ----- -------- --------' , 'Columns':[1,2,5,4,7,8,25],'volt_ind':6, 'temp_bool':1 ,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1,'rh_ind':2,'spd_ind':4,'wdir_ind':5,'p_ind':3,'time_ind':0,'temp_ind':1, 'wind_mfactor':1.0, 'volt_bool':1},
            'Alexander (TT!)': {'bat_cols':[1,3],'Column_Names':['time', '1m temp', '2m temp', '4m temp', '7.5m temp', '15m temp', '30m temp', 'pressure', '1.3m wspd', '2.4m wspd', '4m wspd', '4m wdir', '7.5m wspd', '7.5m wdir', '15m wspd', '15m wdir', '30m wspd', '30m wdir', '7.5m RH', '30m RH', 'ADG', '30m net SW', '30m net LW','voltage'],'Columns':[1,9,8,7,6,5,4,10, 12,13,17,21,16,20,15,19,14,18, 25,24,28,22,23,3] , 'Header':'STATION JulianDate Time(HHMMSS)    T1m(C)    T2m(C)    T4m(C)    T7m(C)   T15m(C)   T30m(C)     P(MB)     SPD1m     SPD2m    SPD4m      DIR4m     SPD7m     DIR7m    SPD15m    DIR15m    SPD30m    DIR30m   RH7m(%)  RH30m(%)    ADG(M)  SW(Wm^2)  LW(Wm^2)  LAT(deg)  LON(deg)', 'temp_bool':1 ,'t1_bool':1, 't2_bool':1 , 't4_bool':1 , 't7_bool':1 , 't15_bool':1 , 't30_bool':1  ,'ws1_bool':1,'wspd_bool':1 ,'rh_bool':1, 'temp_bool':1 ,'ws2_bool':1,'ws4_bool':1,'ws7_bool':1,'ws15_bool':1,'ws30_bool':1 , 'wd4_bool':1 ,'wdir_bool':1,'wd7_bool':1 ,'wd15_bool':1,'wd30_bool':1  ,'pres_bool': 1,'rh7_bool':1,'rh30_bool':1,'sw_bool':1,'lw_bool':1,'adg_bool':1,'space':'------- ---------- ------------    ------    ------    ------    ------   -------   -------     -----     -----     -----    ------     -----     -----     -----    ------    ------    ------    ------   -------  --------    ------  --------  --------  --------  --------','volt_ind':23,'rh_ind':18,'spd_ind':10,'wdir_ind':11,'p_ind':7,'time_ind':0,'temp_ind':3, 'wind_mfactor':1.0, 'volt_bool':1},# tall tower
            'Linda':{'bat_cols':[1,23],'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M) RAD(Wm^2)  LAT(deg)  LON(deg)', 'Columns':[1,2,27,6,9,11,8,22,16,23],'volt_ind':9,'Column_Names':['time', 'upper temperature', 'lower temperature from skin temperature sensor', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage'] ,'space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----    ------ ---------  --------  --------', 'temp_bool':1 ,'adg_bool':1 ,'tup_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'solar_bool': 1,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            'Lorne':{'bat_cols':[1,23],'Column_Names':['time', 'upper temperature', 'lower temperature', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage'],'Columns':[1,2,4,6,9,11,8,22,16,23],'volt_ind':9, 'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M) RAD(Wm^2)  LAT(deg)  LON(deg)','space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----    ------ ---------  --------  --------','adg_bool':1 ,'tup_bool':1 ,'temp_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'solar_bool': 1,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            'Marble Point II':{'bat_cols':[1,23],'Column_Names':['time', 'upper temperature', 'lower temperature', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage'],'Columns':[1,2,4,6,9,11,8,22,16,23],'volt_ind':9, 'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M) RAD(Wm^2)  LAT(deg)  LON(deg)','space':'------- ---------- ------------    ------   -------    ------  --------  --------     -----    ------ ---------  --------  --------', 'adg_bool':0 ,'temp_bool':1 ,'tup_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'solar_bool': 1,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            'Phoenix':{'bat_cols':[1,23],'Column_Names':['time', 'upper temperature', 'lower temperature', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage'],'Columns':[1,2,4,6,9,11,8,22,16,23],'volt_ind':9, 'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M) RAD(Wm^2)  LAT(deg)  LON(deg)','space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----    ------ ---------  --------  --------', 'adg_bool':0 ,'tup_bool':1 ,'temp_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'solar_bool': 0,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            'Windless Bight':{'bat_cols':[1,23],'Column_Names':['time', 'upper temperature', 'lower temperature', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage'],'Columns':[1,2,4,6,9,11,8,22,16,23],'volt_ind':9, 'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M) RAD(Wm^2)  LAT(deg)  LON(deg)','space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----    ------ ---------  --------  --------', 'adg_bool':1 ,'tup_bool':1 ,'temp_bool':1 ,'tlo_bool':1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool':1,'rh_bool':1 ,'solar_bool': 1,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            'White Island':{'bat_cols':[1,23],'Column_Names':['time', 'upper temperature', 'lower temperature', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage'],'Columns':[1,2,4,6,9,11,8,22,16,23],'volt_ind':9, 'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M) RAD(Wm^2)  LAT(deg)  LON(deg)','space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----    ------ ---------  --------  --------', 'adg_bool':0 ,'tup_bool':1 ,'temp_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'solar_bool': 0 ,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0 , 'volt_bool':1},
            
            'Elijah Tall Tower': {'bat_cols':[1,3],'Column_Names':['time', '1m temp', '2m temp', '4m temp', '7.5m temp', '15m temp', '30m temp', 'pressure', '1.3m wspd', '2.4m wspd', '4m wspd', '4m wdir', '7.5m wspd', '7.5m wdir', '15m wspd', '15m wdir', '30m wspd', '30m wdir', '7.5m RH', '30m RH', 'ADG', '30m net SW', '30m net LW','voltage'],'Columns':[1,9,8,7,6,5,4,10, 16,22,15,21,14,20,13,19,12,18,11,17,30,28,26,24,33,38,39,44,45,37,3] ,'volt_ind':30, 'Header':'STATION JulianDate Time(HHMMSS)    T1m(C)    T2m(C)    T4m(C)    T7m(C)   T15m(C)   T30m(C)     P(MB)     SPD1m    DIR1m      SPD2m     DIR2m     SPD4m     DIR4m     SPD7m     DIR7m    SPD15m    DIR15m    SPD30m    DIR30m   RH4m(%)   RH7m(%)  RH15m(%)  RH30m(%)    ADG(M)  SW(Wm^2)  LW(Wm^2)  LAT(deg)  LON(deg)', 'temp_bool':1 ,'temp_ind':2,'spd_ind':10 ,'p_ind':7 ,"time_ind":1 ,'wdir_ind':11 ,'rh_ind':20 ,'t1_bool':1, 't2_bool':1 , 't4_bool':1 , 't7_bool':1 , 't15_bool':1 , 't30_bool':1  ,'ws1_bool':1,'wspd_bool':1 ,'rh_bool':1,'ws2_bool':1,'ws4_bool':1,'ws7_bool':1,'ws15_bool':1,'ws30_bool':1 ,'wspd_bool':1,'wdir_bool':1, 'wd1_bool':1,'wd2_bool':1,'wd4_bool':1 ,'wdir_bool':1,'wd7_bool':1 ,'wd15_bool':1,'wd30_bool':1  ,'pres_bool':1,'rh_bool':1,'rh4_bool':1,'rh7_bool':1,'rh15_bool':1,'rh30_bool':1,'sw_bool':1,'lw_bool':1,'adg_bool':1,'volt_ind':30, 'space':'------- ---------- ------------    ------    ------    ------    ------   -------   -------     -----     -----    -----      -----     -----     -----     -----     -----     -----    ------    ------    ------    ------   -------   -------  --------  --------    ------  --------  --------  --------  --------', 'wind_mfactor':1.0, 'volt_bool':1}, # tall tower
            'Sarah': {'HEADER':'STATION JulianDate Time(HHMMSS)    TupPRT Tuptherm1 Tuptherm2 Tlotherm3     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)  LAT(deg)  LON(deg)','Columns':[0,1,3,5,7,10,12,15,16],'Column_Names':['time', 'upper temperature prt', 'upper temperature thermistor 1','upper temperature thermistor 2', 'lower temperature thermistor 3', 'pressure', 'windspeed', 'winddir', 'humidity','voltage'], 'space':'------- ---------- ------------    ------ --------- --------- ---------     -----  --------  --------     -----  --------  --------','tup_bool':1 , 'temp_bool':1,'tlo_bool':1,'wspd_bool':1 ,'wdir_bool':0 ,'pres_bool': 1,'rh_bool':1, 'wind_mfactor':1,'rh_ind':6,'spd_ind':7,'wdir_ind':8,'p_ind':5,'time_ind':0,'tup_prt_ind':1,'tup_therm1_ind':2,'tup_therm2_ind':3,'tlo_therm3_ind':4,'wind_mfactor':1.0, 'volt_bool':1},
            'Skomik': {'HEADER':'STATION JulianDate Time(HHMMSS)    TupPRT Tuptherm1 Tuptherm2 Tlotherm3     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)  LAT(deg)  LON(deg)','Columns':[0,1,3,5,7,10,12,15,16],'Column_Names':['time', 'upper temperature prt', 'upper temperature thermistor 1','upper temperature thermistor 2', 'lower temperature thermistor 3', 'pressure', 'windspeed', 'winddir', 'humidity','voltage'], 'space':'------- ---------- ------------    ------ --------- --------- ---------     -----  --------  --------     -----  --------  --------','tup_bool':1 , 'temp_bool':1,'tlo_bool':1,'wspd_bool':1 ,'wdir_bool':0 ,'pres_bool': 1,'rh_bool':1, 'wind_mfactor':1,'rh_ind':6,'spd_ind':7,'wdir_ind':8,'p_ind':5,'time_ind':0,'tup_prt_ind':1,'tup_therm1_ind':2,'tup_therm2_ind':3,'tlo_therm3_ind':4, 'wind_mfactor':1.0, 'volt_bool':1},
            
            
            'Siple Dome' : {'bat_cols':[1,23],'Column_Names':['time', 'upper temperature', 'lower temperature', 'pressure', 'windspeed', 'winddir', 'humidity', 'adg', 'solarirradiance','voltage','sw_in','sw_out','lw_in','lw_out'],'Columns':[1,2,4,6,9,11,8,22,16,23,27,28,31,32],'volt_ind':9, 'HEADER': 'STATION JulianDate Time(HHMMSS)    Tup(C)   Tlow(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)    ADG(M)  SW(Wm^2)  LW(Wm^2)  LAT(deg)  LON(deg)','space':'------- ---------- ------------    ------   -------     -----  --------  --------     -----  -------- ---------  --------  --------', 'adg_bool':1 ,'tup_bool':1 ,'temp_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'solar_bool': 1,'rh_ind':6,'spd_ind':4,'wdir_ind':5,'p_ind':3,'adg_ind':7,'solar_ind':8,'time_ind':0,'temp_ind':1, 'tup_ind':1 , 'tlo_ind':2, 'wind_mfactor':1.0, 'volt_bool':1},
            
            'Willie Field':{'bat_cols':[1,23],'HEADER':'STATION  JulianDay Time(HHMMSS)    T10min Tasp10min  Tlo10min     Tinst Tasp_inst  Tlo_inst     T1min Tasp_1min  Tlo_1min     P(MB)  SPD10min  DIR10min   SPDinst   DIRinst    SPD2min  DIR2min     RH(%)  LAT(deg)  LON(deg)', 'Columns':[1,2,3,4,5,6,8,9,11,13,14,15,17,18,19,26,27,30,31,32,33,34,36,23],'Column_Names':['time', '10minavg_asp_temp','inst_asp_temp','10minavg_temp','inst_temp', 'pres','RH_hmp','10minavg_horz_wspd', '10minavg_wdir', '10min_max_wspd', '10min_max_wdir', 'avg_panel_temp','inst_wspd','inst_wdir', 'inst_panel_temp', 'inst_tlo','10minavg_tlo','1minavg_asp_temp','1minavg_temp','1min_avg_tlo','1min_pres_avg','2minavg_wspd', '2minavg_wdir','voltage'] ,'space':'-------  --------- ------------    ------ ---------  --------     ----- ---------  --------     ----- ---------  --------     -----  --------  --------   -------   -------    -------  -------     -----  --------  --------', 'temp_bool':1 ,'tup_bool':1 ,'tlo_bool': 1,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1 ,'time_ind':0,'temp_ind':18,'p_ind':20,'spd_ind':21,'wdir_ind':22 ,'rh_ind':6, 'wind_mfactor':1.0, 'volt_bool':1,'volt_ind':23},
            'MATC':{'bat_cols':[1,2],'HEADER': 'STATION JulianDate Time(HHMMSS)      T(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)  LAT(deg)  LON(deg)','Column_Names':['time', 'temperature', 'humidity', 'pressure', 'windspeed','winddir','voltage'],"Columns":[1,7,5,3,8,9,2] ,'volt_ind':6,'space':'------- ---------- ------------      ----     -----  --------  --------     -----  --------  --------', 'temp_bool':1 ,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1,'rh_ind':2,'spd_ind':4,'wdir_ind':5,'p_ind':3,'time_ind':0,'temp_ind':1,'volt_bool':1,'wind_mfactor':1.0},
            'MATC PCWS':{'bat_cols':[1,23],'HEADER': 'STATION JulianDate Time(HHMMSS)      T(C)     P(MB)  SPD(MPS)  DIR(DEG)     RH(%)  LAT(deg)  LON(deg)','Column_Names':['time', 'temperature', 'humidity', 'pressure', 'windspeed','winddir','voltage'],"Columns":[0,1,12,10,17,18,23] ,'space':'------- ---------- ------------      ----     -----  --------  --------     -----  --------  --------', 'temp_bool':1 ,'wspd_bool':1 ,'wdir_bool':1 ,'pres_bool': 1,'rh_bool':1,'rh_ind':2,'spd_ind':4,'wdir_ind':5,'p_ind':3,'time_ind':0,'temp_ind':1, 'volt_bool':1,'volt_ind':6,'wind_mfactor':1.0},
             }

id_list = []
name_list = []
lat_list = []
lon_list = []
el_list = []
short_list = []
date_list = []
cal_df = pd.DataFrame(columns=['ID','Name','Short_Name','Date','Lat','Lon','Elevation'])
final_cal_df = pd.DataFrame(columns=['ID','Name','Short_Name','Date','Lat','Lon','Elevation'])
ird_stn_df = pd.DataFrame(columns=['ID','Name','Short_Name','Date','Lat','Lon','Elevation'])

clock=dt.datetime.today()
clockdate=clock.strftime("%Y-%m-%d")
clockyear=clockdate[:4]
clockmonth=clockdate[5:7]
clockday=clockdate[8:10]
clockhour=clock.strftime("%H")

with open(cal_file, 'r') as f2:
    num_aws = int(f2.readline()[-4:].strip())
    print("Number of AWS: "+str(num_aws))
    for line in f2:  
        if not line.startswith("C"):
            if len(line) == 84 :
                stn_id = line[0:5].strip()
                date=line[6:13]
                stn_name=line[14:35].strip()
                lat=line[37:44]
                lon=line[45:53]
                elevation = line[55:60].strip()
                el_list.append(elevation)
                date_list.append(date)
                lon_list.append(lon)
                lat_list.append(lat)
                name_list.append(stn_name)
                id_list.append(stn_id)
                
            elif len(line) == 80 or len(line) == 81:
                short_stn_name=line[-5:].strip()
                if len(short_stn_name) == 0:
                    pass
                else:
                    short_list.append(short_stn_name) 
            elif len(line) == 86 or len(line)==85:
                short_stn_name=line[-10:-7]
                short_list.append(short_stn_name)            
            
    cal_df['Elevation'] = el_list
    cal_df["Lon"] = lon_list
    cal_df["Lat"] = lat_list
    cal_df["ID"]=id_list
    cal_df["Name"]=name_list
    cal_df["Date"]=date_list
    cal_df['Short_Name']= short_list

final_cal_list = []
grouped_byid = cal_df.groupby('ID', sort=False) 
keys = list(grouped_byid.groups.keys()) 
for key in keys:
    id_group = grouped_byid.get_group(key)
    last_id = id_group.iloc[-1]
    final_cal_list.append(last_id)
final_cal_df = pd.DataFrame.from_records(final_cal_list)
ird_stn_list = []
non_ird = ['9116','9018', '99808']
final_cal_df['ID'].isin(non_ird)
ird_stn_df = final_cal_df[~final_cal_df['ID'].isin(non_ird)]
ird_stn_df = ird_stn_df.drop_duplicates(subset='Name', keep='last')

 #convert lat lon from cal file to the mcidas conventions (western hem = +, remove letter descriptions)
lat_mcidas = "-" + (ird_stn_df['Lat'].str[:-1])+'0'
e_lon_mcidas = '-'+(ird_stn_df['Lon'][ird_stn_df['Lon'].str.contains('E')].str[:-1])+'0'
w_lon_mcidas = (ird_stn_df['Lon'][ird_stn_df['Lon'].str.contains('W')].str[:-1])+'0'
e_lon = (ird_stn_df['Lon'][ird_stn_df['Lon'].str.contains('E')].str[:-1])+'0'
w_lon = '-'+(ird_stn_df['Lon'][ird_stn_df['Lon'].str.contains('W')].str[:-1])+'0'

ird_stn_df['Lat_mcidas'] = lat_mcidas
#ird_stn_df['Lat_nolabel'] = lat_mcidas
ird_stn_df['Lon_mcidas'] = pd.concat([e_lon_mcidas, w_lon_mcidas])

ird_stn_df['Lon_nolabel'] = pd.concat([e_lon, w_lon])


ird_stns_info = ird_stn_df.set_index('Name')
ird_stns_info.loc['Sarah'] = ['99613','SRH','2025001','77.868S','166.898E','9.0','-77.8680','-166.8980','166.8980']
ird_stns_info.loc['Skomik'] = ['99614','SKM','2025001','79.794S','170.452E','54.0','-79.7940','-170.4520','170.4520']
ird_stns_info.loc['MATC'] = ['99699','MAA','2023001','43.233N','89.583W','262.1','43.233','89.5830','-89.5830']
ird_stns_info.loc['MATC PCWS'] = ['99698','MAP','2023001','43.233N','89.583W','262.1','43.233','89.5830','-89.5830']

print(ird_stns_info)