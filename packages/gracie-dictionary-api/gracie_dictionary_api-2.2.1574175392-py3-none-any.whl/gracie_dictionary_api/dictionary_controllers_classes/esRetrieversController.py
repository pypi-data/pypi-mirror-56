from gracie_dictionary_api import GracieBaseAPI


class esRetrieversController(GracieBaseAPI):
    """Retrieve documents from ElasticSearch."""

    _controller_name = "esRetrieversController"

    def add(self, host, index, name, port, **kwargs):
        """

        Args:
            description: (string): description
            host: (string): host
            index: (string): index
            name: (string): name
            port: (integer): port

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'host': {'name': 'host', 'required': True, 'in': 'query'}, 'index': {'name': 'index', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'port': {'name': 'port', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def assign(self, editorId, retrieverId, **kwargs):
        """

        Args:
            assign: (boolean): assign
            editorId: (string): editorId
            retrieverId: (string): retrieverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'assign': {'name': 'assign', 'required': False, 'in': 'query'}, 'editorId': {'name': 'editorId', 'required': True, 'in': 'query'}, 'retrieverId': {'name': 'retrieverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/assign'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def edit(self, retrieverId, **kwargs):
        """

        Args:
            description: (string): description
            host: (string): host
            index: (string): index
            port: (integer): port
            retrieverId: (string): retrieverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'host': {'name': 'host', 'required': False, 'in': 'query'}, 'index': {'name': 'index', 'required': False, 'in': 'query'}, 'port': {'name': 'port', 'required': False, 'in': 'query'}, 'retrieverId': {'name': 'retrieverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/edit'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def getDocument(self, retrieverId):
        """

        Args:
            retrieverId: (string): retrieverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'retrieverId': {'name': 'retrieverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/getDocument'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def getDocumentsToClusterSet(self, clusterSetId, documentsNumber, retrieverId, **kwargs):
        """

        Args:
            clusterSetId: (string): clusterSetId
            documentsNumber: (integer): documentsNumber
            languageId: (string): languageId
            retrieverId: (string): retrieverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterSetId': {'name': 'clusterSetId', 'required': True, 'in': 'query'}, 'documentsNumber': {'name': 'documentsNumber', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'retrieverId': {'name': 'retrieverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/getDocumentsToClusterSet'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, **kwargs):
        """

        Args:
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'editorId': {'name': 'editorId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def remove(self, retrieverId):
        """

        Args:
            retrieverId: (string): retrieverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'retrieverId': {'name': 'retrieverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/remove'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, retrieverId):
        """

        Args:
            retrieverId: (string): retrieverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'retrieverId': {'name': 'retrieverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/es-retrievers/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
