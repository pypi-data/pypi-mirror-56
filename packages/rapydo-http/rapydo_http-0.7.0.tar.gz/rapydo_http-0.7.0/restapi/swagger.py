# -*- coding: utf-8 -*-

"""
Integrating swagger in automatic ways.
Original source was:
https://raw.githubusercontent.com/gangverk/flask-swagger/master/flask_swagger.py

"""

import re
import os
import tempfile
import json
from bravado_core.spec import Spec
from bravado_core.validate import validate_object
from restapi.attributes import ExtraAttributes, ALL_ROLES
from restapi.confs import PRODUCTION, ABS_RESTAPI_PATH, MODELS_DIR
from restapi.confs import CUSTOM_PACKAGE, EXTENDED_PACKAGE, EXTENDED_PROJECT_DISABLED
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.globals import mem

from restapi.utilities.configuration import load_yaml_file, mix
from restapi.utilities.logs import get_logger

log = get_logger(__name__)
JSON_APPLICATION = 'application/json'


def input_validation(json_parameters, definitionName):

    definition = mem.customizer._definitions['definitions'][definitionName]
    spec = mem.customizer._validated_spec

    # Can raise jsonschema.exceptions.ValidationError
    validate_object(spec, definition, json_parameters)


class BeSwagger(object):
    """Swagger class in our own way:

    Fewer methods than the original swagger reading,
    also more control and closer to the original swagger.
    """

    def __init__(self, endpoints, customizer):

        # Input
        self._endpoints = endpoints
        self._customizer = customizer

        # Swagger paths to be publish
        self._paths = {}
        # Original paths as flask should map
        self._original_paths = {}
        # The complete set of query parameters for all classes
        self._qparams = {}
        # Save schemas for parameters before to remove the custom sections
        # It is used to provide schemas for unittests and automatic forms
        self._parameter_schemas = {}
        self._used_swagger_tags = {}

    def read_my_swagger(self, method, endpoint, file=None, mapping=None):

        if mapping is None:
            old_version = True
            mapping = load_yaml_file(file)
        else:
            old_version = False

        # content has to be a dictionary
        if not isinstance(mapping, dict):
            raise TypeError("Wrong method ")

        # read common
        commons = mapping.pop('common', {})
        if commons:
            log.warning("Commons specs are deprecated")

        # Check if there is at least one except for common
        if len(mapping) < 1:
            raise ValueError("No definition found inside: %s " % file)

        ################################
        # Using 'attrs': a way to save external attributes

        # Instance
        extra = ExtraAttributes()

        ################################
        # Specs should contain only labels written in spec before

        pattern = re.compile(r'\<([^\>]+)\>')

        for label, specs in mapping.items():

            if old_version:
                if label not in endpoint.uris:
                    raise KeyError(
                        "Invalid label '%s' found.\nAvailable labels: %s"
                        % (label, list(endpoint.uris.keys()))
                    )
                uri = endpoint.uris[label]
                log.warning("Deprecated mapping-label endpoint definition: %s", uri)
            else:
                uri = '/%s%s' % (endpoint.base_uri, label)
                # This will be used by server.py.add
                if uri not in endpoint.uris:
                    endpoint.uris[uri] = uri

            ################################
            # add common elements to all specs
            for key, value in commons.items():
                if key not in specs:
                    specs[key] = value

            ################################
            # Separate external definitions

            # Find any custom part which is not swagger definition
            custom = specs.pop('custom', {})

            # Publish the specs on the final Swagger JSON
            # Default is to do it if not otherwise specified
            extra.publish = custom.get('publish', True)
            if not extra.publish:
                log.warning("Publish setting is deprecated")

            # Authentication
            if custom.get('authentication', False):

                # Add Bearer Token security to this method
                # This was already defined in swagger root
                specs['security'] = [{"Bearer": []}]

                # Automatically add the response for Unauthorized in not already defined
                k_int = hcodes.HTTP_BAD_UNAUTHORIZED
                k_str = str(hcodes.HTTP_BAD_UNAUTHORIZED)
                if k_int not in specs['responses'] and k_str not in specs['responses']:
                    specs['responses'][k_str] = {
                        'description': "Missing or invalid credentials or token"
                    }

                # Recover required roles
                roles = custom.get('authorized', [])
                # roles = custom.get('authorized', ['normal_user'])

                # TODO: create a method inside 'auth' to check roles
                # for role in roles:
                #     pass

                # If everything is fine set the roles to be required by Flask
                extra.auth = roles
                extra.required_roles = custom.get('required_roles', ALL_ROLES).lower()
            else:
                extra.auth = None

            # Other things that could be saved into 'custom' subset?

            ###########################
            # Strip the uri of the parameter
            # and add it to 'parameters'
            newuri = uri[:]  # create a copy
            if 'parameters' not in specs:
                specs['parameters'] = []

            ###########################
            # Read Form Data Custom parameters
            cparam = specs.pop('custom_parameters', None)
            if cparam is not None:
                for fdp in cparam:

                    params = self._fdp.get(fdp)
                    if params is None:
                        log.exit("No custom form data '%s'", fdp)
                    else:
                        # Unable to extend with list by using extends() because
                        # it add references to the original object and do not
                        # create copies. Without copying, the same objects will
                        # be modified several times leading to errors
                        for p in params:
                            specs['parameters'].append(p.copy())

            ###########################
            # Read normal parameters
            for parameter in pattern.findall(uri):

                # create parameters
                x = parameter.split(':')
                xlen = len(x)
                paramtype = 'string'

                if xlen == 1:
                    paramname = x[0]
                elif xlen == 2:
                    paramtype = x[0]
                    paramname = x[1]

                # FIXME: complete for all types
                # http://swagger.io/specification/#data-types-12
                if paramtype == 'int':
                    paramtype = 'number'
                if paramtype == 'path':
                    paramtype = 'string'

                path_parameter = {
                    'name': paramname,
                    'type': paramtype,
                    'in': 'path',
                    'required': True,
                }

                specs['parameters'].append(path_parameter)

                # replace in a new uri
                newuri = newuri.replace('<%s>' % parameter, '{%s}' % paramname)

            # cycle parameters and add them to the endpoint class
            query_params = []
            for param in specs['parameters']:

                if param["in"] != 'path':
                    if uri not in self._parameter_schemas:
                        self._parameter_schemas[uri] = {}

                    if method not in self._parameter_schemas[uri]:
                        self._parameter_schemas[uri][method] = []

                    self._parameter_schemas[uri][method].append(param.copy())

                extrainfo = param.pop('custom', {})

                if len(extrainfo) and endpoint.custom['schema']['expose']:

                    # TODO: read a 'custom.publish' in every yaml
                    # to decide if the /schema uri should be in swagger

                    if uri not in endpoint.custom['params']:
                        endpoint.custom['params'][uri] = {}
                    endpoint.custom['params'][uri][method] = extrainfo

                enum = param.pop("enum", None)
                if enum is not None:
                    param["enum"] = []
                    for option in enum:
                        if isinstance(option, str):
                            param["enum"].append(option)
                        else:
                            # enum [{key1: value1}, {key2: value2}]
                            # became enum [key1, ke2]
                            for k in option:
                                param["enum"].append(k)

                # handle parameters in URI for Flask
                if param['in'] == 'query':
                    query_params.append(param)

            if len(query_params) > 0:
                self.query_parameters(
                    endpoint.cls, method=method, uri=uri, params=query_params
                )

            # Swagger does not like empty arrays
            if len(specs['parameters']) < 1:
                specs.pop('parameters')

            ##################
            # Save definition for checking
            if uri not in self._original_paths:
                self._original_paths[uri] = {}
            self._original_paths[uri][method] = specs

            ##################
            # Skip what the developers does not want to be public in swagger
            # NOTE: do not skip if in testing mode
            if not extra.publish and not self._customizer._testing:
                continue

            # Handle global tags
            if 'tags' not in specs and len(endpoint.tags) > 0:
                specs['tags'] = []
            for tag in endpoint.tags:
                self._used_swagger_tags[tag] = True
                if tag not in specs['tags']:
                    specs['tags'].append(tag)

            ##################
            # NOTE: whatever is left inside 'specs' will be
            # passed later on to Swagger Validator...

            # Save definition for publishing
            if newuri not in self._paths:
                self._paths[newuri] = {}
            self._paths[newuri][method] = specs

            log.verbose("Built definition '%s:%s'", method.upper(), newuri)

        endpoint.custom['methods'][method] = extra
        return endpoint

    def query_parameters(self, cls, method, uri, params):
        """
        apply decorator to endpoint for query parameters
        # self._params[classname][URI][method][name]
        """

        clsname = cls.__name__
        if clsname not in self._qparams:
            self._qparams[clsname] = {}
        if uri not in self._qparams[clsname]:
            self._qparams[clsname][uri] = {}
        if method not in self._qparams[clsname][uri]:
            self._qparams[clsname][uri][method] = {}

        for param in params:
            name = param['name']
            if name not in self._qparams[clsname][uri][method]:
                self._qparams[clsname][uri][method][name] = param

    def swaggerish(self):
        """
        Go through all endpoints configured by the current development.

        Provide the minimum required data according to swagger specs.
        """

        # Better chosen dinamically from endpoint.py
        schemes = ['http']
        if PRODUCTION:
            schemes = ['https']

        # A template base
        output = {
            # TODO: update to 3.0.1? Replace bravado with something else?
            # https://github.com/Yelp/bravado/issues/306
            "swagger": "2.0",
            "info": {"version": "0.0.1", "title": "Your application name"},
            "schemes": schemes,
            # "host": "localhost"  # chosen dinamically
            "basePath": "/",
            "securityDefinitions": {
                "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
                # "OauthSecurity": {
                #     "type": "oauth2",
                #     "tokenUrl": "https://oauth.simple.api/token",
                #     "flow": "accessCode",
                #     "authorizationUrl": "https://blabla/authorization",
                #     "scopes": {
                #         "admin": "Admin scope",
                #         "user": "User scope"
                #       }
                # }
                # TODO: check about scopes (roles?)
            },
            "security": [{"Bearer": []}],
        }

        ###################
        # Set existing values
        proj = self._customizer._configurations['project']
        if 'version' in proj:
            output['info']['version'] = proj['version']
        if 'title' in proj:
            output['info']['title'] = proj['title']

        ###################
        models = self.get_models()
        self._fdp = models.pop('FormDataParameters', {})

        key_found = False
        for k in ["definitions", "parameters", "responses"]:
            if k in models:
                output[k] = models.get(k, {})
                key_found = True

        #####################################################
        # I added this for back-compatibility on 21/09/2017.
        # Please remove me in the future
        if not key_found:
            log.warning(
                "Your swagger model file is obsolete, " + "please add *definitions* key"
            )
            log.info("Follow issue #59 for details")
            output['definitions'] = models
        #####################################################

        output['consumes'] = [JSON_APPLICATION]
        output['produces'] = [JSON_APPLICATION]

        ###################
        # Read endpoints swagger files
        for key, endpoint in enumerate(self._endpoints):

            endpoint.custom['methods'] = {}
            endpoint.custom['params'] = {}

            for method, file in endpoint.methods.items():
                # add the custom part to the endpoint

                # In this case we are passing the config dictionary, not the yaml file
                if isinstance(file, dict):
                    self._endpoints[key] = self.read_my_swagger(
                        method, endpoint, mapping=file
                    )
                else:
                    self._endpoints[key] = self.read_my_swagger(
                        method, endpoint, file=file
                    )

        ###################
        # Save query parameters globally
        self._customizer._query_params = self._qparams
        self._customizer._parameter_schemas = self._parameter_schemas
        output['paths'] = self._paths

        ###################
        tags = []
        for tag, desc in self._customizer._configurations['tags'].items():
            if tag not in self._used_swagger_tags:
                log.debug("Skipping unsed tag: %s", tag)
                continue
            tags.append({'name': tag, 'description': desc})
        output['tags'] = tags

        self._customizer._original_paths = self._original_paths
        return output

    def get_models(self):
        """ Read models from base/custom yaml files """

        # BASE definitions
        path = os.path.join(ABS_RESTAPI_PATH, MODELS_DIR)
        data = load_yaml_file('swagger', path=path)

        # EXTENDED definitions, if any
        if EXTENDED_PACKAGE == EXTENDED_PROJECT_DISABLED:
            extended_models = {}
        else:
            path = os.path.join(os.curdir, EXTENDED_PACKAGE, MODELS_DIR)
            # NOTE: with logger=False I skip the warning if this file doesn't exist
            extended_models = load_yaml_file(
                'swagger', path=path, skip_error=True, logger=False
            )

        # CUSTOM definitions
        path = os.path.join(os.curdir, CUSTOM_PACKAGE, MODELS_DIR)
        # NOTE: with logger=False I skip the warning if this file doesn't exist
        custom_models = load_yaml_file(
            'swagger', path=path, skip_error=True, logger=False
        )

        if extended_models is None:
            return mix(data, custom_models)

        m1 = mix(data, extended_models)
        return mix(m1, custom_models)

    def validation(self, swag_dict):
        """
        Based on YELP library,
        verify the current definition on the open standard
        """

        if len(swag_dict['paths']) < 1:
            raise AttributeError("Swagger 'paths' definition is empty")

        filepath = os.path.join(tempfile.gettempdir(), 'test.json')

        try:
            # Fix jsonschema validation problem
            # expected string or bytes-like object
            # http://j.mp/2hEquZy
            swag_dict = json.loads(json.dumps(swag_dict))
            # write it down
            # FIXME: can we do better than this?
            with open(filepath, 'w') as f:
                json.dump(swag_dict, f)
        except Exception as e:
            raise e
            # log.warning("Failed to temporary save the swagger definition")

        bravado_config = {
            'validate_swagger_spec': True,
            'validate_requests': False,
            'validate_responses': False,
            'use_models': False,
        }

        try:
            self._customizer._validated_spec = Spec.from_dict(
                swag_dict, config=bravado_config
            )
            log.debug("Swagger configuration is validated")
        except Exception as e:
            # raise e
            error = str(e).split('\n')[0]
            log.error("Failed to validate:\n%s\n", error)
            return False
        finally:
            os.remove(filepath)

        return True
