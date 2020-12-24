'''
导入文件
'''

from flask import Blueprint
from flask_restful import Api, fields

from flask_pika import Pika as FPika

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_blueprint)

fpika = FPika()

from . import plateYieldStaisticsApi
from . import diagnosisDataApi
from . import VisualizationTsneApi
from . import VisualizationPCAApi
from . import VisualizationMDSApi
from . import getFlag
from . import Visualization
from . import VisualizationCorrelation
from . import VisualizationPlatetypes
from . import Platetypes