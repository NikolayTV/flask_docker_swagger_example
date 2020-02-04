# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restplus import Api, Resource, fields
from catboost import CatBoostRegressor
import pandas as pd 
import json


flask_app = Flask(__name__)
api = Api(app = flask_app, 
          version = "1.0", 
          title = "Example flask servise", 
          description = "Get prediction from some body params",
          doc='/docs',
          default='Predict',
          default_label='Model Inference')

model_fields = api.model(
    'PredictIn', {
                'features': fields.Nested(
                    api.model('BodyParams', {
                        'height': fields.Float(required = True, description="Body height", help='This is to help you understand what to do'),
                        'weight': fields.Float(required = True, description="Body weight", help='This is to help you understand what to do'),
                        'age':   fields.Float(required = True, description="Body age", help='This is to help you understand what to do'),
                        'sugar':   fields.Float(required = True, description="Sugar in blodd", help='This is to help you understand what to do'),
                                 })),
                'modelVersion': fields.String(required=True, description='Model version', enum=['1.0'])})

response_fields =  api.model('PredictOut', {
                'Predicted output': fields.Float,
                })


model = CatBoostRegressor()      
model.load_model('models/catboost_regressor.cat')

@api.route('/api/predict/')
class MainClass(Resource):
    @api.doc()
    @api.expect(model_fields)
    #@api.response(code=400, model=error_fields, description='Some other Error')
    @api.response(code=200, model=response_fields,  description='Success')
    def post(self):
        #try:
            height = request.json['features']['height']
            weight = request.json['features']['weight']
            age = request.json['features']['age']
            sugar = request.json['features']['sugar']

            X = pd.DataFrame(data={'height':height, 'weight':weight, 'age':age, 'sugar':sugar}, index=[0])

            pred = model.predict(X)
            return {
                    "Predicted output": float(pred)
                   }, 200

if __name__ == '__main__':
    flask_app.run(debug=False, host='0.0.0.0', port=7777)






### Error customization
''' 
error_fields =  api.model('ProblemDetails', {
                'statusCode': fields.Integer,
                'title': fields.String,
                'message': fields.String,
                'fields': fields.String,
                })


class BaseError(Exception):
    """Base Error Class"""
    def __init__(self, statusCode=400, title=None, message=None, fields=None):
        Exception.__init__(self)
        self.statusCode = statusCode
        self.title = title
        self.message = message
        self.fields = fields

    def to_dict(self):
        return {'statusCode': self.statusCode,
                'title': self.title,
                'message': self.message,
                'fields': self.fields}


class FieldError(BaseError):
    def __init__(self, fields):
        BaseError.__init__(self)
        self.statusCode = 400
        self.message = 'One or more data fields are incorrect'
        self.title = 'FieldError'
        self.fields = fields


@api.errorhandler(FieldError)
def handle_error(error):
    return error.to_dict(), getattr(error, 'statusCode')

@api.errorhandler
def default_error_handler(error):
    """Returns Internal server error"""
    error = ServerError()
    return error.to_dict(), getattr(error, 'statusCode')

class ServerError(BaseError):
    def __init__(self, message='Internal server error'):
        BaseError.__init__(self)
        self.statusCode = 400
        self.message = 'The browser (or proxy) sent a request that this server could not understand.'
        self.title = 'Bad request'
        self.fields = None

'''