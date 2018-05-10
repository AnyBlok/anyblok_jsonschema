# This file is a part of the AnyBlok / JsonSchema project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.

from anyblok.tests.testcase import DBTestCase
from anyblok_marshmallow.tests import (
    add_simple_model, ExempleSchema, add_complexe_model, CustomerSchema)
from anyblok_jsonschema import AnyBlokJSONSchema
from anyblok import Declarations
from anyblok.column import Integer, Text


class TestJsonSchema(DBTestCase):

    def test_simple_schema_1(self):
        registry = self.init_registry(add_simple_model)
        schema = ExempleSchema(registry=registry)
        jsonschema = AnyBlokJSONSchema()
        self.assertEqual(
            jsonschema.dump(schema),
            {
                '$id': 'Model.Schema.Model.Exemple',
                'definitions': {},
                'properties': {
                    'id': {
                        'format': 'integer',
                        'title': 'id',
                        'type': 'number'
                    },
                    'name': {
                        'maxLength': 64,
                        'title': 'name',
                        'type': 'string'
                    },
                    'number': {
                        'format': 'integer',
                        'title': 'number',
                        'type': 'number'
                    },
                },
                'required': ['name'],
                'type': 'object'
            }
        )

    def test_simple_schema_2(self):
        registry = self.init_registry(add_simple_model)
        schema = ExempleSchema(registry=registry)
        jsonschema = AnyBlokJSONSchema()
        self.assertEqual(
            jsonschema.dump(schema.schema),
            {
                '$id': 'Model.Schema.Model.Exemple',
                'definitions': {},
                'properties': {
                    'id': {
                        'format': 'integer',
                        'title': 'id',
                        'type': 'number'
                    },
                    'name': {
                        'maxLength': 64,
                        'title': 'name',
                        'type': 'string'
                    },
                    'number': {
                        'format': 'integer',
                        'title': 'number',
                        'type': 'number'
                    },
                },
                'required': ['name'],
                'type': 'object'
            }
        )

    def test_complexe_schema(self):
        registry = self.init_registry(add_complexe_model)
        schema = CustomerSchema(registry=registry)
        jsonschema = AnyBlokJSONSchema()
        self.assertEqual(
            jsonschema.dump(schema.schema),
            {
                '$id': 'Model.Schema.Model.Customer',
                'definitions': {
                    'AddressSchema': {
                        'properties': {
                            'city': {
                                '$ref': '#/definitions/CitySchema',
                                'type': 'object',
                            },
                            'id': {
                                'format': 'integer',
                                'title': 'id',
                                'type': 'number',
                            },
                            'street': {
                                'maxLength': 64,
                                'title': 'street',
                                'type': 'string',
                            },
                        },
                        'required': ['street'],
                        'type': 'object',
                    },
                    'CitySchema': {
                        'properties': {
                            'id': {
                                'format': 'integer',
                                'title': 'id',
                                'type': 'number',
                            },
                            'name': {
                                'maxLength': 64,
                                'title': 'name',
                                'type': 'string',
                            },
                            'zipcode': {
                                'maxLength': 64,
                                'title': 'zipcode',
                                'type': 'string',
                            },
                        },
                        'required': ['name', 'zipcode'],
                        'type': 'object',
                    },
                    'TagSchema': {
                        'properties': {
                            'id': {
                                'format': 'integer',
                                'title': 'id',
                                'type': 'number',
                            },
                            'name': {
                                'maxLength': 64,
                                'title': 'name',
                                'type': 'string',
                            },
                        },
                        'required': ['name'],
                        'type': 'object',
                    }
                },
                'properties': {
                    'addresses': {
                        'items': {
                            '$ref': '#/definitions/AddressSchema',
                            'many': True,
                            'type': 'object'
                        },
                        'type': ['array', 'null'],
                    },
                    'id': {
                        'format': 'integer',
                        'title': 'id',
                        'type': 'number',
                    },
                    'name': {
                        'maxLength': 64,
                        'title': 'name',
                        'type': 'string',
                    },
                    'tags': {
                        'items': {
                            '$ref': '#/definitions/TagSchema',
                            'many': True,
                            'type': 'object'
                        },
                        'type': ['array', 'null'],
                    },
                },
                'required': ['name'],
                'type': 'object'
            }
        )

    def test_schema_with_text(self):

        def add_in_registry():

            @Declarations.register(Declarations.Model)
            class Exemple:
                id = Integer(primary_key=True)
                text = Text()

        registry = self.init_registry(add_in_registry)
        schema = ExempleSchema(registry=registry)
        jsonschema = AnyBlokJSONSchema()
        print(jsonschema.dump(schema))
        self.assertEqual(
            jsonschema.dump(schema),
            {
                '$id': 'Model.Schema.Model.Exemple',
                'definitions': {},
                'properties': {
                    'id': {
                        'format': 'integer',
                        'title': 'id',
                        'type': 'number'
                    },
                    'text': {
                        'attrs': {
                            'type': 'textarea',
                        },
                        'title': 'text',
                        'type': 'string',
                    },
                },
                'required': [],
                'type': 'object'
            }
        )
