from gracie_dictionary_api import GracieBaseAPI


class geoCodesController(GracieBaseAPI):
    """Phone and postal codes."""

    _controller_name = "geoCodesController"

    def add(self, code, entityId, typeId):
        """

        Args:
            code: (string): code
            entityId: (string): entityId
            typeId: (string): typeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'code': {'name': 'code', 'required': True, 'in': 'query'}, 'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, entityId, typeId):
        """

        Args:
            entityId: (string): entityId
            typeId: (string): typeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def remove(self, codeId):
        """

        Args:
            codeId: (string): codeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'codeId': {'name': 'codeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/remove'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, codeId):
        """

        Args:
            codeId: (string): codeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'codeId': {'name': 'codeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def typesList(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/geo-codes/typesList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
