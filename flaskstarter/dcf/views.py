# -*- coding: utf-8 -*-
import os
import pandas as pd
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from ..extensions import db
import json

dcf_views = Blueprint('dcf', __name__, url_prefix='/dcf')


@dcf_views.route('/df/<id>', methods=['GET'])
def read_df(id):
    
    print(os.getcwd())
    "/Users/paddy/code/dcf-server"
    df = pd.read_csv('./flaskstarter/dcf/sample-data/2014-01-citibike-tripdata.csv')
    return json.loads(df.to_json(orient='table', indent=2))
    #return os.getcwd()

