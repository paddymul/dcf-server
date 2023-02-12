# -*- coding: utf-8 -*-
import os
import pandas as pd
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from flask_cors import cross_origin
from ..extensions import db
import json
from .dcf_transform import dcf_transform, s
#from lispy import s
dcf_views = Blueprint('dcf', __name__, url_prefix='/dcf')


#make an @serve_df decorator that deals with query params and converting the df



@dcf_views.route('/df/<id>', methods=['GET'])
@cross_origin()
def read_df(id):
    df = pd.read_csv('./flaskstarter/dcf/sample-data/2014-01-citibike-tripdata.csv')
    slice_start = int(request.args.get('slice_start', 0))
    slice_end = request.args.get('slice_end', False)
    if slice_end is not False:
        df = df[slice_start:int(slice_end)]
    return json.loads(df.to_json(orient='table', indent=2))


@dcf_views.route('/transform_df/<id>', methods=['GET'])
@cross_origin()
def transform_df(id):
    df = pd.read_csv('./flaskstarter/dcf/sample-data/2014-01-citibike-tripdata.csv')
    instructions = json.loads(request.args.get('instructions', None))

    #slice before or after??? probably after, otherwise run a dcf command
    df = dcf_transform(instructions, df)

    slice_start = int(request.args.get('slice_start', 0))
    slice_end = request.args.get('slice_end', False)
    if slice_end is not False:
        df = df[slice_start:int(slice_end)]
    return json.loads(df.to_json(orient='table', indent=2))

