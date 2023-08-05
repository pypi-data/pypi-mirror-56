from gracie_dictionary_api import GracieBaseAPI


class geoEntitiesController(GracieBaseAPI):
    """Geo entities.  """

    _controller_name = "geoEntitiesController"

    def add(self, countryId, latitude, longitude, popularity, **kwargs):
        """

        Args:
            adminCode: (string): adminCode
            alias: (string): alias
            briefs: (string): briefs
            countryId: (string): countryId
            featureCodeId: (string): featureCodeId
            latitude: (number): latitude
            longitude: (number): longitude
            names: (string): names
            parentId: (string): parentId
            popularity: (integer): popularity
            population: (integer): population

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'adminCode': {'name': 'adminCode', 'required': False, 'in': 'query'}, 'alias': {'name': 'alias', 'required': False, 'in': 'query'}, 'briefs': {'name': 'briefs', 'required': False, 'in': 'query'}, 'countryId': {'name': 'countryId', 'required': True, 'in': 'query'}, 'featureCodeId': {'name': 'featureCodeId', 'required': False, 'in': 'query'}, 'latitude': {'name': 'latitude', 'required': True, 'in': 'query'}, 'longitude': {'name': 'longitude', 'required': True, 'in': 'query'}, 'names': {'name': 'names', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': True, 'in': 'query'}, 'population': {'name': 'population', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/add'
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
        api = '/geoEntity/delete'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def edit(self, id, **kwargs):
        """

        Args:
            adminCode: (string): adminCode
            featureCodeId: (string): featureCodeId
            id: (string): id
            latitude: (number): latitude
            longitude: (number): longitude
            parentId: (string): parentId
            popularity: (integer): popularity
            population: (integer): population

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'adminCode': {'name': 'adminCode', 'required': False, 'in': 'query'}, 'featureCodeId': {'name': 'featureCodeId', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'latitude': {'name': 'latitude', 'required': False, 'in': 'query'}, 'longitude': {'name': 'longitude', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'population': {'name': 'population', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/edit'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, name, **kwargs):
        """

        Args:
            languageId: (string): languageId
            limit: (integer): limit
            name: (string): name
            offset: (integer): offset
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy
            parentId: (string): parentId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/list'
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
        api = '/geoEntity/restore'
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
        api = '/geoEntity/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
