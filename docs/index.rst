.. requests-forecast documentation master file, created by
   sphinx-quickstart on Tue Apr 16 10:00:35 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

requests-forecast documentation
===============================


Configuration
=============

**Required arguments**

.. raw:: html

    <table>
        <thead>
            <tr>
                <th>Option</th>
                <th>Use</th>
                <th>Default</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><em>onSelect</em></td>
                <td>
                    A function that takes the Google geocoder's result object and decides what to do with it, like it load it on a map, or redirect to another page, or whatever you need.
                </td>
                <td>An ugly alert with the result's address.</td>
            </tr>
        </tbody>
    </table>

**Optional arguments**

.. raw:: html

    <table>
        <thead>
            <tr>
                <th>Option</th>
                <th>Use</th>
                <th>Default</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><em>acceptableAddressTypes</em></td>
                <td>
                    A whitelist of address types allowed to appear in the results.
                    Drawn from <a href="http://code.google.com/apis/maps/documentation/javascript/services.html#GeocodingAddressTypes">the set defined by Google's geocoder</a>.
                </td>
                <td>All types accepted</td>
            </tr>
        </tbody>
    </table>


Contents:

.. toctree::
   :maxdepth: 2

   ../README.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

