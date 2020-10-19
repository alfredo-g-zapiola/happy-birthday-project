import json
import boto3
import os
import ast

destino = 'agimenezzapiola@gmail.com'

SES = boto3.client('ses')


def lambda_handler(event, context):
    response = SES.send_email(Source='agimenezzapiola@gmail.com',
    Destination={'ToAddresses': [destino]},
    Message={'Subject': {
        'Data': 'Feliz cumple boludo!',
        'Charset': 'utf-8'
        },
        'Body': {
            'Text': {            'Data': 'Hola siukooo, te mando feliz cumple desde amazon web services\
            lambdaaaa. Te quiero boludo, programé esto para las 3 GMT. Posta te\
            quiero siukazo, estoy escribiendo esto con alto entusiasmo para que se\
            mande. Contame después cuando te llegue :). Por si te da curiosidad\
            te imprimo el evento de AWS (json): \n %s ' % event }
        }
     }
    )
    return response