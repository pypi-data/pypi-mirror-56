Async interface to Red Hat Product Pages, using Twisted
=======================================================

.. image:: https://travis-ci.org/ktdreyer/txproductpages.svg?branch=master
             :target: https://travis-ci.org/ktdreyer/txproductpages

.. image:: https://badge.fury.io/py/txproductpages.svg
             :target: https://badge.fury.io/py/txproductpages

Access Red Hat Product Pages's REST API asyncronously (non-blocking) using the
Twisted framework.


Simple example: Fetching a release
----------------------------------

.. code-block:: python

    from txproductpages import Connection
    from twisted.internet import defer, reactor


    @defer.inlineCallbacks
    def example():
        pp = Connection()
        # fetch a release
        try:
            release = yield pp.release('ceph-3-0')
            # release is a Munch (dict-like) object.
            print(release.name)
        except Exception as e:
            print(e)


    if __name__ == '__main__':
        example().addCallback(lambda ign: reactor.stop())
        reactor.run()


More Examples
-------------

See ``examples/`` directory

Packages that use this package
------------------------------

* `helga-productpages <https://pypi.org/project/helga-productpages/>`_
