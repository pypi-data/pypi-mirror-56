.. :changelog:

Release History
===============

`3.2.0`_ (17 Nov 2019)
----------------------
- Change pin for tornado-aws to support tornado-aws 2

`3.1.0`_ (07 Jul 2019)
----------------------
- When marshalling empty strings on put, translate to value to NULL instead of raising an exception

`3.0.2`_ (24 May 2019)
----------------------
- Saftely retrieve Attributes key in unwrap_delete_put_update_item for local dev

`3.0.1`_ (02 May 2019)
----------------------
- Change the pinning of Tornado to support Tornado 6

`3.0.0`_ (11 Feb 2019)
----------------------
- Update to support Python 3.7
- Drop support for Python 2

`2.3.0`_ (24 Jan 2018)
----------------------
- Add handling for ``tornado_aws.exceptions.RequestException``
- Update to tornado-aws 1.0.0

`2.2.0`_ (06 Jun 2017)
----------------------
- Update to tornado-aws 0.8.0 and add Python 3.6 to supported versions

`2.1.3`_ (27 Jan 2017)
----------------------
- Add HTTP Internal Server Error (500) and Service Unavailable (503) to retriable exceptions

`2.1.2`_ (28 Oct 2016)
----------------------
- Change the pinning of tornado-aws to open it up a little wider

`2.1.1`_ (21 Oct 2016)
----------------------
- Add ``DYANMODB_NO_CREDS_RATE_LIMIT`` environment variable support to the mixin

`2.1.0`_ (20 Oct 2016)
----------------------
- Fix exception handling for requests to actually catch all the exceptions we care about

`2.0.0`_ (17 Oct 2016)
----------------------
- Breaking API change for Client.get_item to allow for return values for ConsumedCapacity
- Implement Client.delete_item, Client.update_item, Client.query, Client.scan
- Improved parameter validation

`1.1.0`_ (12 Oct 2016)
----------------------
- Remove the service tag in InfluxDB
- Remove the correlation-id field value
- Collect all of the paged query results

`1.0.2`_ (26 Sep 2016)
----------------------
- Fix a mixin InfluxDB integration issue

`1.0.1`_ (26 Sep 2016)
----------------------
- Make ``DynamoDBMixin`` available from ``sprockets_dynamodb``

`1.0.0`_ (26 Sep 2016)
----------------------
- Initial release

`Next Release`_
---------------

.. _Next Release: https://github.com/sprockets/sprockets_dynamodb/compare/3.0.2...master
.. _3.0.2: https://github.com/sprockets/sprockets-dynamodb/compare/3.0.1...3.0.2
.. _3.0.1: https://github.com/sprockets/sprockets-dynamodb/compare/3.0.0...3.0.1
.. _3.0.0: https://github.com/sprockets/sprockets-dynamodb/compare/2.2.0...3.0.0
.. _2.3.0: https://github.com/sprockets/sprockets-dynamodb/compare/2.2.0...2.3.0
.. _2.2.0: https://github.com/sprockets/sprockets-dynamodb/compare/2.1.3...2.2.0
.. _2.1.3: https://github.com/sprockets/sprockets-dynamodb/compare/2.1.2...2.1.3
.. _2.1.2: https://github.com/sprockets/sprockets-dynamodb/compare/2.1.1...2.1.2
.. _2.1.1: https://github.com/sprockets/sprockets-dynamodb/compare/2.1.0...2.1.1
.. _2.1.0: https://github.com/sprockets/sprockets-dynamodb/compare/2.0.0...2.1.0
.. _2.0.0: https://github.com/sprockets/sprockets-dynamodb/compare/1.1.0...2.0.0
.. _1.1.0: https://github.com/sprockets/sprockets-dynamodb/compare/1.0.2...1.1.0
.. _1.0.2: https://github.com/sprockets/sprockets-dynamodb/compare/1.0.1...1.0.2
.. _1.0.1: https://github.com/sprockets/sprockets-dynamodb/compare/1.0.0...1.0.1
.. _1.0.0: https://github.com/sprockets/sprockets-dynamodb/compare/0.0.0...1.0.0
