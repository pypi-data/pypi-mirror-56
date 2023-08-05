from typing import Optional

from dateutil import parser

from apex_client.request import ApexRequest


class ApexObject:
    valid_properties = []
    date_properties = []
    mapped_properties = {}

    def __init__(self, json_data: dict):
        self.dynamic_properties = []

        for key in self.valid_properties:
            setattr(self, key, json_data.get(key))

        for key in self.mapped_properties.keys():
            setattr(self, self.mapped_properties[key], json_data.get(key))

        if 'dynamic_fields' in json_data:
            for dynamic_field in json_data.get('dynamic_fields'):
                dynamic_dict = {
                    'network_project_id': dynamic_field.get('network_project_id'),
                    'network_project_name': dynamic_field.get('network_project_name'),
                    'fields': {}
                }

                for field in dynamic_field['fields']:
                    dynamic_dict['fields'].update({
                        field['property']: {
                            'network_id': field['network_id'],
                            'type': field['type'],
                            'value': field['value']
                        }
                    })

                self.dynamic_properties.append(dynamic_dict)

        for key in self.date_properties:
            if json_data.get(key):
                setattr(self, key, parser.parse(json_data.get(key)))
            else:
                setattr(self, key, None)

    @classmethod
    def _get(cls, path: str) -> Optional['ApexObject']:
        response = ApexRequest.get(path)

        if response['status_code'] == 200:
            return cls(response['response'])

        return None

    def _get_dynamic_property_from_dict(self, index, key, default_value=None):
        try:
            dynamic_property = self.dynamic_properties[index]['fields'].get(key)

            if dynamic_property:
                value = dynamic_property.get('value')

                if value is not None:
                    return value

        except IndexError:
            pass

        if default_value is not None:
            return default_value

        return None

    def get_dynamic_property(self, key, default_value=None):
        for item in self.dynamic_properties[::-1]:
            if key in item['fields'].keys():
                return self._get_dynamic_property_from_dict(self.dynamic_properties.index(item), key, default_value)

        return self._get_dynamic_property_from_dict(0, key, default_value)

    def has_dynamic_property(self, key) -> bool:
        for item in self.dynamic_properties:
            if key in item['fields'].keys():
                return True

        return False

    def get_dynamic_property_display(self, key):
        dynamic_property = None

        for item in self.dynamic_properties:
            if key in item['fields'].keys():
                dynamic_property = item['fields'][key]
                break

        if dynamic_property:
            value = self.get_dynamic_property(key)

            if value and dynamic_property.get('options') and dynamic_property.get('options').get('choices'):
                for choice in dynamic_property['options']['choices']:
                    if str(choice[0]) == str(value):
                        return choice[1]

        return None

    def get_dynamic_fields(self):
        dynamic_fields = []

        for item in self.dynamic_properties:
            dynamic_property = {
                'network_project_id': item['network_project_id'],
                'network_project_name': item['network_project_name'],
                'fields': [
                    {
                        'network_id': field['network_id'],
                        'property': key,
                        'value': field['value']
                    } for key, field in item['fields'].items()
                ]
            }

            dynamic_fields.append(dynamic_property)

        return dynamic_fields

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self)}>"

    def __str__(self):
        return "Empty class"

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)

        except AttributeError as e:
            if name in self.date_properties or name in self.valid_properties:
                return None
            else:
                raise e
