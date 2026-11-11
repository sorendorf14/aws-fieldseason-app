#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################
# FILENAME: fieldszn_talltower.py                          Apr. 2025
#
# PURPOSE: 
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
# S. Orendorf March 2026
#
#
########################################################################

import numpy as np 
import pandas as pd 
from dash import dcc, html, Input, Output, dash_table, callback, Dash, State, ALL 
import dash 
import fpdf
from fpdf import FPDF
#import pypdf as pdf
import datetime as dt
from datetime import datetime, timedelta #import cal_file_setup #from cal_file_setup import df import csv import datetime as dt
import dash_bootstrap_components as dbc
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

figure_path = r'/Users/username/Pictures/'
pdf_output_path = r'/Users/username/Desktop/'

red_button_style = {'color': 'white', 'background-color': 'red','width':'10'}
default_button_style = {'color': 'black', 'background-color': 'lightgray','width':'10'}

sheet=['https://codepen.io/chriddyp/pen/bWLwgP.css'] #external_stylesheets=sheet
app = Dash(__name__,suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'content':'width=device-width'}] )

app.layout =dbc.Container(
        [dbc.Row(html.H1(['AWS Field Season App - Tall Tower Version'], className='text-center')),
        dbc.Row([
            dbc.Col([
                html.Label(html.B(['Station Name: '])) ,
                dcc.Input(placeholder='Enter name', type='text',value='',id='stn-name', debounce=False, autoComplete='on',size='20', style={'margin-left':'10px'},persistence=True)])
            ]),
        html.Br(),
        dbc.Row([dbc.Col([
                html.Label(html.B(['Date (MM/DD/YYYY): '])),
            
                dcc.Input(placeholder='Enter date', type='text',value='',id='date', debounce=False, autoComplete='on',size='20', style={'margin-left':'10px'},persistence=True ),
                ])]),
         html.Br(),
         dbc.Row([dbc.Col([html.Label('Departure Time (from base to AWS, HHMM, 24 hour time): ', style={'margin-left':'50px'} ), #,persistence_type='session'
                         dcc.Input(placeholder='enter time',type='text',id='depart-base-time', style={'margin-left':'10px'},persistence=True)]),
                         
                dbc.Col([html.Label('Arrival Time (to AWS, HHMM):' ),
                         dcc.Input(placeholder='enter time',type='text',id='arrival-aws-time', style={'margin-left':'10px'},persistence=True)]),                
            ]),
         dbc.Row([
                dbc.Col([html.Label('Departure Time (from AWS to base, HHMM):' , style={'margin-left':'150px'} ),
                         dcc.Input(placeholder='enter time',type='text',id='depart-aws-time', style={'margin-left':'30px'},persistence=True)]),
                dbc.Col([html.Label('Arrival Time (to base, HHMM): ' ),
                         dcc.Input(placeholder='enter time',type='text',id='arrival-base-time', style={'margin-left':'10px'},persistence=True)]),                
            ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label(html.B(['Location: ']), style={'margin-right':'10px'}),
                dcc.RadioItems(['Automatic GPS Location', 'Manual Lat/Lon Input' ], 'Automatic GPS Location', id='location-selection')
        ])]),
        html.Div(id="geolocation-position-output"),
        html.Div(id="geolocation-position-inputs"),
        dcc.Store(id='lon-output',data='string'),
        dcc.Store(id='lat-output',data='string'),
        dbc.Row([
            dbc.Col([html.Label(html.B(['Work Crew: '])),
            html.Br(),
            dcc.Textarea(placeholder='Enter people',id='crew-input',style={'width': '95%', 'height': 100},persistence=True)]
                   )]),
        html.Br(),
        dbc.Row([
            dbc.Col([html.Label(html.B(['Transport Method (input names of pilot(s) if applicable): '])),
            html.Br(),
            dcc.Textarea(placeholder='Enter method/people',id='transport-input',style={'width': '95%', 'height': 100},persistence=True)]
                   )]),
        html.Br(),
        dbc.Row([dbc.Col([
            html.Label(html.B(['Work Purpose: '])),
            html.Br(),
            dcc.Textarea(placeholder='Enter text',id='work-purpose',style={'width': '95%', 'height': 100},persistence=True)])]),
        
        html.Br(),
        dbc.Row([
            dbc.Col([html.Label(html.B(['Weather Conditions: '])),
            html.Br(),
            dcc.Textarea(placeholder='Enter conditions',id='wx-notes',style={'width': '95%', 'height': 100},persistence=True)]
                   )]),
        html.Br(),
        dbc.Row([
            dbc.Col([html.Label(html.B('Field Notes: ')),
            html.Br(),
            dcc.Textarea(placeholder='Enter notes',id='field-notes',style={'width': '95%', 'height': 100},persistence=True)]
                   )]),
        html.Br(),
        dbc.Row([html.Label(html.B('Intrumentation Heights'))]),
        dbc.Row([html.Label('Input applicable instrument heights before and after servicing. If a station does not have one of the instruments, please input "N/A":')]),
        dbc.Row([
            dbc.Col([html.Label(['Select Units: '], style={'margin-left':'10px'}), dcc.RadioItems(['inches', 'meters','centimeters' ],'inches', id='unit-selection',inline=True, style={'margin-left':'30px'})])]),
        dbc.Row([dbc.Col(html.Label(html.B('Before')),width={'offset':4}),
            dbc.Col(html.Label(html.B('After')),width={'offset':2})]),
                         
        dbc.Row([dbc.Col(html.Label(('1m Temperature')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='t1-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='t1-height-after',style={'width': '90%', 'height': 50},persistence=True))]),    
        dbc.Row([dbc.Col(html.Label(('2m Temperature')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='t2-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='t2-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('4m Temperature')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='t4-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='t4-height-after',style={'width': '90%', 'height': 50},persistence=True))]),    
        dbc.Row([dbc.Col(html.Label(('7m Temperature')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='t7-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='t7-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('15m Temperature')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='t15-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='t15-height-after',style={'width': '90%', 'height': 50},persistence=True))]),    
        dbc.Row([dbc.Col(html.Label(('30m Temperature')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='t30-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='t30-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('1m Pressure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='pres1-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='pres1-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
        dbc.Row([dbc.Col(html.Label(('2m Pressure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='pres2-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='pres2-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
        dbc.Row([dbc.Col(html.Label(('4m Pressure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='pres4-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='pres4-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
        dbc.Row([dbc.Col(html.Label(('7m Pressure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='pres7-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='pres7-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
        dbc.Row([dbc.Col(html.Label(('15m Pressure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='pres15-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='pres15-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
        dbc.Row([dbc.Col(html.Label(('30m Pressure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='pres30-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='pres30-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
         dbc.Row([dbc.Col(html.Label(('1m RH')),width=2,style={'textAlign':'center'}),
            dbc.Col(dcc.Textarea(id='rh1-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='rh1-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
         dbc.Row([dbc.Col(html.Label(('2m RH')),width=2,style={'textAlign':'center'}),
            dbc.Col(dcc.Textarea(id='rh2-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='rh2-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
         dbc.Row([dbc.Col(html.Label(('4m RH')),width=2,style={'textAlign':'center'}),
            dbc.Col(dcc.Textarea(id='rh4-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='rh4-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
         dbc.Row([dbc.Col(html.Label(('7m RH')),width=2,style={'textAlign':'center'}),
            dbc.Col(dcc.Textarea(id='rh7-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='rh7-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
         dbc.Row([dbc.Col(html.Label(('15m RH')),width=2,style={'textAlign':'center'}),
            dbc.Col(dcc.Textarea(id='rh15-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='rh15-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
         dbc.Row([dbc.Col(html.Label(('30m RH')),width=2,style={'textAlign':'center'}),
            dbc.Col(dcc.Textarea(id='rh30-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='rh30-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row(
            [dbc.Col(html.Label(('ADG')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='adg-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='adg-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('1m Wind Speed')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wspd1-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wspd1-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('2m Wind Speed')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wspd2-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wspd2-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('4m Wind Speed')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wspd4-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wspd4-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('7m Wind Speed')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wspd7-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wspd7-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('15m Wind Speed')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wspd15-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wspd15-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('30m Wind Speed')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wspd30-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wspd30-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
         
        dbc.Row([dbc.Col(html.Label(('1m Wind Direction')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wdir1-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wdir1-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('2m Wind Direction')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wdir2-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wdir2-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('4m Wind Direction')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wdir4-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wdir4-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('7m Wind Direction')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wdir7-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wdir7-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('15m Wind Direction')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wdir15-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wdir15-height-after',style={'width': '90%', 'height': 50},persistence=True))]),

        dbc.Row([dbc.Col(html.Label(('30m Wind Direction')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='wdir30-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='wdir30-height-after',style={'width': '90%', 'height': 50},persistence=True))]),
        dbc.Row(
            [dbc.Col(html.Label(('30m Solar Radiation')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='sw-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='sw-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        dbc.Row([dbc.Col(html.Label(('Electronics Enclosure')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Textarea(id='datalogger-height-b4',style={'width': '90%', 'height': 50},persistence=True)),
            dbc.Col(dcc.Textarea(id='datalogger-height-after',style={'width': '90%', 'height': 50},persistence=True))]), 
        html.Br(),
        dbc.Row(html.Label(html.B('Input Images of Station Before and After Servicing. '))),
        dbc.Row(html.Label('Take photo facing the direction listed. Supported file types are JPEG, PNG, GIF, and WebP.')),
        dbc.Row([dbc.Col(html.Label(html.B('Before')),width={'offset':4}),
            dbc.Col(html.Label(html.B('After')),width={'offset':3})]),
                         
        dbc.Row([dbc.Col(
            html.Label(html.B('North')),width=2,style={'textAlign': 'center'}),
            dbc.Col(dcc.Upload(
                id='upload-image-north-before',
                children=html.Div([
                    'Drag and Drop or ',
                    html.U('Select Files')
                ]),
                style={
                    'width': '5',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '1px'
                },
             
                multiple=False ),width={'size':5}),
            dbc.Col(dcc.Upload(
                id='upload-image-north-after',
                children=html.Div([
                    'Drag and Drop or ',
                    html.U('Select Files')
                ]),
                style={
                    'width': '5',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '1px'
                },
              
                multiple=False),width={'size':5})]),
         
         dbc.Row([dbc.Col(
            html.Label(html.B('South')),width=2,style={'textAlign': 'center'}),
            dbc.Col(
                dcc.Upload(
                    id='upload-image-south-before',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.U('Select Files')
                    ]),
                    style={
                        'width': '5',
                        'height': '50px',
                        'lineHeight': '50px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '1px'
                    },
                    
                    multiple=False),width={'size':5,}),
            dbc.Col(dcc.Upload(
                id='upload-image-south-after',
                children=html.Div([
                    'Drag and Drop or ',
                    html.U('Select Files')
                ]),
                style={
                    'width': '5',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '1px'
                },
                
                multiple=False),width={'size':5})]),

         dbc.Row([dbc.Col(
            html.Label(html.B('East')),width=2,style={'textAlign': 'center'}),
            dbc.Col(
                dcc.Upload(
                    id='upload-image-east-before',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.U('Select Files')
                    ]),
                    style={
                        'width': '5',
                        'height': '50px',
                        'lineHeight': '50px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '1px'
                    },
                    # Allow multiple files to not be uploaded
                    multiple=False),width={'size':5}),
            dbc.Col(dcc.Upload(
                id='upload-image-east-after',
                children=html.Div([
                    'Drag and Drop or ',
                    html.U('Select Files')
                ]),
                style={
                    'width': '5',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '1px'
                },
                # Allow multiple files to be uploaded
                multiple=False),width={'size':5})]),
        
         dbc.Row([dbc.Col(
            html.Label(html.B('West')),width=2,style={'textAlign': 'center'}),
            dbc.Col(
                dcc.Upload(
                    id='upload-image-west-before',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.U('Select Files')
                    ]),
                    style={
                        'width': '5',
                        'height': '50px',
                        'lineHeight': '50px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '1px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False),width={'size':5}),
                  
            dbc.Col(dcc.Upload(
                id='upload-image-west-after',
                children=html.Div([
                    'Drag and Drop or ',
                    html.U('Select Files')]),
                style={
                    'width': '5',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '1px'
                }, multiple=False), width={'size':5})]), 

         dbc.Row([dbc.Col(), dbc.Col(html.Div(id='output-image-upload-east-before')), dbc.Col(html.Div(id='output-image-upload-east-after'))]),
         dbc.Row([dbc.Col(), dbc.Col(html.Div(id='output-image-upload-west-before')), dbc.Col(html.Div(id='output-image-upload-west-after'))]),
         dbc.Row([dbc.Col(), dbc.Col(html.Div(id='output-image-upload-north-before')), dbc.Col(html.Div(id='output-image-upload-north-after'))]),
         dbc.Row([dbc.Col(), dbc.Col(html.Div(id='output-image-upload-south-before')), dbc.Col(html.Div(id='output-image-upload-south-after'))]),
         
         html.Br(),
         dbc.Row([html.Label(html.B('Extra Images'))]),
         dbc.Row(dbc.Col(
                dcc.Upload(
                    id='upload-image-extra',
                    children=html.Div([ 'Drag and Drop or ',html.U('Select Files')]),
                    style={
                        'width': '10',
                        'height': '50px',
                        'lineHeight': '50px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '1px' },multiple=True), width={'size':10}), style={'margin-left':'100px'}),
         html.Div(id='output-image-extra'),
         #html.Div(id='output-image-extra2'),
         dcc.Store(id='field-notes-out',data=[]),
         dcc.Store(id="name-out",data=[]),
         dcc.Store(id='caption-store',data=[]),
         dcc.Store(id='filename-store',data=[]),
         dcc.Store(id="date-out",data=[]),
         dcc.Store(id="transport-out",data=[]),
         dcc.Store(id='work-purpose-out',data=[]),
         dcc.Store(id='wx-notes-out',data=[]),
         dcc.Store(id='crew-out',data=[]),
         dcc.Store(id='t1-b4-out',data=[]),
         dcc.Store(id='t1-after-out',data=[]),
         dcc.Store(id='t2-b4-out',data=[]),
         dcc.Store(id='t2-after-out',data=[]),
         dcc.Store(id='t4-b4-out',data=[]),
         dcc.Store(id='t4-after-out',data=[]),
         dcc.Store(id='t7-b4-out',data=[]),
         dcc.Store(id='t7-after-out',data=[]),
         dcc.Store(id='t15-b4-out',data=[]),
         dcc.Store(id='t15-after-out',data=[]),
         dcc.Store(id='t30-b4-out',data=[]),
         dcc.Store(id='t30-after-out',data=[]),
         dcc.Store(id='pres1-b4-out',data=[]),
         dcc.Store(id='pres1-after-out',data=[]),
         dcc.Store(id='pres2-b4-out',data=[]),
         dcc.Store(id='pres2-after-out',data=[]),
         dcc.Store(id='pres4-b4-out',data=[]),
         dcc.Store(id='pres4-after-out',data=[]),
         dcc.Store(id='pres7-b4-out',data=[]),
         dcc.Store(id='pres7-after-out',data=[]),
         dcc.Store(id='pres15-b4-out',data=[]),
         dcc.Store(id='pres15-after-out',data=[]),
         dcc.Store(id='pres30-b4-out',data=[]),
         dcc.Store(id='pres30-after-out',data=[]),
         
         dcc.Store(id='rh1-b4-out',data=[]),
         dcc.Store(id='rh1-after-out',data=[]),
         dcc.Store(id='rh2-b4-out',data=[]),
         dcc.Store(id='rh2-after-out',data=[]),
         dcc.Store(id='rh4-b4-out',data=[]),
         dcc.Store(id='rh4-after-out',data=[]),
         dcc.Store(id='rh7-b4-out',data=[]),
         dcc.Store(id='rh7-after-out',data=[]),
         dcc.Store(id='rh15-b4-out',data=[]),
         dcc.Store(id='rh15-after-out',data=[]),
         dcc.Store(id='rh30-b4-out',data=[]),
         dcc.Store(id='rh30-after-out',data=[]),
         dcc.Store(id='adg-b4-out',data=[]),
         dcc.Store(id='adg-after-out',data=[]),
         dcc.Store(id='wspd1-b4-out',data=[]),
         dcc.Store(id='wspd1-after-out',data=[]),
         dcc.Store(id='wspd2-b4-out',data=[]),
         dcc.Store(id='wspd2-after-out',data=[]),
         dcc.Store(id='wspd4-b4-out',data=[]),
         dcc.Store(id='wspd4-after-out',data=[]),
         dcc.Store(id='wspd7-b4-out',data=[]),
         dcc.Store(id='wspd7-after-out',data=[]),
         dcc.Store(id='wspd15-b4-out',data=[]),
         dcc.Store(id='wspd15-after-out',data=[]),
         dcc.Store(id='wspd30-b4-out',data=[]),
         dcc.Store(id='wspd30-after-out',data=[]),
         dcc.Store(id='wdir1-b4-out',data=[]),
         dcc.Store(id='wdir1-after-out',data=[]),
         dcc.Store(id='wdir2-b4-out',data=[]),
         dcc.Store(id='wdir2-after-out',data=[]),
         dcc.Store(id='wdir4-b4-out',data=[]),
         dcc.Store(id='wdir4-after-out',data=[]),
         dcc.Store(id='wdir7-b4-out',data=[]),
         dcc.Store(id='wdir7-after-out',data=[]),
         dcc.Store(id='wdir15-b4-out',data=[]),
         dcc.Store(id='wdir15-after-out',data=[]),
         dcc.Store(id='wdir30-b4-out',data=[]),
         dcc.Store(id='wdir30-after-out',data=[]),
         dcc.Store(id='sw-b4-out',data=[]),
         dcc.Store(id='sw-after-out',data=[]),
         dcc.Store(id='datalogger-b4-out',data=[]),
         dcc.Store(id='datalogger-after-out',data=[]),
         dcc.Store(id='depart-aws-time-out',data=[]),
         dcc.Store(id='depart-base-time-out',data=[]),
         dcc.Store(id='arrival-base-time-out',data=[]),
         dcc.Store(id='arrival-aws-time-out',data=[]),
         

         html.Br(),html.Br(),
         html.Button('Save as pdf',id='save-pdf-button'),
         html.Div(id='download-pdf'),
         #html.Button('Save Progress', id='save-progress-button'),
         #dcc.Download(id="download-dataframe-csv"),
         #dcc.Input(id='img-width',placeholder='Width',type='number' ),
         #dcc.Input(id='img-height', placeholder='Height', type='number'),
         #dcc.Download(id='download-pdf'),
         html.Br(), html.Br()    ],fluid=True)

#get lat lon data and save 
@callback(Output('transport-out','data'),
         Output('work-purpose-out','data'),
         Output('date-out','data'),
         Output('name-out','data'),
         Output('wx-notes-out','data'),
         Output('crew-out','data'),
         Output('field-notes-out','data'),
         Output('depart-base-time-out','data'),
         Output('depart-aws-time-out','data'),
         Output('arrival-base-time-out','data'),
         Output('arrival-aws-time-out','data'),
         Output('t1-b4-out','data'),
         Output('t1-after-out','data'),
         Output('t2-b4-out','data'),
         Output('t2-after-out','data'),
         Output('t4-b4-out','data'),
         Output('t4-after-out','data'),
         Output('t7-b4-out','data'),
         Output('t7-after-out','data'),
         Output('t15-b4-out','data'),
         Output('t15-after-out','data'),
         Output('t30-b4-out','data'),
         Output('t30-after-out','data'),
         Output('pres1-b4-out','data'),
         Output('pres1-after-out','data'),
         Output('pres2-b4-out','data'),
         Output('pres2-after-out','data'),
         Output('pres4-b4-out','data'),
         Output('pres4-after-out','data'),
         Output('pres7-b4-out','data'),
         Output('pres7-after-out','data'),
         Output('pres15-b4-out','data'),
         Output('pres15-after-out','data'),
         Output('pres30-b4-out','data'),
         Output('pres30-after-out','data'),
         Output('rh1-b4-out','data'),
         Output('rh1-after-out','data'),
         Output('rh2-b4-out','data'),
         Output('rh2-after-out','data'),
         Output('rh4-b4-out','data'),
         Output('rh4-after-out','data'),
         Output('rh7-b4-out','data'),
         Output('rh7-after-out','data'),
         Output('rh15-b4-out','data'),
         Output('rh15-after-out','data'),
         Output('rh30-b4-out','data'),
         Output('rh30-after-out','data'),
         Output('wspd1-b4-out','data'),
         Output('wspd1-after-out','data'),
         Output('wspd2-b4-out','data'),
         Output('wspd2-after-out','data'),
         Output('wspd4-b4-out','data'),
         Output('wspd4-after-out','data'),
         Output('wspd7-b4-out','data'),
         Output('wspd7-after-out','data'),
         Output('wspd15-b4-out','data'),
         Output('wspd15-after-out','data'),
         Output('wspd30-b4-out','data'),
         Output('wspd30-after-out','data'),
         Output('wdir1-b4-out','data'),
         Output('wdir1-after-out','data'),
         Output('wdir2-b4-out','data'),
         Output('wdir2-after-out','data'),
         Output('wdir4-b4-out','data'),
         Output('wdir4-after-out','data'),
         Output('wdir7-b4-out','data'),
         Output('wdir7-after-out','data'),
         Output('wdir15-b4-out','data'),
         Output('wdir15-after-out','data'),
         Output('wdir30-b4-out','data'),
         Output('wdir30-after-out','data'),
         Output('adg-b4-out','data'),
         Output('adg-after-out','data'),
         Output('sw-b4-out','data'),
         Output('sw-after-out','data'),
         Output('datalogger-b4-out','data'),
         Output('datalogger-after-out','data'),
         Input('transport-input','value'),
         Input('work-purpose','value'),
         Input('date','value'),
         Input('stn-name','value'),
         Input('wx-notes','value'),
         Input('crew-input','value'),
         Input('field-notes','value'),
         Input('depart-base-time','value'),
         Input('depart-aws-time','value'),
         Input('arrival-base-time','value'),
         Input('arrival-aws-time','value'),
         Input('t1-height-b4','value'),
         Input('t1-height-after','value'),
         Input('t2-height-b4','value'),
         Input('t2-height-after','value'),
         Input('t4-height-b4','value'),
         Input('t4-height-after','value'),
         Input('t7-height-b4','value'),
         Input('t7-height-after','value'),
         Input('t15-height-b4','value'),
         Input('t15-height-after','value'),
         Input('t30-height-b4','value'),
         Input('t30-height-after','value'),
         Input('pres1-height-b4','value'),
         Input('pres1-height-after','value'),
         Input('pres2-height-b4','value'),
         Input('pres2-height-after','value'),
         Input('pres4-height-b4','value'),
         Input('pres4-height-after','value'),
         Input('pres7-height-b4','value'),
         Input('pres7-height-after','value'),
         Input('pres15-height-b4','value'),
         Input('pres15-height-after','value'),
         Input('pres30-height-b4','value'),
         Input('pres30-height-after','value'),
         Input('rh1-height-b4','value'),
         Input('rh1-height-after','value'),
         Input('rh2-height-b4','value'),
         Input('rh2-height-after','value'),
         Input('rh4-height-b4','value'),
         Input('rh4-height-after','value'),
         Input('rh7-height-b4','value'),
         Input('rh7-height-after','value'),
         Input('rh15-height-b4','value'),
         Input('rh15-height-after','value'),
         Input('rh30-height-b4','value'),
         Input('rh30-height-after','value'),
         Input('wspd1-height-b4','value'),
         Input('wspd1-height-after','value'),
         Input('wspd2-height-b4','value'),
         Input('wspd2-height-after','value'),
         Input('wspd4-height-b4','value'),
         Input('wspd4-height-after','value'),
         Input('wspd7-height-b4','value'),
         Input('wspd7-height-after','value'),
         Input('wspd15-height-b4','value'),
         Input('wspd15-height-after','value'),
         Input('wspd30-height-b4','value'),
         Input('wspd30-height-after','value'),
         Input('wdir1-height-b4','value'),
         Input('wdir1-height-after','value'),
         Input('wdir2-height-b4','value'),
         Input('wdir2-height-after','value'),
         Input('wdir4-height-b4','value'),
         Input('wdir4-height-after','value'),
         Input('wdir7-height-b4','value'),
         Input('wdir7-height-after','value'),
         Input('wdir15-height-b4','value'),
         Input('wdir15-height-after','value'),
         Input('wdir30-height-b4','value'),
         Input('wdir30-height-after','value'),
         Input('adg-height-b4','value'),
         Input('adg-height-after','value'),
         Input('sw-height-b4','value'),
         Input('sw-height-after','value'),
         Input('datalogger-height-b4','value'),
         Input('datalogger-height-after','value'))

def output_text_values(transport,work_purpose,date,name,wx_notes,crew,notes,depart_base,depart_aws,arrive_base,arrive_aws,t1_b4, t1_after,t2_b4, t2_after,t4_b4, t4_after,t7_b4, t7_after,t15_b4, t15_after,t30_b4, t30_after,pres1_b4, pres1_after,pres2_b4, pres2_after,pres4_b4, pres4_after,pres7_b4, pres7_after,pres15_b4, pres15_after,pres30_b4, pres30_after,rh1_b4, rh1_after,rh2_b4, rh2_after,rh4_b4, rh4_after,rh7_b4, rh7_after,rh15_b4, rh15_after,rh30_b4, rh30_after,wspd1_b4, wspd1_after,wspd2_b4, wspd2_after,wspd4_b4, wspd4_after,wspd7_b4, wspd7_after,wspd15_b4, wspd15_after,wspd30_b4, wspd30_after,wdir1_b4, wdir1_after,wdir2_b4, wdir2_after,wdir4_b4, wdir4_after,wdir7_b4, wdir7_after,wdir15_b4, wdir15_after,wdir30_b4, wdir30_after,adg_b4, adg_after,sw_b4,sw_after,datalogger_b4, datalogger_after):
    return(transport,work_purpose,date,name,wx_notes,crew,notes,depart_base,depart_aws,arrive_base,arrive_aws,t1_b4, t1_after,t2_b4, t2_after,t4_b4, t4_after,t7_b4, t7_after,t15_b4, t15_after,t30_b4, t30_after,pres1_b4, pres1_after,pres2_b4, pres2_after,pres4_b4, pres4_after,pres7_b4, pres7_after,pres15_b4, pres15_after,pres30_b4, pres30_after,rh1_b4, rh1_after,rh2_b4, rh2_after,rh4_b4, rh4_after,rh7_b4, rh7_after,rh15_b4, rh15_after,rh30_b4, rh30_after,wspd1_b4, wspd1_after,wspd2_b4, wspd2_after,wspd4_b4, wspd4_after,wspd7_b4, wspd7_after,wspd15_b4, wspd15_after,wspd30_b4, wspd30_after,wdir1_b4, wdir1_after,wdir2_b4, wdir2_after,wdir4_b4, wdir4_after,wdir7_b4, wdir7_after,wdir15_b4, wdir15_after,wdir30_b4, wdir30_after,adg_b4, adg_after,sw_b4,sw_after,datalogger_b4, datalogger_after)

@callback(Output("geolocation-position-inputs", "children"),
    Input('location-selection','value'))
def display(loc_value):
    if loc_value == 'Automatic GPS Location':
        return(dbc.Row([
            dbc.Col([
                #html.Label(html.B(['Location: ']), style={'margin-right':'10px'}),
                html.Button("Update Position", id="update-btn"),
                dcc.Geolocation(id="geolocation")])]), ) #,high_accuracy=True,show_alert=True

    elif loc_value == 'Manual Lat/Lon Input':
        return(dbc.Row([
            dbc.Col([
                html.Label(['Manual location input if GPS is not working:']),
                dcc.Input(placeholder='Enter Lat', type='text',value='',id='lat-input',debounce=False,autoComplete='on',size='20', style={'margin-left':'10px'} ),
                dcc.Input(placeholder='Enter Lon', type='text',value='',id='lon-input',debounce=False,autoComplete='on',size='20', style={'margin-left':'10px'} ),
            ])]))
#"""
@callback(Output("geolocation", "update_now"), 
          Input("update-btn", "n_clicks"))
def update_now(click):
    return True if click and click > 0 else False

@callback(Output("geolocation-position-output", "children"),
    Input("geolocation", "local_date"),
    Input("geolocation", "position"))
def display_output(date, pos):
    if pos:
        lat = pos['lat']
        lon = pos['lon']
        return(str(round(lat,4))+' '+str(round(lon,4)), html.P(
            f"As of {date} your location was: lat {pos['lat']},lon {pos['lon']}, accuracy {pos['accuracy']} meters"))

@callback(Output('lat-output','data'),
         Output('lon-output','data'),
         Input('lat-input','value'),
         Input('lon-input','value'))

def output_latlon_values(lat,lon):
    return(lat,lon)

def parse_contents_extra( filename):
        return( filename+'\n')
def parse_contents(contents, filename, date,title):
    
    if title[0] == 'Extra Pictures':

        return(title[0]+': '+ filename[0]+'\n')
    else:
        return(title[0]+': '+ filename)


@callback(Output('output-image-upload-west-after', 'children'),
              Input('upload-image-west-after', 'contents'),
              State('upload-image-west-after', 'filename'),
              State('upload-image-west-after', 'last_modified'), prevent_initial_call=True)

def update_output_wa(list_of_contents_wa, list_of_names_wa, list_of_dates_wa):
    
    if list_of_contents_wa is not None:
        title = ['West After']
        children_west_after = [parse_contents(list_of_contents_wa, list_of_names_wa, list_of_dates_wa,title)]
        return( children_west_after)

@callback(Output('output-image-upload-west-before', 'children'),
              Input('upload-image-west-before', 'contents'),
              State('upload-image-west-before', 'filename'),
              State('upload-image-west-before', 'last_modified'), prevent_initial_call=True)

def update_output_wb(list_of_contents_wb, list_of_names_wb, list_of_dates_wb):
    if list_of_contents_wb is not None:
        title = ['West Before']
        children_west_before = [parse_contents(list_of_contents_wb, list_of_names_wb, list_of_dates_wb,title)]
        return( children_west_before)

@callback(Output('output-image-upload-east-after', 'children'),
              Input('upload-image-east-after', 'contents'),
              State('upload-image-east-after', 'filename'),
              State('upload-image-east-after', 'last_modified'), prevent_initial_call=True)

def update_output_ea(list_of_contents_ea, list_of_names_ea, list_of_dates_ea):
    if list_of_contents_ea is not None:
        title = ['East After']
        children_east_after =  [parse_contents(list_of_contents_ea, list_of_names_ea, list_of_dates_ea,title)]
        return( children_east_after)

@callback(Output('output-image-upload-east-before', 'children'),
              Input('upload-image-east-before', 'contents'),
              State('upload-image-east-before', 'filename'),
              State('upload-image-east-before', 'last_modified'), prevent_initial_call=True)

def update_output_eb(list_of_contents_eb, list_of_names_eb, list_of_dates_eb):
    if list_of_contents_eb is not None:
        title = ['East Before']
        children_east_before = [parse_contents(list_of_contents_eb, list_of_names_eb, list_of_dates_eb,title)]
        
        return( children_east_before)
        
@callback(Output('output-image-upload-north-after', 'children'),
              Input('upload-image-north-after', 'contents'),
              State('upload-image-north-after', 'filename'),
              State('upload-image-north-after', 'last_modified'), prevent_initial_call=True)

def update_output_na(list_of_contents_na, list_of_names_na, list_of_dates_na):
    if list_of_contents_na is not None:
        title = ['North After']
        children_north_after = [parse_contents(list_of_contents_na, list_of_names_na, list_of_dates_na,title)]
        return( children_north_after)

@callback(Output('output-image-upload-north-before', 'children'),
              Input('upload-image-north-before', 'contents'),
              State('upload-image-north-before', 'filename'),
              State('upload-image-north-before', 'last_modified'), prevent_initial_call=True)

def update_output_nb(list_of_contents_nb, list_of_names_nb, list_of_dates_nb):
    if list_of_contents_nb is not None:
        title = ['North Before']
        children_north_before = [parse_contents(list_of_contents_nb, list_of_names_nb, list_of_dates_nb,title)]
        return( children_north_before)

@callback(Output('output-image-upload-south-after', 'children'),
              Input('upload-image-south-after', 'contents'),
              State('upload-image-south-after', 'filename'),
              State('upload-image-south-after', 'last_modified'), prevent_initial_call=True)

def update_output_sa(list_of_contents_sa, list_of_names_sa, list_of_dates_sa):
    if list_of_contents_sa is not None:
        title = ['South After']
        children_south_after = [parse_contents(list_of_contents_sa, list_of_names_sa, list_of_dates_sa,title)]
        return( children_south_after)

@callback(Output('output-image-upload-south-before', 'children'),
              Input('upload-image-south-before', 'contents'),
              State('upload-image-south-before', 'filename'),
              State('upload-image-south-before', 'last_modified'), prevent_initial_call=True)

def update_output_sb(list_of_contents_sb, list_of_names_sb, list_of_dates_sb):
    if list_of_contents_sb is not None:
        title = ['South Before']
        children_south_before =[parse_contents(list_of_contents_sb, list_of_names_sb, list_of_dates_sb,title)]
        return( children_south_before)

        
@callback(
    Output('output-image-extra', 'children',allow_duplicate=True),
    #Input('upload-image-extra', 'contents'),
    Input('upload-image-extra', 'filename'),
    prevent_initial_call=True)

def update_output_extra(list_of_filenames):
    
    image_blocks = []
    if list_of_filenames is not None:
        for i, fig_name in enumerate( list_of_filenames):
            #names_extra_all.append(fig_name)
            parsed_contents = parse_contents_extra(fig_name)
            image_block = html.Div([parsed_contents,
                dcc.Input(id={'type': 'caption-input', 'index': i}, type='text',
                          placeholder='Enter caption for ' + fig_name, style={'width':'90%'}),
                          html.Button('X',id={'type': 'rm-picture', 'index': i}, style=default_button_style)])
            image_blocks.append(image_block)
        return(image_blocks)


@callback(Output('caption-store', 'data'),
    Output('filename-store', 'data'),
    Output({'type': 'rm-picture', 'index': ALL}, 'style', allow_duplicate=True),
    Input({'type': 'rm-picture', 'index': ALL}, 'n_clicks'),
    Input({'type': 'caption-input', 'index': ALL}, 'value'),
    State('upload-image-extra', 'filename'),
    prevent_initial_call=True)
def rm_pictures(nclicks, captions, filenames):   
    
    ctx = dash.callback_context
    style = []
    # Copy the inputs so we can safely modify
    updated_captions = list(captions)
    updated_filenames = list(filenames)
    clicked_index = ctx.triggered_id['index']
    for click in nclicks:
        if click is not None:
            index = ctx.triggered_id['index']
            #list_of_contents.pop(index)
            updated_captions.pop(index)
            #caption_list = captions
            updated_filenames.pop(index)
            #names_extra_all.pop(index)
            style.append(red_button_style )
        else:
            style.append(default_button_style)
    return(updated_captions, updated_filenames, style)

@callback([Output('download-pdf','children')],
    [Input('save-pdf-button','n_clicks'),
    Input('unit-selection','value')],
    [State('caption-store','data', allow_optional=True),
    State('filename-store','data', allow_optional=True),
    #State({'type': 'caption-input', 'index': ALL}, 'value'),
    State('upload-image-south-before', 'filename', allow_optional=True),
    State('upload-image-south-after', 'filename', allow_optional=True),
    State('upload-image-north-before', 'filename', allow_optional=True),
    State('upload-image-north-after', 'filename', allow_optional=True),          
    State('upload-image-east-before', 'filename', allow_optional=True),
    State('upload-image-east-after', 'filename', allow_optional=True),
    State('upload-image-west-before', 'filename', allow_optional=True),
    State('upload-image-west-after', 'filename', allow_optional=True),
    State('upload-image-extra', 'filename', allow_optional=True),
    State('work-purpose-out','data'),
    State('date-out','data'),
    State('name-out','data'),
    State('wx-notes-out','data'),
    State('crew-out','data'),
    State('transport-out','data'),
    State('lat-output','data'),
    State('lon-output','data'),
    State('field-notes-out','data'),
    State('arrival-aws-time-out','data'),
    State('arrival-base-time-out','data'),
    State('depart-base-time-out','data'), 
    State('depart-aws-time-out','data'),
    State('location-selection','value'),
    State("geolocation-position-output", "children"),
    State('t1-b4-out','data'),
    State('t1-after-out','data'),
    State('t2-b4-out','data'),
    State('t2-after-out','data'),
    State('t4-b4-out','data'),
    State('t4-after-out','data'),
    State('t7-b4-out','data'),
    State('t7-after-out','data'),
    State('t15-b4-out','data'),
    State('t15-after-out','data'),
    State('t30-b4-out','data'),
    State('t30-after-out','data'),
    State('pres1-b4-out','data'),
    State('pres1-after-out','data'),
    State('pres2-b4-out','data'),
    State('pres2-after-out','data'),
    State('pres4-b4-out','data'),
    State('pres4-after-out','data'),
    State('pres7-b4-out','data'),
    State('pres7-after-out','data'),
    State('pres15-b4-out','data'),
    State('pres15-after-out','data'),
    State('pres30-b4-out','data'),
    State('pres30-after-out','data'),
    State('rh1-b4-out','data'),
    State('rh1-after-out','data'),
    State('rh2-b4-out','data'),
    State('rh2-after-out','data'),
    State('rh4-b4-out','data'),
    State('rh4-after-out','data'),
    State('rh7-b4-out','data'),
    State('rh7-after-out','data'),
    State('rh15-b4-out','data'),
    State('rh15-after-out','data'),
    State('rh30-b4-out','data'),
    State('rh30-after-out','data'),
    State('wspd1-b4-out','data'),
    State('wspd1-after-out','data'),
    State('wspd2-b4-out','data'),
    State('wspd2-after-out','data'),
    State('wspd4-b4-out','data'),
    State('wspd4-after-out','data'),
    State('wspd7-b4-out','data'),
    State('wspd7-after-out','data'),
    State('wspd15-b4-out','data'),
    State('wspd15-after-out','data'),
    State('wspd30-b4-out','data'),
    State('wspd30-after-out','data'),
    State('wdir1-b4-out','data'),
    State('wdir1-after-out','data'),
    State('wdir2-b4-out','data'),
    State('wdir2-after-out','data'),
    State('wdir4-b4-out','data'),
    State('wdir4-after-out','data'),
    State('wdir7-b4-out','data'),
    State('wdir7-after-out','data'),
    State('wdir15-b4-out','data'),
    State('wdir15-after-out','data'),
    State('wdir30-b4-out','data'),
    State('wdir30-after-out','data'),
    State('adg-b4-out','data'),
    State('adg-after-out','data'),
    State('sw-b4-out','data'),
    State('sw-after-out','data'),
    State('datalogger-b4-out','data'),
    State('datalogger-after-out','data')],prevent_initial_call=True)

def update_output(nclicks,units,captions,filenames_store,sb_file,sa_file,nb_file,na_file,eb_file,ea_file,wb_file,wa_file,extra_file,purpose,date,name,wx_notes,crew,transportation,lat,lon,field_notes,arrival_time_aws,arrival_time_base,depart_time_base,depart_time_aws,loc_method_sel,auto_loc,t1_b4,t1_after,t2_b4,t2_after,t4_b4,t4_after,t7_b4,t7_after,t15_b4,t15_after,t30_b4,t30_after,pres1_b4,pres1_after,pres2_b4,pres2_after,pres4_b4,pres4_after,pres7_b4,pres7_after,pres15_b4,pres15_after,pres30_b4,pres30_after,rh1_b4,rh1_after,rh2_b4,rh2_after,rh4_b4,rh4_after,rh7_b4,rh7_after,rh15_b4,rh15_after,rh30_b4,rh30_after,wspd1_b4,wspd1_after,wspd2_b4,wspd2_after,wspd4_b4,wspd4_after,wspd7_b4,wspd7_after,wspd15_b4,wspd15_after,wspd30_b4,wspd30_after,wdir1_b4,wdir1_after,wdir2_b4,wdir2_after,wdir4_b4,wdir4_after,wdir7_b4,wdir7_after,wdir15_b4,wdir15_after,wdir30_b4,wdir30_after,adg_b4,adg_after,sw_b4,sw_after,datalogger_b4,datalogger_after):
   
    if units == 'inches':
        pass
    elif units == 'meters':
        
        if t1_b4 != 'N/A': t1_b4 =str(float(t1_b4) * 39.37)
        if t1_after != 'N/A': t1_after =str(float(t1_after) * 39.37) 
        if t2_b4 != 'N/A': t2_b4 =str(float(t2_b4) * 39.37)
        if t2_after != 'N/A': t2_after =str(float(t2_after) * 39.37) 
        if t4_b4 != 'N/A': t4_b4 =str(float(t4_b4) * 39.37)
        if t4_after != 'N/A': t4_after =str(float(t4_after) * 39.37) 
        if t7_b4 != 'N/A': t7_b4 =str(float(t7_b4) * 39.37)
        if t7_after != 'N/A': t7_after =str(float(t7_after) * 39.37) 
        if t15_b4 != 'N/A': t15_b4 =str(float(t15_b4) * 39.37)
        if t15_after != 'N/A': t15_after =str(float(t15_after) * 39.37) 
        if t30_b4 != 'N/A': t30_b4 =str(float(t30_b4) * 39.37)
        if t30_after != 'N/A': t30_after =str(float(t30_after) * 39.37) 
        
        if pres1_b4 != 'N/A': pres1_b4 =str(float(pres1_b4) * 39.37)
        if pres1_after != 'N/A': pres1_after =str(float(pres1_after) * 39.37)
        if pres2_b4 != 'N/A': pres2_b4 =str(float(pres2_b4) * 39.37)
        if pres2_after != 'N/A': pres2_after =str(float(pres2_after) * 39.37)
        if pres4_b4 != 'N/A': pres4_b4 =str(float(pres4_b4) * 39.37)
        if pres4_after != 'N/A': pres4_after =str(float(pres4_after) * 39.37)
        if pres7_b4 != 'N/A': pres7_b4 =str(float(pres7_b4) * 39.37)
        if pres7_after != 'N/A': pres7_after =str(float(pres7_after) * 39.37)
        if pres15_b4 != 'N/A': pres15_b4 =str(float(pres15_b4) * 39.37)
        if pres15_after != 'N/A': pres15_after =str(float(pres15_after) * 39.37)
        if pres30_b4 != 'N/A': pres30_b4 =str(float(pres30_b4) * 39.37)
        if pres30_after != 'N/A': pres30_after =str(float(pres30_after) * 39.37)
            
        if rh1_b4 != 'N/A': rh1_b4 =str(float(rh1_b4) * 39.37)
        if rh1_after != 'N/A': rh1_after =str(float(rh1_after) * 39.37)
        if rh2_b4 != 'N/A': rh2_b4 =str(float(rh2_b4) * 39.37)
        if rh2_after != 'N/A': rh2_after =str(float(rh2_after) * 39.37)
        if rh4_b4 != 'N/A': rh4_b4 =str(float(rh4_b4) * 39.37)
        if rh4_after != 'N/A': rh4_after =str(float(rh4_after) * 39.37)
        if rh7_b4 != 'N/A': rh7_b4 =str(float(rh7_b4) * 39.37)
        if rh7_after != 'N/A': rh7_after =str(float(rh7_after) * 39.37)
        if rh15_b4 != 'N/A': rh15_b4 =str(float(rh15_b4) * 39.37)
        if rh15_after != 'N/A': rh15_after =str(float(rh15_after) * 39.37)
        if rh30_b4 != 'N/A': rh30_b4 =str(float(rh30_b4) * 39.37)
        if rh30_after != 'N/A': rh30_after =str(float(rh30_after) * 39.37)
            
        if wspd1_b4 != 'N/A': wspd1_b4 =str(float(wspd1_b4) * 39.37)
        if wspd1_after != 'N/A': wspd1_after =str(float(wspd1_after) * 39.37)
        if wspd2_b4 != 'N/A': wspd2_b4 =str(float(wspd2_b4) * 39.37)
        if wspd2_after != 'N/A': wspd2_after =str(float(wspd2_after) * 39.37)
        if wspd4_b4 != 'N/A': wspd4_b4 =str(float(wspd4_b4) * 39.37)
        if wspd4_after != 'N/A': wspd4_after =str(float(wspd4_after) * 39.37)
        if wspd7_b4 != 'N/A': wspd7_b4 =str(float(wspd7_b4) * 39.37)
        if wspd7_after != 'N/A': wspd7_after =str(float(wspd7_after) * 39.37)
        if wspd15_b4 != 'N/A': wspd15_b4 =str(float(wspd15_b4) * 39.37)
        if wspd15_after != 'N/A': wspd15_after =str(float(wspd15_after) * 39.37)
        if wspd30_b4 != 'N/A': wspd30_b4 =str(float(wspd30_b4) * 39.37)
        if wspd30_after != 'N/A': wspd30_after =str(float(wspd30_after) * 39.37)
        if wdir1_b4 != 'N/A': wdir1_b4 =str(float(wdir1_b4) * 39.37)
        if wdir1_after != 'N/A': wdir1_after =str(float(wdir1_after) * 39.37)
        if wdir2_b4 != 'N/A': wdir2_b4 =str(float(wdir2_b4) * 39.37)
        if wdir2_after != 'N/A': wdir2_after =str(float(wdir2_after) * 39.37)
        if wdir4_b4 != 'N/A': wdir4_b4 =str(float(wdir4_b4) * 39.37)
        if wdir4_after != 'N/A': wdir4_after =str(float(wdir4_after) * 39.37)
        if wdir7_b4 != 'N/A': wdir7_b4 =str(float(wdir7_b4) * 39.37)
        if wdir7_after != 'N/A': wdir7_after =str(float(wdir7_after) * 39.37)
        if wdir15_b4 != 'N/A': wdir15_b4 =str(float(wdir15_b4) * 39.37)
        if wdir15_after != 'N/A': wdir15_after =str(float(wdir15_after) * 39.37)
        if wdir30_b4 != 'N/A': wdir30_b4 =str(float(wdir30_b4) * 39.37)
        if wdir30_after != 'N/A': wdir30_after =str(float(wdir30_after) * 39.37)
        if adg_b4 != 'N/A':adg_b4 =str(float(adg_b4) * 39.37)
        if adg_after != 'N/A': adg_after =str(float(adg_after) * 39.37)
        if sw_b4 != 'N/A':sw_b4 =str(float(sw_b4) * 39.37)
        if sw_after != 'N/A': sw_after =str(float(sw_after) * 39.37)
        if datalogger_b4 != 'N/A': datalogger_b4 =str(float(datalogger_b4) * 39.37)
        if datalogger_after != 'N/A': datalogger_after =str(float(datalogger_after) * 39.37)


    elif units == 'centimeters':
        
        if t1_b4 != 'N/A': t1_b4 =str(float(t1_b4) * 0.393701)
        if t1_after != 'N/A': t1_after =str(float(t1_after) * 0.393701) 
        if t2_b4 != 'N/A': t2_b4 =str(float(t2_b4) * 0.393701)
        if t2_after != 'N/A': t2_after =str(float(t2_after) * 0.393701) 
        if t4_b4 != 'N/A': t4_b4 =str(float(t4_b4) * 0.393701)
        if t4_after != 'N/A': t4_after =str(float(t4_after) * 0.393701) 
        if t7_b4 != 'N/A': t7_b4 =str(float(t7_b4) * 0.393701)
        if t7_after != 'N/A': t7_after =str(float(t7_after) * 0.393701) 
        if t15_b4 != 'N/A': t15_b4 =str(float(t15_b4) * 0.393701)
        if t15_after != 'N/A': t15_after =str(float(t15_after) * 0.393701) 
        if t30_b4 != 'N/A': t30_b4 =str(float(t30_b4) * 0.393701)
        if t30_after != 'N/A': t30_after =str(float(t30_after) * 0.393701) 
        
        if pres1_b4 != 'N/A': pres1_b4 =str(float(pres1_b4) * 0.393701)
        if pres1_after != 'N/A': pres1_after =str(float(pres1_after) * 0.393701)
        if pres2_b4 != 'N/A': pres2_b4 =str(float(pres2_b4) * 0.393701)
        if pres2_after != 'N/A': pres2_after =str(float(pres2_after) * 0.393701)
        if pres4_b4 != 'N/A': pres4_b4 =str(float(pres4_b4) * 0.393701)
        if pres4_after != 'N/A': pres4_after =str(float(pres4_after) * 0.393701)
        if pres7_b4 != 'N/A': pres7_b4 =str(float(pres7_b4) * 0.393701)
        if pres7_after != 'N/A': pres7_after =str(float(pres7_after) * 0.393701)
        if pres15_b4 != 'N/A': pres15_b4 =str(float(pres15_b4) * 0.393701)
        if pres15_after != 'N/A': pres15_after =str(float(pres15_after) * 0.393701)
        if pres30_b4 != 'N/A': pres30_b4 =str(float(pres30_b4) * 0.393701)
        if pres30_after != 'N/A': pres30_after =str(float(pres30_after) * 0.393701)
            
        if rh1_b4 != 'N/A': rh1_b4 =str(float(rh1_b4) * 0.393701)
        if rh1_after != 'N/A': rh1_after =str(float(rh1_after) * 0.393701)
        if rh2_b4 != 'N/A': rh2_b4 =str(float(rh2_b4) * 0.393701)
        if rh2_after != 'N/A': rh2_after =str(float(rh2_after) * 0.393701)
        if rh4_b4 != 'N/A': rh4_b4 =str(float(rh4_b4) * 0.393701)
        if rh4_after != 'N/A': rh4_after =str(float(rh4_after) * 0.393701)
        if rh7_b4 != 'N/A': rh7_b4 =str(float(rh7_b4) * 0.393701)
        if rh7_after != 'N/A': rh7_after =str(float(rh7_after) * 0.393701)
        if rh15_b4 != 'N/A': rh15_b4 =str(float(rh15_b4) * 0.393701)
        if rh15_after != 'N/A': rh15_after =str(float(rh15_after) * 0.393701)
        if rh30_b4 != 'N/A': rh30_b4 =str(float(rh30_b4) * 0.393701)
        if rh30_after != 'N/A': rh30_after =str(float(rh30_after) * 0.393701)
            
        if wspd1_b4 != 'N/A': wspd1_b4 =str(float(wspd1_b4) * 0.393701)
        if wspd1_after != 'N/A': wspd1_after =str(float(wspd1_after) * 0.393701)
        if wspd2_b4 != 'N/A': wspd2_b4 =str(float(wspd2_b4) * 0.393701)
        if wspd2_after != 'N/A': wspd2_after =str(float(wspd2_after) * 0.393701)
        if wspd4_b4 != 'N/A': wspd4_b4 =str(float(wspd4_b4) * 0.393701)
        if wspd4_after != 'N/A': wspd4_after =str(float(wspd4_after) * 0.393701)
        if wspd7_b4 != 'N/A': wspd7_b4 =str(float(wspd7_b4) * 0.393701)
        if wspd7_after != 'N/A': wspd7_after =str(float(wspd7_after) * 0.393701)
        if wspd15_b4 != 'N/A': wspd15_b4 =str(float(wspd15_b4) * 0.393701)
        if wspd15_after != 'N/A': wspd15_after =str(float(wspd15_after) * 0.393701)
        if wspd30_b4 != 'N/A': wspd30_b4 =str(float(wspd30_b4) * 0.393701)
        if wspd30_after != 'N/A': wspd30_after =str(float(wspd30_after) * 0.393701)
        if wdir1_b4 != 'N/A': wdir1_b4 =str(float(wdir1_b4) * 0.393701)
        if wdir1_after != 'N/A': wdir1_after =str(float(wdir1_after) * 0.393701)
        if wdir2_b4 != 'N/A': wdir2_b4 =str(float(wdir2_b4) * 0.393701)
        if wdir2_after != 'N/A': wdir2_after =str(float(wdir2_after) * 0.393701)
        if wdir4_b4 != 'N/A': wdir4_b4 =str(float(wdir4_b4) * 0.393701)
        if wdir4_after != 'N/A': wdir4_after =str(float(wdir4_after) * 0.393701)
        if wdir7_b4 != 'N/A': wdir7_b4 =str(float(wdir7_b4) * 0.393701)
        if wdir7_after != 'N/A': wdir7_after =str(float(wdir7_after) * 0.393701)
        if wdir15_b4 != 'N/A': wdir15_b4 =str(float(wdir15_b4) * 0.393701)
        if wdir15_after != 'N/A': wdir15_after =str(float(wdir15_after) * 0.393701)
        if wdir30_b4 != 'N/A': wdir30_b4 =str(float(wdir30_b4) * 0.393701)
        if wdir30_after != 'N/A': wdir30_after =str(float(wdir30_after) * 0.393701)
        if adg_b4 != 'N/A':adg_b4 =str(float(adg_b4) * 0.393701)
        if adg_after != 'N/A': adg_after =str(float(adg_after) * 0.393701)
        if sw_b4 != 'N/A':sw_b4 =str(float(sw_b4) * 0.393701)
        if sw_after != 'N/A': sw_after =str(float(sw_after) * 0.393701)
        if datalogger_b4 != 'N/A': datalogger_b4 =str(float(datalogger_b4) * 0.393701)
        if datalogger_after != 'N/A': datalogger_after =str(float(datalogger_after) * 0.393701)

    if nclicks is not None:

        table_data = ((' ', 'Before', 'After'),
                     ('1m Temperature', t1_b4, t1_after ),
                     ('2m Temperature', t2_b4, t2_after ),
                     ('4m Temperature', t4_b4, t4_after ),
                     ('7m Temperature', t7_b4, t7_after ),
                     ('15m Temperature', t15_b4, t15_after ),
                     ('30m Temperature', t30_b4, t30_after ),
                     ('1m Pressure', pres1_b4, pres1_after ),
                     ('2m Pressure', pres2_b4, pres2_after ),
                     ('4m Pressure', pres4_b4, pres4_after ),
                     ('7m Pressure', pres7_b4, pres7_after ),
                     ('15m Pressure', pres15_b4, pres15_after ),
                     ('30m Pressure', pres30_b4, pres30_after ),
                     ('1m Relative Humidity', rh1_b4, rh1_after ),
                     ('2m Relative Humidity', rh2_b4, rh2_after ),
                     ('4m Relative Humidity', rh4_b4, rh4_after ),
                     ('7m Relative Humidity', rh7_b4, rh7_after ),
                     ('15m Relative Humidity', rh15_b4, rh15_after ),
                     ('30m Relative Humidity', rh30_b4, rh30_after ),
                     ('1m Wind Speed', wspd1_b4, wspd1_after ),
                     ('2m Wind Speed', wspd2_b4, wspd2_after ),
                     ('4m Wind Speed', wspd4_b4, wspd4_after ),
                     ('7m Wind Speed', wspd7_b4, wspd7_after ),
                     ('15m Wind Speed', wspd15_b4, wspd15_after ),
                     ('30m Wind Speed', wspd30_b4, wspd30_after ),
                     ('1m Wind Direction', wdir1_b4, wdir1_after ),
                     ('2m Wind Direction', wdir2_b4, wdir2_after ),
                     ('4m Wind Direction', wdir4_b4, wdir4_after ),
                     ('7m Wind Direction', wdir7_b4, wdir7_after ),
                     ('15m Wind Direction', wdir15_b4, wdir15_after ),
                     ('30m Wind Direction', wdir30_b4, wdir30_after ),
                     ('ADG', adg_b4, adg_after ),
                     ('Solar Radiation', sw_b4, sw_after ),
                     ('Electronics Enclosure', datalogger_b4, datalogger_after ))
        
        if nb_file is not None:
            nb_figure = figure_path+nb_file
        else:
            nb_figure = None
        if sb_file is not None:
            sb_figure = figure_path+sb_file
        else:
            sb_figure = None
        if eb_file is not None:
            eb_figure = figure_path+eb_file
        else:
            eb_figure = None
        if wb_file is not None:
            wb_figure = figure_path+wb_file
        else:
            wb_figure = None
            
        if na_file is not None:
            na_figure = figure_path+na_file
        else:
            na_figure = None
        if sa_file is not None:
            sa_figure = figure_path+sa_file
        else:
            sa_figure = None
        if ea_file is not None:
            ea_figure = figure_path+ea_file
        else:
            ea_figure = None
        if wa_file is not None:
            wa_figure = figure_path+wa_file
        else:
            wa_figure = None
        fullname = name+ ' AWS' #need to add (stn id)
        fulldate = 'Date Visited: '+date
        dept_arrival_time_base_aws = 'Departure Time (from base to AWS): '+depart_time_base+ '         Arrival Time (at AWS): '+arrival_time_aws
        dept_arrival_time_aws_base = 'Departure Time (from AWS to base): '+depart_time_aws+ '         Arrival Time (at base): '+arrival_time_base
        fulltravel = 'Transportation Method and Pilot Name(s): ' + transportation
        #fullloc = 'Location: '+location
        fullpurpose = 'Purpose for Visit: '+purpose
        fullcrew = 'Work Crew: '+crew
        full_wx_conditions = 'Weather Conditions: '+wx_notes
        #full_inst_heights=  tab
        fullnotes = 'Field Work Notes: '+field_notes
        if loc_method_sel == 'Automatic GPS Location':
            
            fullloc = 'Location: '+ auto_loc[0]
        elif loc_method_sel == 'Manual Lat/Lon Input':
            fullloc = 'Location: '+ lat + ' '+lon 
        pdf = FPDF()
        # Add a page
        #pdf.set_display_mode(zoom='default',layout='TWO_COLUMN_LEFT')
        pdf.add_page()
        # set style and size of font 
        pdf.set_font("Times", size = 16, style='B')
    
        # create a cell
        pdf.cell(200, 5, text = fullname, align='C')
        pdf.set_font("Times", size=12)
        # add another cell
        pdf.ln()
        pdf.ln()
        pdf.cell(200,7,text = fulldate)
        pdf.ln()
        pdf.cell(200,5, text=dept_arrival_time_base_aws, align='C')
        pdf.ln()
        pdf.cell(200,5, text=dept_arrival_time_aws_base, align='C')
        pdf.ln()
        pdf.write(5,text = fullloc)
        pdf.ln()
        pdf.write(5,text = fullcrew)
        pdf.ln()
        pdf.write(5,text = fullpurpose)
        pdf.ln()
        pdf.ln()
        pdf.write(5,text = fulltravel)
        pdf.ln()
        pdf.ln()
        pdf.write(5,text = full_wx_conditions)
        pdf.ln()
        pdf.ln()
        pdf.write(5,text = fullnotes)
        pdf.ln()
        pdf.cell(200,5,text='Instrumentation Heights (inches):')
        pdf.ln()
        with pdf.table() as table:
            for data_row in table_data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        width_extra = pdf.epw - 24
        pdf.add_page()
        width_img_b4after = (pdf.epw/2) - 12
        width_img_single = (pdf.epw)-24
        if nb_figure is not None and na_figure is not None:
            pdf.cell(100,5, text='Pointing towards North - Before', align='C')
            pdf.cell(80,5, text='Pointing towards North - After', align='C')
            pdf.image(nb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(na_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if sb_figure is not None and sa_figure is not None:
            pdf.cell(100,5, text='Pointing towards South - Before', align='C')
            pdf.cell(80,5, text='Pointing towards South - After', align='C')
            pdf.image(sb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(sa_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if eb_figure is not None and ea_figure is not None:
            pdf.cell(100,5, text='Pointing towards East - Before', align='C')
            pdf.cell(80,5, text='Pointing towards East - After', align='C')
            pdf.image(eb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(ea_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if wb_figure is not None and wa_figure is not None:
            pdf.cell(100,5, text='Pointing towards West - Before', align='C')
            pdf.cell(80,5, text='Pointing towards West - After', align='C')
            pdf.image(wb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(wa_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()

        if nb_figure is None and na_figure is not None:
            #pdf.cell(100,5, text='North Before', align='C')
            pdf.cell(200,5, text='Pointing towards North - After', align='C')
            #pdf.image(nb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(na_figure, w=width_img_single, x=20,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if sb_figure is None and sa_figure is not None:
            #pdf.cell(100,5, text='South Before', align='C')
            pdf.cell(200,5, text='Pointing towards South - After', align='C')
            #pdf.image(sb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(sa_figure, w=width_img_single, x=20,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if eb_figure is None and ea_figure is not None:
            #pdf.cell(100,5, text='East Before', align='C')
            pdf.cell(200,5, text='Pointing towards East - After', align='C')
            #pdf.image(eb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(ea_figure, w=width_img_single,x=20,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if wb_figure is None and wa_figure is not None:
            #pdf.cell(100,5, text='West Before', align='C')
            pdf.cell(200,5, text='Pointing towards West - After', align='C')
            #pdf.image(wb_figure, w=width_img_b4after,x=20,y=20, keep_aspect_ratio=True)
            pdf.image(wa_figure, w=width_img_single,x=20,y=20,  keep_aspect_ratio=True)
            pdf.add_page()

        if nb_figure is not None and na_figure is None:
            pdf.cell(200,5, text='Pointing towards North - Before', align='C')
            #pdf.cell(80,5, text='North After', align='C')
            pdf.image(nb_figure, w=width_img_single,x=20,y=20, keep_aspect_ratio=True)
            #pdf.image(na_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if sb_figure is not None and sa_figure is None:
            pdf.cell(200,5, text='Pointing towards South - Before', align='C')
            #pdf.cell(80,5, text='South After', align='C')
            pdf.image(sb_figure, w=width_img_single,x=20,y=20, keep_aspect_ratio=True)
            #pdf.image(sa_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if eb_figure is not None and ea_figure is None:
            pdf.cell(200,5, text='Pointing towards East - Before', align='C')
            #pdf.cell(80,5, text='East After', align='C')
            pdf.image(eb_figure, w=width_img_single,x=20,y=20, keep_aspect_ratio=True)
            #pdf.image(ea_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
        if wb_figure is not None and wa_figure is None:
            pdf.cell(200,5, text='Pointing towards West - Before', align='C')
            #pdf.cell(80,5, text='West After', align='C')
            pdf.image(wb_figure, w=width_img_single,x=20,y=20, keep_aspect_ratio=True)
            #pdf.image(wa_figure, w=width_img_b4after, x=pdf.w/2,y=20, keep_aspect_ratio=True)
            pdf.add_page()
            
        if len(captions) > 1:
            #print(captions, names_extra_all)
            pdf.cell(200,5, text='Extra Pictures', align='C')
            lengths = list(range(len(captions)))
            for file, caption, i in zip(filenames_store, captions, lengths):                
                if caption is not None and file is not None:
                    
                    figure = figure_path+file
                    pdf.write(5,text = caption)
                    pdf.image(figure,x=20,y=30,w=width_extra, keep_aspect_ratio=True)
                    pdf.ln()
                    #pdf.write(10,text = caption)
                    if float(i) != float(lengths[-1]):
                        pdf.add_page()
                    elif float(i) == float(lengths[-1]):
                        pass
                else:
                    pass
        if len(captions) == 1:
            extra_figure = figure_path+filenames_store[0]
            pdf.cell(200,5, text='Extra Pictures', align='C')
            pdf.image(extra_figure,x=20,y=30,w=width_extra, keep_aspect_ratio=True)
            pdf.write(5, text=captions[0])
    save_date = date.replace(r'/', '')
    pdf.output(pdf_output_path+name+"_"+str(save_date)+".pdf")   
    return(['PDF Saved! '])

if __name__ == "__main__":
    app.run(port=8898)
