from gracie_dictionary_api import GracieBaseAPI


class approversController(GracieBaseAPI):
    """Approver is someone who can approve edited by editors data in the database."""

    _controller_name = "approversController"

    def assignAll(self, editorsAssignment):
        """

        Args:
            editorsAssignment: (string): editorsAssignment

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'editorsAssignment': {'name': 'editorsAssignment', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/assignAll'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def assignCountry(self, approverId, dictionaryId, **kwargs):
        """

        Args:
            approverId: (string): approverId
            assign: (boolean): assign
            dictionaryId: (string): dictionaryId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': True, 'in': 'query'}, 'assign': {'name': 'assign', 'required': False, 'in': 'query'}, 'dictionaryId': {'name': 'dictionaryId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/assignCountry'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def assignEditor(self, approverId, editorId, **kwargs):
        """

        Args:
            approverId: (string): approverId
            assign: (boolean): assign
            editorId: (string): editorId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': True, 'in': 'query'}, 'assign': {'name': 'assign', 'required': False, 'in': 'query'}, 'editorId': {'name': 'editorId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/assignEditor'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def assignTopic(self, approverId, dictionaryId, **kwargs):
        """

        Args:
            approverId: (string): approverId
            assign: (boolean): assign
            dictionaryId: (string): dictionaryId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': True, 'in': 'query'}, 'assign': {'name': 'assign', 'required': False, 'in': 'query'}, 'dictionaryId': {'name': 'dictionaryId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/assignTopic'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def countriesList(self, **kwargs):
        """

        Args:
            approverId: (string): approverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/countriesList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def editorsList(self, **kwargs):
        """

        Args:
            approverId: (string): approverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/editorsList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/approvers/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def listAll(self, approverId):
        """

        Args:
            approverId: (string): approverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/listAll'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def topicsList(self, **kwargs):
        """

        Args:
            approverId: (string): approverId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'approverId': {'name': 'approverId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/approvers/topicsList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
