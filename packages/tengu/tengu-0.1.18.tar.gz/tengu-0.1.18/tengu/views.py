import json
import socket
from flask import Blueprint, request
import boto3
from .__init__ import app



#obx = Blueprint('obx', __name__)

def page_view_log_count():
    client = boto3.client(
            'cloudwatch',
            aws_access_key_id=app.config['access_key'],
            aws_secret_access_key=app.config['secret_key'],
            )

    response = client.put_metric_data(
        Namespace='Application',
        MetricData=[
            {
                'MetricName': 'ViewCount',
                'Value': 1.0,
                'Unit': 'Count',
            },
        ]
    )

    return response


@app.route('/')
def root_view():
    page_view_log_count()
    return 'Hello World ' + socket.gethostname()
