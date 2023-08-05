from gracie_feeds_api import GracieBaseAPI


class filtersController(GracieBaseAPI):
    """Filters management."""

    _controller_name = "filtersController"

    def getFiltersTree(self, alertRuleId):
        """Get filters tree.

        Args:
            alertRuleId: (string): alertRuleId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/getFiltersTree'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def removeFiltersTree(self, alertRuleId):
        """Remove filters tree.

        Args:
            alertRuleId: (string): alertRuleId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/removeFiltersTree'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def setFiltersTree(self, alertRuleId, filters):
        """Set filters tree.

        Args:
            alertRuleId: (string): alertRuleId
            filters: (string): filters

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}, 'filters': {'name': 'filters', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/setFiltersTree'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
