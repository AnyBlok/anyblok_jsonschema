# This file is a part of the AnyBlok / JsonSchema project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from marshmallow_jsonschema import JSONSchema
from anyblok_marshmallow import ModelSchema, Nested, Text, PhoneNumber, Country
from marshmallow.compat import basestring
from marshmallow.class_registry import get_class
from marshmallow.decorators import post_dump
from marshmallow import missing


class AnyBlokJSONSchema(JSONSchema):

    def _get_default_mapping(self, obj):
        mapping = super(AnyBlokJSONSchema, self)._get_default_mapping(obj)
        mapping.update({
            Nested: '_from_nested_schema',
            Text: '_from_text_schema',
            PhoneNumber: '_from_tel_schema',
            Country: '_from_country_schema',
        })
        return mapping

    def _from_nested_schema(self, obj, field):
        """Support nested field."""
        if isinstance(field.nested, basestring):
            nested = get_class(field.nested)
        elif isinstance(field.schema, ModelSchema):
            nested = Nested(field.schema.schema.__class__).nested
            nested.__name__ = field.nested.__name__
        else:
            nested = field.nested

        name = nested.__name__
        outer_name = obj.__class__.__name__
        only = field.only
        exclude = field.exclude

        # If this is not a schema we've seen, and it's not this schema,
        # put it in our list of schema defs
        if name not in self._nested_schema_classes and name != outer_name:
            wrapped_nested = AnyBlokJSONSchema(nested=True)
            wrapped_dumped = wrapped_nested.dump(
                nested(only=only, exclude=exclude, context=obj.context)
            )
            self._nested_schema_classes[name] = wrapped_dumped
            self._nested_schema_classes.update(
                wrapped_nested._nested_schema_classes
            )

        # and the schema is just a reference to the def
        schema = {
            'type': 'object',
            '$ref': '#/definitions/{}'.format(name)
        }

        # NOTE: doubled up to maintain backwards compatibility
        metadata = field.metadata.get('metadata', {})
        metadata.update(field.metadata)

        for md_key, md_val in metadata.items():
            if md_key == 'metadata':
                continue
            schema[md_key] = md_val

        if field.many:
            schema = {
                'type': ["array"] if field.required else ['array', 'null'],
                'items': schema,
            }

        return schema

    def _apply_common_attribute(self, schema, field):
        if field.dump_only:
            schema['readonly'] = True

        if field.default is not missing:
            schema['default'] = field.default

        metadata = field.metadata.get('metadata', {})
        metadata.update(field.metadata)

        for md_key, md_val in metadata.items():
            if md_key == 'metadata':
                continue
            schema[md_key] = md_val

    def _from_text_schema(self, obj, field):
        json_schema = {
            'title': field.attribute or field.name,
            'type': 'string',
            'attrs': {
                'type': 'textarea',
            },
        }
        self._apply_common_attribute(json_schema, field)
        return json_schema

    def _from_tel_schema(self, obj, field):
        schema = {
            'title': field.attribute or field.name,
            'type': 'string',
            'attrs': {
                'type': 'tel',
            },
        }
        self._apply_common_attribute(schema, field)
        return schema

    def _from_country_schema(self, obj, field):
        return self._from_python_type(obj, field, str)

    @post_dump(pass_many=False)
    def wrap(self, data):
        if not self.nested:
            data.update({
                'definitions': self._nested_schema_classes,
                '$id': self.obj.__class__.__name__,
            })

        return data

    def dump(self, schema, *args, **kwargs):
        try:
            if isinstance(schema, ModelSchema):
                schema = schema.schema
        except AttributeError:
            pass

        return super(AnyBlokJSONSchema, self).dump(schema, *args, **kwargs)
