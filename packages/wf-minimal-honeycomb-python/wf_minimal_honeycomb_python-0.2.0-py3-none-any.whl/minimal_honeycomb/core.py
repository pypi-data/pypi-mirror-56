from gqlpycgen.client import Client, FileUpload
from gqlpycgen.api import QueryBase, MutationBase
from uuid import uuid4
import json
import os

INDENT_STRING = '  '

class MinimalHoneycombClient:
    def __init__(
        self,
        uri=None,
        token_uri=None,
        audience=None,
        client_id=None,
        client_secret=None
    ):
        if uri is None:
            uri = os.getenv('HONEYCOMB_URI')
            if uri is None:
                raise ValueError('Honeycomb URI not specified and environment variable HONEYCOMB_URI not set')
        if token_uri is None:
            token_uri = os.getenv('HONEYCOMB_TOKEN_URI')
            if token_uri is None:
                raise ValueError('Honeycomb token URI not specified and environment variable HONEYCOMB_TOKEN_URI not set')
        if audience is None:
            audience = os.getenv('HONEYCOMB_AUDIENCE')
            if audience is None:
                raise ValueError('Honeycomb audience not specified and environment variable HONEYCOMB_AUDIENCE not set')
        if client_id is None:
            client_id = os.getenv('HONEYCOMB_CLIENT_ID')
            if client_id is None:
                raise ValueError('Honeycomb client ID not specified and environment variable HONEYCOMB_CLIENT_ID not set')
        if client_secret is None:
            client_secret = os.getenv('HONEYCOMB_CLIENT_SECRET')
            if client_secret is None:
                raise ValueError('Honeycomb client secret not specified and environment variable HONEYCOMB_CLIENT_SECRET not set')
        self.client = Client(
            uri=uri,
            client_credentials={
                'token_uri': token_uri,
                'audience': audience,
                'client_id': client_id,
                'client_secret': client_secret,
            }
        )
        self.mutation = MutationBase(self.client)
        self.query = QueryBase(self.client)

    def request(
        self,
        request_type,
        request_name,
        arguments,
        return_object
    ):
        request_string = self.request_string(
            request_type,
            request_name,
            arguments,
            return_object
        )
        if arguments is not None:
            variables = {argument_name: argument_info['value'] for argument_name, argument_info in arguments.items()}
        else:
            variables = None
        if request_name == 'createDatapoint':
            # Prepare upload package
            filename = uuid4().hex
            try:
                data = variables.get('datapoint').get('file').get('data')
            except:
                raise ValueError('createDatapoint arguments do not contain datapoint.file.data field')
            try:
                content_type = variables.get('datapoint').get('file').get('contentType')
            except:
                raise ValueError('createDatapoint arguments do not contain datapoint.file.contentType field')
            files = FileUpload()
            data_json = json.dumps(data)
            files.add_file("variables.datapoint.file.data", filename, data_json, content_type)
            # Replace data with filename
            variables['datapoint']['file']['data'] = filename
            response = self.client.execute(request_string, variables, files)
        else:
            response = self.query.query(request_string, variables)
        try:
            return_value = response.get(request_name)
        except:
            raise ValueError('Received unexpected response from Honeycomb: {}'.format(response))
        return return_value

    def request_string(
        self,
        request_type,
        request_name,
        arguments,
        return_object
    ):
        if arguments is not None:
            top_level_argument_list_string = ', '.join(['${}: {}'.format(argument_name, argument_info['type']) for argument_name, argument_info in arguments.items()])
            top_level_string = '{} {}({})'.format(
                request_type,
                request_name,
                top_level_argument_list_string
            )
            second_level_argument_list_string = ', '.join(['{}: ${}'.format(argument_name, argument_name) for argument_name in arguments.keys()])
            second_level_string = '{}({})'.format(
                request_name,
                second_level_argument_list_string
            )
        else:
            top_level_string = '{} {}'.format(
                request_type,
                request_name
            )
            second_level_string = request_name
        object = [
            {top_level_string: [
                {second_level_string: return_object}
            ]}
        ]
        request_string = self.request_string_formatter(object)
        return request_string

    def request_string_formatter(self, object, indent_level=0):
        request_string = ''
        for object_component in object:
            if hasattr(object_component, 'keys'):
                if len(object_component) == 0:
                    raise ValueError('Object for formatting has zero length')
                if len(object_component) > 1:
                    raise ValueError('Multiple objects with children must be represented by separate dicts')
                # parent = object_component.keys()[0]
                # children = object_component.values()[0]
                for parent, children in object_component.items():
                    request_string += '{}{} {{\n{}{}}}\n'.format(
                        INDENT_STRING*indent_level,
                        parent,
                        self.request_string_formatter(children, indent_level=indent_level + 1),
                        INDENT_STRING*indent_level
                    )
            else:
                request_string += '{}{}\n'.format(
                    INDENT_STRING*indent_level,
                    object_component
                )
        return request_string
