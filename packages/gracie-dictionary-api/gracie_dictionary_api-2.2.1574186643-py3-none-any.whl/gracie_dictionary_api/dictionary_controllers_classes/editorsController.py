from gracie_dictionary_api import GracieBaseAPI


class editorsController(GracieBaseAPI):
    """Editor - is someone who can edit data in the database. """

    _controller_name = "editorsController"

    def assignAll(self, dictionariesAssignment):
        """

        Args:
            dictionariesAssignment: (string): dictionariesAssignment

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dictionariesAssignment': {'name': 'dictionariesAssignment', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/editors/assignAll'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def assignCountry(self, dictionaryId, editorId, **kwargs):
        """

        Args:
            assign: (boolean): assign
            dictionaryId: (string): dictionaryId
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'assign': {'name': 'assign', 'required': False, 'in': 'query'}, 'dictionaryId': {'name': 'dictionaryId', 'required': True, 'in': 'query'}, 'editorId': {'name': 'editorId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/editors/assignCountry'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def assignTopic(self, dictionaryId, editorId, **kwargs):
        """

        Args:
            assign: (boolean): assign
            dictionaryId: (string): dictionaryId
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'assign': {'name': 'assign', 'required': False, 'in': 'query'}, 'dictionaryId': {'name': 'dictionaryId', 'required': True, 'in': 'query'}, 'editorId': {'name': 'editorId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/editors/assignTopic'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def countriesList(self, **kwargs):
        """

        Args:
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'editorId': {'name': 'editorId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/editors/countriesList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/editors/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def listAll(self, editorId):
        """

        Args:
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'editorId': {'name': 'editorId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/editors/listAll'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def topicsList(self, **kwargs):
        """

        Args:
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'editorId': {'name': 'editorId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/editors/topicsList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
