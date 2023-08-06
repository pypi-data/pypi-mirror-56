aws-secretsmanager
==================

This package provides a `SecretsManager` class that injects secret values from the AWS Secrets Manager service as environment variables.

If using AWS Lambda, the class can be used as a decorator on your handler function to automatically detect AWS Secrets Manager rotation events and dynamically update secret values if a secret rotation takes place.

Usage
-----

The following examples assume an AWS Secrets Manager secret called ``MySecret`` exists with the following secret value:

.. code:: json

  {
    "FOO": "bar",
    "TEST": "me"
  }

Basic Usage
***********

.. code:: python

  from aws_secretsmanager import SecretsManager

  # You can supply the name of the secret to the constructor
  secret = SecretsManager('MySecret')

  # If you don't supply the name of the secret, you can lookup the name from the SECRET environment variable
  os.environ['SECRET'] = 'MySecret'
  secret = SecretsManager()

  # You can use a different environment variable by specifying the secrets_key constructor parameter
  os.environ['MY_SECRET_KEY'] = 'MySecret'
  secret = SecretsManager(secrets_key='MY_SECRET_KEY')

  # After creating the SecretsManager object, each key in the secret value is available as a dictionary value
  foo = secret['FOO']  # Sets foo to 'bar'
  test = secret['TEST']  # Sets test to 'me'

  # SecretsManager will also create environment variables for each key in the secret value
  foo = os.environ['FOO']  # Sets foo to 'bar'
  test = os.environ['TEST']  # Sets test to 'me'

Advanced Usage
**************

For Lambda functions you can decorate your handlers with the SecretsManager object.

This will detect SecretsManager rotation events passed in via a custom CloudWatch event and dynamically update the secret value.

By default the expected custom CloudWatch event format is demonstrated below:

.. code:: json

  {
    "source":"secretsmanager",
    "detail-type":"Secret Rotation",
    "detail": {
      "secretId":"MySecret"
    }
  }

The custom event should be sent by your secrets rotation function using the CloudWatch events `PutEvents API call <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events.html#CloudWatchEvents.Client.put_events>`_ after the ``finishSecret`` step as outlined at https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-lambda-function-overview.html:

.. code:: python

  import boto3
  import json

  events = boto3.client('events')
  detail = json.dumps({'secretId':'MySecret'})

  # Put custom CloudWatch event
  events.put_events(Entries=[{'Source':'secretsmanager','DetailType':'Secret Rotation','Detail':detail}]

You can then create a CloudWatch events rule that invokes your Lambda function with the following event pattern:

.. code:: json

  {
    "source": [
      "secretsmanager"
    ],
    "detail-type": [
      "Secret Rotation"
    ],
    "detail": {
      "secretId": [
        "MySecret"
      ]
    }
  }

The following is an example of creating a CloudWatch events rule using the AWS CLI:

.. code:: bash

  $ aws events put-rule --name test \
      --event-pattern '{"source":["secretsmanager"],"detail-type":["Secret Rotation"],"detail":{"secretId":["MySecret"]}}'
  {
    "RuleArn": "arn:aws:events:ap-southeast-2:012345678901:rule/test"
  }

After creating the rule you need to attach a target to the rule that invokes your Lambda function:

.. code:: bash

  $ aws events put-targets --rule test --targets "Id"="Test","Arn"="arn:aws:lambda:ap-southeast-2:function:my-function"

And grant permission for CloudWatch events to invoke your Lambda function:

.. code:: bash

  $ aws lambda add-permission --function-name my-function \
      --action 'lambda:InvokeFunction' --principal events.amazonaws.com --statement-id events-access \
      --source-arn arn:aws:events:ap-southeast-2:012345678901:rule/test

Finally you can decorate your Lambda function handler with the SecretsManager object, which will automatically process the custom CloudWatch events trigger by your rotation function:

.. code:: python

  from aws_secretsmanager import SecretsManager

  secret = SecretsManager('MySecret')

  @secret
  def handler(event, context)
    ...
    ...

  # Assuming 'MySecret' is updated and Lambda handler is configured as a target for the custom CloudWatch event
  # then the following example CloudWatch event will dynamically update the secret
  event = {'version': '0', 'id': 'f5d47c23-2f37-7632-254a-734323ff5208', 'detail-type': 'Secret Rotation', 'source': 'secretsmanager', 'account': '012345678901', 'time': '2018-02-25T22:58:07Z', 'region': 'ap-southeast-2', 'detail': {'secretId': 'MySecret'}}
  handler(event,{})  # Updates secret value

Note that your handler function code is NOT invoked when the custom CloudWatch event is detected.

You can also override the expected ``source``, ``detail`` key and ``detail-type`` values as demonstrated below:

.. code:: python

  from aws_secretsmanager import SecretsManager

  secret = SecretsManager(
                name='MySecret',
                rotation_source='secretsmanager',
                rotation_detail_type='Secret Rotation',
                rotation_detail_key='secretId')

  @secret
  def handler(event, context):
    ...
    ...

Installation
------------

    pip install aws-secretsmanager

Requirements
------------

- boto3_

.. _boto3: https://github.com/boto/boto3

Authors
-------

- `Justin Menga`_

.. _Justin Menga: https://github.com/mixja
