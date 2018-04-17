ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_unity
short_description: Configure and manage Dell EMC Unity Storage System
description:
    - This module can be used to configure and manage Dell EMC Unity Storage System.
    - The module supports check mode.
version_added: "2.2"
author:
    - "Jiale Huo (jiale.huo@emc.com)"
    - "Craig Smith (craig.j.smith@emc.com)"
options:
    unity_hostname:
        description:
            - Hostname of the Unity system's management interface.
        required: true
        type: string
    unity_username:
        description:
            - Username of the Unity system's default administrator user.
        required: false
        default: "admin"
        type: string
    unity_password:
        description:
            - Password of the Unity system's default administrator user.
        required: false
        default: "Password123#"
        type: string
    unity_license_path:
        description:
            - Path to the license file of the Unity system.
        required: false
        type: string
    unity_updates:
        description: 
            - Update resources of the Unity system.
            - See "Unisphere Management REST API Programer's Guide" for examples of how to update Unity system resources.
            - See "Unisphere Management REST API Reference Guide" for details and arguments of each individual resource's update operations.
        required: false
        type: list
        suboptions:
            resource_type:
                description:
                    - Type of the resource to be queried.
                required: true
                type: string
            id:
                description:
                    - ID of an instance of the resouce type to be updated.
                    - If this option is present, then instance update of the resouce type will be executed.
                    - Otherwise, if this option is missing, then the update operation either creates a new instance, or executes a class-level action.
                    - If the "action" option is present, then a class-level action on the resource type is executed.
                    - Otherwise, if the "action" option is missing, then a new instance of the resource type is created.
                required: false
                type: string
            action:
                description:
                    - Action of the update operation.
                    - If the "id" option is present, then the action is executed on the instance.
                    - Otherwise, if the "id" option is missing, then the action is executed at the class-level on the resouce type. 
                required: false
                default: "modify"
                type: string
            attributes:
                description:
                    - The attributes to compare to decide whether an update should be executed.
                    - If attributes are missing, then the default, hard-coded attribute will be compared against the existing values.
                    - If attributes is a list, then queries of attributes of the same names will be compared to the ones in the update.
                    - Sometimes an attribute in the query field is different from that as an update argument, in this case, a dictionary mapping queried attributes to update arguments can be used.
                    - If the update is on an instance with ID, then the attributes specifies which one of the current values of the instance should be compared with the values to be updated. If all values are the same, then the update will not be executed, but a warning will be issued.
                    - If the update is to create a new instance, then the attributes are used to search for instances of the same attribute values. If such duplicates exist, a warning will be issued in check mode.
                    - Dotted attributes can be used to compare related resources.
                required: false
                type: list or dictionary
            filter:
                description:
                    - A filter for query to find duplicates of an instance creation update.
                    - See "Unisphere Management REST API Programmer's Guide" for details on how to create a filter for queries.
                    - It can be a partial filter, complemented by the list of attributes to compare.
                    - If the filter is missing, then the default, hard-coded filter will be used.
                required: false
                type: string
            language:
                description:
                    - Overrides the value of the Accept-language: header.
                    - This is useful for testing from a plain browser or from an environment where URL parameters are easier to use than HTTP headers.
                    - The language parameter specifies the localization language for error messages, events, alerts, and other localizable responses.
                required: false
                choices:
                    - de-DE: German
                    - en-US: English
                    - es-MX: Latin American Spanish
                    - fr-FR: French
                    - ja-JP: Japanese
                    - ko-KR: Korean
                    - pt-BR: Brazilian Portuguese
                    - ru-RU: Russian
                    - zh-CN: Chinese
                default: en-US
                type: string
            timeout:
                description:
                    - Seconds before timeout.
                    - Executes the request in the background. Most active management requests (ones that attempt to change the configuration) support this option. 
                    - The documentation for each API method in the Unisphere Management REST API Reference Guide specifies whether the method supports this option.
                required: false
                type: int
    unity_password_updates:
        description: 
            - Update passwords of users of the Unity system. a
        required: false
        type: list
        suboptions:
            username: 
                description:
                    - Name of the user.
                required: true
                type: string
            password:
                description:
                    - Current password of the user.
                required: true
                type: string
            new_password:
                description:
                    - New passowrd of the user.
                required: true
                type: string
    unity_queries:
        description:
            - Query the Unity system for resource information.
            - See "Unisphere Management REST API Programmer's Guide" for detailed description and examples of the query parameters.
            - See "Unisphere Management REST API Reference Guide" for details and attributes (field names) of each individual resource's query operations.
        required: false
        type: list
        suboptions:
            resource_type:
                description:
                    - Type of the resource to be queried.
                required: true
                type: string
            id:
                description:
                    - ID of an instance of the resouce type to be queried.
                    - If this option is missing, then collection query of the resource type will be executed.
                    - Otherwise, if this option is present, then instance query of the resource type will be executed.
                required: false
                type: string
            compact:
                description:
                    - Omits metadata from each instance in the query response.
                required: false
                default: true
                type: bool
            fields:
                description:
                    - Specifies a comma-separated list of attributes to return in a response.
                    - If you do not use this parameter, a query will return the id attribute only.
                    - When using fields, you can:
                        - Use dot notation syntax to return the values of related attributes.
                        - Optionally, define a new attribute from field expressions associated with one or more existing attributes.
                required: false
                type: string
            filter:
                description:
                    - Filters the response data against a set of criteria. Only matching resource instances are returned. Filtering is case insensitive.
                    - When using filter, you can use dot notation syntax to filter by the attributes of related resource types.
                    - Only applies to collection query requests.
                required: false
                type: string
            groupby:
                description:
                    - Groups the specified values and applies the @sum function to each group.
                    - For example, you could use groupby with @sum to return a summary of disk sizes for each disk type.
                    - Only applies to collection query requests.
                required: false
                type: string
            language:
                description:
                    - Overrides the value of the Accept-language: header.
                    - This is useful for testing from a plain browser or from an environment where URL parameters are easier to use than HTTP headers.
                    - The language parameter specifies the localization language for error messages, events, alerts, and other localizable responses.
                required: false
                choices:
                    - de-DE: German
                    - en-US: English
                    - es-MX: Latin American Spanish
                    - fr-FR: French
                    - ja-JP: Japanese
                    - ko-KR: Korean
                    - pt-BR: Brazilian Portuguese
                    - ru-RU: Russian
                    - zh-CN: Chinese
                default: en-US
                type: string
            orderby:
                description:
                    - Specifies how to sort response data. You can sort response data in ascending or descending order by the attributes of the queried resource type. And you can use dot notation syntax to sort response data by the attributes of related resource types.
                    - Only applies to collection query requests.
                required: false
                type: string
            page:
                description:
                    - Identifies the page to return in a response by specifying the page number. If this parameter is not specified, the server returns all resource instances that meet the request criteria in page 1.
                    - Only applies to collection query requests.
                required: false
                type: int
            per_page:
                description:
                    - Specifies the number of resource type instances that form a page. If this parameter is not specified, the server returns all resource instances that meet the request criteria in the page specified by page (or in page 1, if page is also not specified).
                    - The server imposes an upper limit of 2000 on the number of resource instances returned in a page.
                    - Only applies to collection query requests.
                required: false
                type: int
            with_entrycount:
                description:
                    - Indicates whether to return the entryCount response component in the response data. The entryCount response component indicates the number of resource instances in the complete list. You can use it to get the total number of entries when paging returned a partial response.
                    - By default, the entryCount response component is not returned. Set with_entrycount=true to return the entryCount response component.
                    - Only applies to collection query requests.
                required: false
                default: true
                type: bool
notes:
    - GitHub project: U(https://github.com/jialehuo/ansible-dellemc-unity)
    - This module supports check mode.
requirements:
    - Python >= 2.7
    - requests >= 1.3
    - Unity >= 4.0
'''

EXAMPLES = '''
- name: Initial setup
  dellemc_unity:
    unity_hostname: "192.168.0.100"
    unity_username: admin
    unity_password: Password123#
    unity_updates:
      - {resource_type: system, id: '0', attributes: {'isEULAAccepted':'isEulaAccepted'}, isEulaAccepted: 'true'}
    unity_password_updates:
      - {username: admin, password: Password123#, new_password: Password123!}
    unity_license_path: /home/labadmin/unity.lic

- name: Updates and queries
  dellemc_unity:
    unity_hostname: "192.168.0.202"
    unity_username: admin
    unity_password: Password123!
    unity_updates:
      - {resource_type: user, name: test1, password: Welcome1!, role: administrator, attributes: [name]}
      - {resource_type: user, id: 'user_test1', attributes: {'role.id':'role'}, role: 'operator'}
      - {resource_type: remoteSyslog, id: '0', enabled: True, address: '192.168.0.11:515', protocol: 1, facility: 0}
      - {resource_type: dnsServer, id: '0', addresses: [10.254.66.23, 10.254.66.24]}
      - {resource_type: ntpServer, id: '0', attributes: [addresses], addresses: [10.254.140.21, 10.254.140.22], rebootPrivilege: 2}
    unity_password_updates:
      - {username: test1, password: Welcome1!, new_password: Welcome2!}
    unity_queries:
      - {resource_type: user, id: 'user_test1', fields: 'role.id'}
      - {resource_type: remoteSyslog, id: "0", fields: 'address,protocol,facility,enabled'}      # id parameter has to be of the string type
      - {resource_type: dnsServer, fields: "domain, addresses, origin", page: 1, per_page: 100}
      - {resource_type: ntpServer, id: "0", fields: addresses}      # id parameter has to be of the string type

- name: Deletes
  dellemc_unity:
    unity_hostname: "192.168.0.202"
    unity_username: admin
    unity_password: Password123!
    unity_updates:
      - {resource_type: user, id: 'user_test1', action: 'delete'}
'''

RETURN = '''
unity_query_results:
    description:
        - A list of JSON objects detailing the results of each successful query operation.
    returned: always
    type: list
    sample: >
        "unity_query_results": [
            {
                "entries": [
                    {
                        "content": {
                            "id": "user_test1", 
                            "role": {
                                "id": "operator"
                            }
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "role.id", 
                    "id": "user_test1", 
                    "resource_type": "user"
                }, 
                "url": "https://192.168.0.202/api/instances/user/user_test1?compact=true&fields=role.id"
            }, 
            {
                "entries": [
                    {
                        "content": {
                            "address": "192.168.0.11:515", 
                            "enabled": true, 
                            "facility": 0, 
                            "id": "0", 
                            "protocol": 1
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "address,protocol,facility,enabled", 
                    "id": "0", 
                    "resource_type": "remoteSyslog"
                }, 
                "url": "https://192.168.0.202/api/instances/remoteSyslog/0?compact=true&fields=address%2Cprotocol%2Cfacility%2Cenabled"
            }, 
            {
                "entries": [
                    {
                        "content": {
                            "addresses": [
                                "10.254.66.23", 
                                "10.254.66.24"
                            ], 
                            "id": "0", 
                            "origin": 2
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "domain, addresses, origin", 
                    "page": 1, 
                    "per_page": 100, 
                    "resource_type": "dnsServer"
                }, 
                "url": "https://192.168.0.202/api/types/dnsServer/instances?compact=true&fields=domain%2C+addresses%2C+origin&with_entrycount=true&page=1&per_page=100"
            }, 
            {
                "entries": [
                    {
                        "content": {
                            "addresses": [
                                "10.254.140.21", 
                                "10.254.140.22"
                            ], 
                            "id": "0"
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "addresses", 
                    "id": "0", 
                    "resource_type": "ntpServer"
                }, 
                "url": "https://192.168.0.202/api/instances/ntpServer/0?compact=true&fields=addresses"
            }
        ]
    contains:
        entries:
            description:
                - A list of JSON objects for each instance of the resource type returned by the query.
            returned: always
            type: complex
            contains:
                content:
                    description:
                        - Content of the instance.
                        - Contains at least the ID of the instance, and possibly other fields specified by the 'fields' parameter in the 'unity_queries' option.
                    returned: always
                    type: complex
        entryCount:
            description:
                - Count of entries returned.
            type: int
        query:
            description:
                - The original query.
            returned: always
            type: complex
        url:
            description:
                - URL of the query.
            returned: always
            type: string

unity_update_results:
    description:
        - A list of JSON objects detailing the results of each operation.
    returned: always
    type: list
    sample: >
        "unity_update_results": [
            {
                "args": {
                    "name": "test1", 
                    "password": "Welcome1!", 
                    "role": "administrator"
                }, 
                "HTTP_method": "POST",
                "response": {
                    "@base": "https://192.168.0.202/api/instances/user", 
                    "content": {
                        "id": "user_test1"
                    }, 
                    "links": [
                        {
                            "href": "/user_test1", 
                            "rel": "self"
                        }
                    ], 
                    "updated": "2017-04-04T13:32:05.837Z"
                },
                "url": "https://192.168.0.202/api/types/user/instances"
            }, 
            {
                "args": {
                    "address": "192.168.0.11:515", 
                    "enabled": true, 
                    "facility": 0, 
                    "protocol": 1
                }, 
                "HTTP_method": "POST",
                "url": "https://192.168.0.202/api/instances/remoteSyslog/0/action/modify"
            }, 
            {
                "update": {
                    "addresses": [
                        "10.254.66.23", 
                        "10.254.66.24"
                    ], 
                    "id": "0", 
                    "resource_type": "dnsServer"
                }, 
                "warning": "The existing instances already has the same attributes as the update operation. No update will happen."
            }, 
            {
                "args": {
                    "addresses": [
                        "10.254.140.21", 
                        "10.254.140.22"
                    ], 
                    "rebootPrivilege": 2
                }, 
                "HTTP_method": "POST",
                "url": "https://192.168.0.202/api/instances/ntpServer/0/action/modify"
            },
            {
                "HTTP_method": "DELETE", 
                "url": "https://192.168.0.202/api/instances/user/user_test1"
            }
        ]
    contains:
        HTTP_method:
            description:
                - HTTP method used to effect the update.
            returned: success
            type: string
        url:
            description:
                - URL of the operation to change the resource.
            returned: success
            type: string
        args:
            description:
                - Arguments of the operation to change the resource.
            returned: success
            type: complex
        response:
            description:
                - Non-empty response of the update operation from the Unity system.
            returned: success
            type: complex
        update:
            description:
                - The original update request.
                - Only returned when the update failed.
            returned: failure
            type: complex
        message:
            description:
                - Warning or failure message of the failed update operation.
            returned: failure
            type: string

'''

import requests, json, re

__author__ = "Andrew Petrov"
__maintainer__ = "Andrew Petrov"
__email__ = "marsofandrew@gmail.com"


class Unity:

    def __init__(self, host, username='admin', password='Password123#'):
        self.hostname = host
        self.username = username
        self.password = password

        self.apibase = 'https://' + self.hostname  # Base URL of the REST API
        self.headers = {'X-EMC-REST-CLIENT': 'true', 'content-type': 'application/json',
                        'Accept': 'application/json'}  # HTTP headers for REST API requests, less the 'EMC-CSRF-TOKEN' header
        self.session = requests.Session()

        self.changed = False
        self.updateResults = []
        self.queryResults = []
        self.err = None

        self._start_session()

    def __del__(self):
        self._stop_session()

    def reset(self):
        self.changed = False
        self.updateResults = []
        self.queryResults = []
        self.err = None

    def _create(self, resource_type, update):  # TODO:maybe fix it
        paramKeys = ['language', 'timeout']
        urlKeys = ['attributes', 'filter'] + paramKeys
        url = '/api/types/' + resource_type + '/instances'

        params = {key: update[key] for key in update if key in paramKeys}
        args = {key: update[key] for key in update if key not in urlKeys}
        msg = {}
        return self._do_post(url, args, params=params, msg=msg)

    def _modify(self, resource_type, resource_id, update):
        paramKeys = ['language', 'timeout']
        urlKeys = ['resource_type', 'id', 'action', 'attributes', 'filter'] + paramKeys
        params = {key: update[key] for key in update if key in paramKeys}
        args = {key: update[key] for key in update if key not in urlKeys}
        msg = {}

        url = '/api/instances/' + resource_type + '/' + resource_id + '/action/' + 'modify'
        return self._do_post(url, args, params=params, msg=msg)

    def _delete(self, resource_type, resource_id):
        url = '/api/instances/' + resource_type + '/' + resource_id
        msg = {}
        return self._do_delete(url, msg)

    def _do_specific_action(self, resource_type, action, update):
        paramKeys = ['language', 'timeout']
        urlKeys = ['resource_type', 'id', 'action', 'attributes', 'filter'] + paramKeys
        params = {key: update[key] for key in update if key in paramKeys}
        args = {key: update[key] for key in update if key not in urlKeys}
        msg = {}
        url = '/api/types/' + resource_type + '/action/' + action
        return self._do_post(url, args, params=params, msg=msg)

    def update(self, action, resource_type, update_data):
        if action == 'create':
            return self._create(resource_type, update_data)
        if action == 'modify':
            resource_id = 0
            return self._modify(resource_type, resource_id, update_data)
        if action == 'delete':
            resource_id = 0
            return self._delete(resource_type, resource_id)
        return self._do_specific_action(resource_type, action, update_data)

    def query(self, resource_type, query_data):
        instanceKeys = ['compact', 'fields', 'language']  # Instance query keys
        collectionKeys = ['compact', 'fields', 'filter', 'groupby', 'language', 'orderby', 'page', 'per_page',
                          'with_entrycount']
        if 'id' in query_data:
            url = '/api/instances/' + resource_type + '/' + query_data['id']
            paramKeys = instanceKeys
        else:
            url = '/api/types/' + query_data['resource_type'] + '/instances'
            paramKeys = collectionKeys
        params = {key: query_data[key] for key in paramKeys if
                  key in query_data}
        if 'compact' not in params:
            params['compact'] = 'true'  # By default, omit metadata from each instance in the query response

        if 'id' not in query_data and 'with_entrycount' not in params:  # Collection query without the 'with_entrycount' parameter
            params['with_entrycount'] = 'true'  # By default, return the entryCount response component in the response data.
        resp = self._do_get(url, params)
        r = json.loads(resp.text)  # ?????????????????????????? r ?????????????????
        result = {'resource_type': resource_type}
        if 'id' in query_data:
            result['id'] = query_data['id']
            result.update(r['content'])
        else:
            result['entries'] = []
            for entry in r['entries']:
                result['entries'].append(entry['content'])
        return result

    # def run_password_update(self, update):  # TODO: Fix it
    #    username = update.get('username')
    #    password = update.get('password')
    #    newPassword = update.get('new_password')
    #    kwargs = {'auth': requests.auth.HTTPBasicAuth(username, password), 'headers': self.headers, 'verify': False}
    #    resp = requests.get(self.apibase + '/api/instances/system/0', **kwargs)
    #    self._get_result(resp, **kwargs)  # process get results
    #    update = {'resource_type': 'user', 'id': 'user_' + username, 'password': newPassword, 'oldPassword': password}
    #    self.run_update(update)

    def _start_session(self):
        url = '/api/instances/system/0'
        auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        resp = self._do_get(url, auth=auth)
        # Add 'EMC-CSRF-TOKEN' header
        self.headers['EMC-CSRF-TOKEN'] = resp.headers['EMC-CSRF-TOKEN']

    def _stop_session(self):
        url = '/api/types/loginSessionInfo/action/logout'
        args = {'localCleanupOnly': 'true'}
        self._do_post(url, args, changed=False)

    def _get_msg(self, resp):
        try:
            msg = json.loads(resp.text)
        except ValueError:
            msg = {'httpStatusCode': resp.status_code, 'messages': [{'en-US': resp.text}]}
        return msg

    def _get_result(self, resp, **kwargs):
        if resp.status_code // 100 == 2:  # HTTP status code 2xx = success
            return resp

        self.err = self._get_msg(resp)
        self.err.update({'url': resp.url})

        if resp.status_code == 401 and kwargs.get('auth'):  # Unauthorized password
            self.err['messages'][0]['en-US'] = "Authentication error for User '" + kwargs['auth'].username + "'"  # Update error message

    def _change_result(self, resp, url, args=None, changed=True, msg=None, **kwargs):
        if resp:
            url = resp.url
        elif 'params' in kwargs:  # Reconstruct URL with parameters
            url += '?'
            for key, value in kwargs['params'].items():
                url += key + '=' + value + '&'
            url = url.strip('?&')
        if (resp is None) or (resp and resp.status_code // 100 == 2):
            if changed:
                self.changed = changed
            if changed or msg:
                changeContent = {'changed': changed}
                if args:
                    changeContent['args'] = args
                if resp and resp.text:  # append response if it exists
                    changeContent['response'] = json.loads(resp.text)
                if msg:  # append messages if they exist
                    changeContent.update(msg)
                self.updateResults.append(changeContent)
        else:
            self.err = self._get_msg(resp)
            self.err['url'] = resp.url
            if args is not None:
                self.err['args'] = args

    def _do_get(self, url, params=None, **kwargs):
        kwargs = self._add_headers_to_kwargs(**kwargs)
        resp = self.session.get(self.apibase + url, params=params, **kwargs)
        self._get_result(resp, **kwargs)
        return resp

    def _do_post(self, url, args, changed=True, msg=None, **kwargs):
        kwargs = self._add_headers_to_kwargs(**kwargs)
        resp = self.session.post(self.apibase + url, json=args, **kwargs)
        self._change_result(resp, url, args, changed=changed, msg=msg, **kwargs)
        return resp

    def _do_delete(self, url, msg=None, **kwargs):  # TODO: remake it
        kwargs = self._add_headers_to_kwargs(**kwargs)
        resp = self.session.delete(self.apibase + url, **kwargs)
        self._change_result(resp, url, msg=msg, **kwargs)
        return resp

    def _add_headers_to_kwargs(self, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs.update({'headers': self.headers, 'verify': False})
        return kwargs
