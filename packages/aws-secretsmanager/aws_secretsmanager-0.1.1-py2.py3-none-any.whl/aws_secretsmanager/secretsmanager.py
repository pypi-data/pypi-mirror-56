import os
import boto3
import json
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))


class SecretsManager:
  def __init__( self, 
                name=None,
                secrets_key='SECRET',
                rotation_source='secretsmanager',
                rotation_detail_type='Secret Rotation',
                rotation_detail_key='secretId'):
    self._values = {}
    self._handler = None
    name = name or os.environ.get(secrets_key)
    if name is None:
      return
    if type(name) is not str:
      raise TypeError("Secret must be of type string but is of type %s" % type(name))
    self._name = name
    self._client = boto3.client('secretsmanager')
    self._rotation_source = rotation_source
    self._rotation_detail_type = rotation_detail_type
    self._rotation_detail_key = rotation_detail_key
    self.get_secret(name)
  def __call__(self, *args):
    if callable(args[0]):
      self._handler = args[0]
      return self
    else:
      event = args[0]
      if (event.get('source') == self._rotation_source and 
          event.get('detail-type') == self._rotation_detail_type and
          event.get('detail',{}).get(self._rotation_detail_key) == self._name):
        self.get_secret()
      else:
        return self._handler(*args)
  def __getitem__(self, secret):
    return self._values.get(secret)
  def get_secret(self, name=None):
    name = name or self._name
    try:
      secret = self._client.get_secret_value(SecretId=name)
      for k,v in json.loads(secret['SecretString']).items():
        self._values[k] = v
        os.environ[k] = v
    except:
      log.exception("An error occurred loading the secret")
