from gracie_feeds_api import GracieBaseAPI


class rulesController(GracieBaseAPI):
    """Manager of all loaded rules"""

    _controller_name = "rulesController"

    def list(self, **kwargs):
        """Return the list of all rules.

        Args:
            locale: (string): locale

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'locale': {'name': 'locale', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/rules/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, ruleId, **kwargs):
        """Return the rule.

        Args:
            locale: (string): locale
            ruleId: (string): ruleId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'locale': {'name': 'locale', 'required': False, 'in': 'query'}, 'ruleId': {'name': 'ruleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/rules/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
