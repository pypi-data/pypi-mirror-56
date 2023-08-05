from gracie_feeds_api import GracieBaseAPI


class alertRulesController(GracieBaseAPI):
    """Alert rule defines a method of processing the data in Elasticsearch."""

    _controller_name = "alertRulesController"

    def add(self, alertRuleName, projectId, **kwargs):
        """Create new alert rule for project.

        Args:
            alertRuleName: (string): alertRuleName
            description: (string): description
            isRunning: (boolean): isRunning
            projectId: (string): projectId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleName': {'name': 'alertRuleName', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alertRules/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def edit(self, alertRuleId, isRunning, **kwargs):
        """Edit existing alert rule.

        Args:
            alertRuleId: (string): alertRuleId
            alertRuleName: (string): alertRuleName
            description: (string): description
            isRunning: (boolean): isRunning

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}, 'alertRuleName': {'name': 'alertRuleName', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alertRules/edit'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, projectId):
        """Return list of alert rules for project.

        Args:
            projectId: (string): projectId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alertRules/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def remove(self, alertRuleId):
        """Remove existing alert rule.

        Args:
            alertRuleId: (string): alertRuleId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alertRules/remove'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, alertRuleId):
        """Return the alert rule by ID.

        Args:
            alertRuleId: (string): alertRuleId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alertRules/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
