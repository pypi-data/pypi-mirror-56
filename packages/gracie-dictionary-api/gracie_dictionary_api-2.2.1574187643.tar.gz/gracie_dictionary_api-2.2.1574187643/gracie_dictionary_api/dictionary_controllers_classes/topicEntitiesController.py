from gracie_dictionary_api import GracieBaseAPI


class topicEntitiesController(GracieBaseAPI):
    """Topic entity."""

    _controller_name = "topicEntitiesController"

    def add(self, popularity, topicTypeId, **kwargs):
        """

        Args:
            alias: (string): alias
            briefs: (string): briefs
            names: (string): names
            popularity: (integer): popularity
            topicTypeId: (string): topicTypeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alias': {'name': 'alias', 'required': False, 'in': 'query'}, 'briefs': {'name': 'briefs', 'required': False, 'in': 'query'}, 'names': {'name': 'names', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': True, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def clone(self, id, topicTypeId, **kwargs):
        """

        Args:
            deleteSource: (boolean): deleteSource
            id: (string): id
            popularity: (integer): popularity
            topicTypeId: (string): topicTypeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'deleteSource': {'name': 'deleteSource', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/clone'
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
        api = '/topicEntity/delete'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def downloadExportFile(self, taskId):
        """

        Args:
            taskId: (string): taskId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'taskId': {'name': 'taskId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/downloadExportFile'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): id
            popularity: (integer): popularity
            topicTypeId: (string): topicTypeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/edit'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def exportTopicEntities(self, topicTypeId, **kwargs):
        """

        Args:
            languageId: (string): languageId
            topicTypeId: (string): topicTypeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/exportTopicEntities'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def importTopicEntities(self, file, topicTypeId, **kwargs):
        """

        Args:
            file: (file): file
            languageId: (string): languageId
            stopOnError: (boolean): stopOnError
            topicTypeId: (string): topicTypeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'stopOnError': {'name': 'stopOnError', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/importTopicEntities'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, name, **kwargs):
        """

        Args:
            languageId: (string): languageId
            limit: (integer): limit
            name: (string): Prefix of searched name
            offset: (integer): offset
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy
            topicId: (string): topicId
            topicTypeId: (string): topicTypeId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'topicId': {'name': 'topicId', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def restore(self, id):
        """

        Args:
            id: (string): id

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/restore'
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
        api = '/topicEntity/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
