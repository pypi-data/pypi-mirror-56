#!/usr/env/python
# coding: utf-8

"""
OpenD6 Flask API
"""

from os import path
from json import load
from flask import Flask, redirect, url_for, jsonify

def get_data():
    """Retrieve OpenD6 Data from file
    >>> get_data()
    """
    with open(path.join(path.dirname(__file__), 'schema.json')) as opendsix_data:
        return load(opendsix_data)

def define_api():
    """Define API endpoints
    >>> define_api()
    """
    api = Flask(__name__)
    data = get_data()

    @api.route('/')
    def _get_index():
        """Return index
        >>> _get_index()
        """
        return redirect(url_for('_get_api'))

    @api.route('/api/')
    def _get_api():
        """Return base attributes
        >>> _get_api()
        """
        return redirect(url_for('_list_routes'))

    @api.route('/api/v1/')
    def _list_routes():
        """Return a list of all available api calls for v1
        >>> _list_routes()
        """
        return redirect(url_for('_get_api_info'))

    @api.route('/api/v1/info/')
    def _get_api_info():
        """Return api info
        >>> _get_api_info()
        """
        api_info = {"opendsix" : data}
        return jsonify(api_info)

    @api.route('/api/v1/attributes/')
    def _get_attributes():
        """Return attributes
        >>> _get_attributes()
        """
        return jsonify(data['attributes'])

    @api.route('/api/v1/base/attributes/')
    def _get_base_attributes():
        """Return base attributes
        >>> _get_base_attributes()
        """
        base = data['properties']['attributes']
        attributes = data['attributes']
        base_attr = int(base  / len(attributes))
        base_attributes = []
        for attr in attributes:
            base_attributes[attr] = base_attr
        return jsonify(base_attributes)

    @api.route('/api/v1/properties')
    def _get_properties():
        """Return basic properties
        >>> _get_properties()
        """
        return jsonify(data['properties'])

    @api.route('/api/v1/quirks')
    def _get_quirks():
        """Return all quirks from OpenD6.
        >>> quirks = _get_quirks()
        type(quirks) == string
        """
        return jsonify(data['quirks'])

    return api
