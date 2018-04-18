ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

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

    def __init__(self, host, username='admin', password='Password123!'):
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
            resource_id = update_data['id']
            return self._modify(resource_type, resource_id, update_data)
        if action == 'delete':
            resource_id = update_data['id']
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
            url = '/api/types/' + resource_type + '/instances'
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
