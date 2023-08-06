================================
django-ok-17track |PyPI version|
================================

|Build Status| |Upload Python Package| |Python Versions| |PyPI downloads| |license| |Project Status|

django-17track is an unofficial 17track.com API wrapper for Django.

Installation
============

Install with pip:

.. code:: shell

    $ pip install django-ok-17track

Update INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = [
        ...
        'track17',
        ...
    ]

Make migrations

.. code:: shell

    $ python manage.py migrate



Available settings
==================

``TRACK17_API_KEY`` - API key for service.

``TRACK17_API_KEY_FUNCTION`` - Custom function to return API key, if you want to store it outside the Django settings.

``TRACK17_COUNTRIES_URL`` - Url to grab countries. Uses `https://www.17track.net/en/apicountry`_.

``TRACK17_CARRIERS_URL`` - Url to grab carriers. Uses `https://www.17track.net/en/apicarrier`_.


Basic example to use:
=====================

How to get all countries and carriers:
--------------------------------------

    .. code:: shell

        python managet.py populate_carriers
    

How to register tracking number and get it's info:
--------------------------------------------------

    .. code:: python

        from rest_framework import serializers
        from track17.services import register_track, get_track_info, get_track_info_as_packages
        from apps.track17.exceptions import DateProcessingError


        
        # try to register tracking number at 17track API
        try:
        register_track('tracking_number')
        except DateProcessingError as exc:
        raise serializers.ValidationError(str(exc))    
        
        # try to fetch an actual info about a tracking number
        try:
            response: Dict = get_track_info('tracking_number')
        except DateProcessingError as exc:
            raise serializers.ValidationError(str(exc))

        accepted_packages = response.get('accepted', [])

        # return packages info as a list of `PackageEntity` (dataclass instance) objects
        # in a readable way with a represantion of carriers and countries as Django model instances
        packages = get_track_info_as_packages(accepted)


Or can use 17track adapter directly:
------------------------------------

    .. code:: python

        from track17.track17 import Track17Adapter

        
        track17 = Track17Adapter()
        response = track17.register('number1', 'number2')
        response = track17.get_track_info('number1', 'number2')	
    

.. |PyPI version| image:: https://badge.fury.io/py/django-ok-17track.svg
   :target: https://badge.fury.io/py/django-ok-17track
.. |Build Status| image:: https://travis-ci.org/LowerDeez/django-ok-17track.svg?branch=master
   :target: https://travis-ci.org/LowerDeez/django-ok-17track
   :alt: Build status
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/django-ok-17track.svg
   :target: https://pypi.org/project/django-ok-17track/
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/django-ok-17track.svg
   :alt: Software license
   :target: https://github.com/LowerDeez/django-ok-17track/blob/master/LICENSE
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/django-ok-17track.svg
   :alt: PyPI downloads
.. |Project Status| image:: https://img.shields.io/pypi/status/django-ok-17track.svg
   :target: https://pypi.org/project/django-ok-17track/  
.. |Upload Python Package| image:: https://github.com/LowerDeez/django-ok-17track/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/LowerDeez/django-ok-17track
   :alt: Project Status

.. _https://www.17track.net/en/apicountry: https://www.17track.net/en/apicountry
.. _https://www.17track.net/en/apicarrier: https://www.17track.net/en/apicarrier
