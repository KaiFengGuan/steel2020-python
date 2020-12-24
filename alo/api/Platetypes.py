'''
Visualization
'''
from flask_restful import Resource, reqparse
from flask import json
from . import api
import pandas as pd
import numpy as np
from ..utils import getSQLData
from ..utils import getFlagArr
import json
from scipy.interpolate import interp1d

parser = reqparse.RequestParser(trim=True, bundle_errors=True)



class Platetypes(Resource):
    '''
    Platetypes
    '''
    def get(self,upid):
        """
        get
        ---
        tags:
          - 钢板类型
        parameters:
          - in: path
            name: upid
            required: true
            description: 钢板upid
            type: string
        responses:
            200:
                description: 执行成功
        """
        jsondata=getSQLData('SELECT  productcategory FROM dcenter.l2_m_primary_data where upid='+repr(upid))
        return jsondata[0][0],200, {'Access-Control-Allow-Origin': '*'}
api.add_resource(Platetypes, '/v1.0/model/Platetypes/<upid>/')