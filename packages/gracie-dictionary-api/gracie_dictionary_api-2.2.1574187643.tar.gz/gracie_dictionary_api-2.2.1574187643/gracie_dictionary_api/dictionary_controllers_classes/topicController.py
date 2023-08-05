from gracie_dictionary_api import GracieBaseAPI


class topicController(GracieBaseAPI):
    """Topic"""

    _controller_name = "topicController"

    def add(self, name):
        """

        Args:
            name: (string): name

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topic/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def delete(self, id):
        """

        Args:
            id: (string): id

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topic/delete'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, **kwargs):
        """

        Args:
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topic/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, id):
        """

        Args:
            id: (string): id

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topic/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
