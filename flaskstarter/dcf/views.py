# -*- coding: utf-8 -*-
import os
import pandas as pd
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..extensions import db
import json

dcf_views = Blueprint('dcf', __name__, url_prefix='/dcf')


#make an @serve_df decorator that deals with query params and converting the df

@dcf_views.route('/df/<id>', methods=['GET'])
def read_df(id):
    df = pd.read_csv('./flaskstarter/dcf/sample-data/2014-01-citibike-tripdata.csv')
    slice_start = request.args.get('slice_start', 0)
    slice_end = request.args.get('slice_end', False)
    if slice_end is not False:
        df = df[slice_start:int(slice_end)]
    return json.loads(df.to_json(orient='table', indent=2))

