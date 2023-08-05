===========
Chalice
===========


Chalice is a microframework for writing serverless apps in python. It allows
you to quickly create and deploy applications that use AWS Lambda.  It provides:

* A command line tool for creating, deploying, and managing your app
* A decorator based API for integrating with Amazon API Gateway, Amazon S3,
  Amazon SNS, Amazon SQS, and other AWS services.
* Automatic IAM policy generation


You can create Rest APIs:

.. code-block:: python

    from chalice import Chalice

    app = Chalice(app_name="helloworld")

    @app.route("/")
    def index():
        return {"hello": "world"}

Tasks that run on a periodic basis:

.. code-block:: python

    from chalice import Chalice, Rate

    app = Chalice(app_name="helloworld")

    # Automatically runs every 5 minutes
    @app.schedule(Rate(5, unit=Rate.MINUTES))
    def periodic_task(event):
        return {"hello": "world"}


You can connect a lambda function to an S3 event:

.. code-block:: python

    from chalice import Chalice

    app = Chalice(app_name="helloworld")

    # Whenever an object is uploaded to 'mybucket'
    # this lambda function will be invoked.

    @app.on_s3_event(bucket='mybucket')
    def handler(event):
        print("Object uploaded for bucket: %s, key: %s"
              % (event.bucket, event.key))

As well as an SQS queue:

.. code-block:: python

    from chalice import Chalice

    app = Chalice(app_name="helloworld")

    # Invoke this lambda function whenever a message
    # is sent to the ``my-queue-name`` SQS queue.

    @app.on_sqs_message(queue='my-queue-name')
    def handler(event):
        for record in event:
            print("Message body: %s" % record.body)


And several other AWS resources.

Once you've written your code, you just run ``chalice deploy``
and Chalice takes care of deploying your app.

::

    $ chalice deploy
    ...
    https://endpoint/dev

    $ curl https://endpoint/api
    {"hello": "world"}

Up and running in less than 30 seconds.
Give this project a try and share your feedback with us here on Github.

The documentation is available
`on readthedocs <http://chalice.readthedocs.io/en/latest/>`__.


Related Projects
----------------
* `AWS Chalice <https://github.com/aws/chalice>`__ - Repository from which this
  project was forked.
* `serverless <https://github.com/serverless/serverless>`__ - Build applications
  comprised of microservices that run in response to events, auto-scale for
  you, and only charge you when they run.
* `Zappa <https://github.com/Miserlou/Zappa>`__ - Deploy python WSGI applications
  on AWS Lambda and API Gateway.
* `claudia <https://github.com/claudiajs/claudia>`__ - Deploy node.js projects
  to AWS Lambda and API Gateway.
* `Domovoi <https://github.com/kislyuk/domovoi>`_ - An extension to Chalice that
  handles a variety of AWS Lambda event sources such as SNS push notifications,
  S3 events, and Step Functions state machines.
