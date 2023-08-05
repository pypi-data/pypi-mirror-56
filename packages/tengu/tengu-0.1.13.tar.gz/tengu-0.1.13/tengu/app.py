import os
from .factory import FlaskFactory
#from .views import obx
from .models import db


def get_aws_keys():
    import hvac
    client = hvac.Client(
                url=os.environ.get('VAULT_ADDR', 'http://localhost:8200'),
                token=os.environ.get('VAULT_TOKEN', 'null'),
                )
    creds = client.read('aws/creds/{}'.format(os.environ.get('VAULT_ROLE', 'default')))
    creds.update({'aws_region': 'us-east-1'})
    return {k: v for k, v in creds['data'].items() if 'key' in k}


def get_app():
    factory = FlaskFactory()
    
#     blueprint_dicts = [
#             dict(
#                 bp=obx,
#             )
#         ]
    
    app = factory.initiallize_flask(db)  # , blueprint_dicts)
    app.config.update(get_aws_keys())
    return app
