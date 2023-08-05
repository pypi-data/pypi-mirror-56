from gracie_dictionary_api import GracieBaseAPI


class performanceController(GracieBaseAPI):
    """Text processing performance measurement"""

    _controller_name = "performanceController"

    def enable(self, enabled):
        """

        Args:
            enabled: (boolean): enabled

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/performance/enable'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/performance/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
