# REST client for the Zoom API

[![Build Status](https://api.travis-ci.org/uw-it-aca/uw-restclients-zoom.svg?branch=master)](https://travis-ci.org/uw-it-aca/uw-restclients-zoom)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/uw-restclients-zoom/badge.svg?branch=master)](https://coveralls.io/r/uw-it-aca/uw-restclients-zoom?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-zoom.svg)](https://pypi.python.org/pypi/uw-restclients-zoom)
![Python versions](https://img.shields.io/pypi/pyversions/uw-restclients-zoom.svg)

Installation:

    pip install UW-RestClients-Zoom

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_ZOOM_DAO_CLASS=Live

    # Zoom REST API hostname (eval or production)
    RESTCLIENTS_ZOOM_HOST=https://...

    # Zoom Key/Secret
    RESTCLIENTS_ZOOM_API_KEY=
    RESTCLIENTS_ZOOM_API_SECRET=

Optional settings:

    # Customizable parameters for urllib3
    RESTCLIENTS_ZOOM_TIMEOUT=5
    RESTCLIENTS_ZOOM_POOL_SIZE=10

See examples for usage.  Pull requests welcome.
