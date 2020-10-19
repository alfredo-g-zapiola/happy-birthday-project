import boto3
import os
from datetime import datetime

from boto3.dynamodb.conditions import Key

SENDER = os.environ['DefaultSender']
SES = boto3.client('ses')
DDB = boto3.resource('dynamodb')

MONTH = int(datetime.today().strftime('%m'))
DAY = int(datetime.today().strftime('%d'))


def check_database():
    table = DDB.Table('Compleanni')
    response = table.query(
        KeyConditionExpression=Key('BDAY_MONTH').eq(MONTH)
    )
    print('Printing response from dynamo:\n', response)
    people = [p for p in response['Items'] if p['BDAY_DAY']==DAY]
    return people


def send_email(data_dict):
    response = SES.send_email(Source=SENDER,
                              Destination={'ToAddresses': [data_dict['Email']],
                                           'CcAddresses': [SENDER]},
                              Message={'Subject': {
                                  'Data': data_dict.get('Subject', 'Feliz cumple!!'),
                                  'Charset': 'utf-8'
                              },
                                  'Body': {
                                      'Text': {
                                          'Data': data_dict.get('Body', 'Feliz cumple, abrazo grande!! Alfredo')
                                      }
                                  }
                              }
                              )
    return response


def lambda_handler(event, context):
    print('Printing event:\n', event)
    people = check_database()
    if people:
        print('Sending email(s)\n')
        return [send_email(p) for p in people]
    else:
        print('No birthdays today')
        return 'Nothing to do today'
