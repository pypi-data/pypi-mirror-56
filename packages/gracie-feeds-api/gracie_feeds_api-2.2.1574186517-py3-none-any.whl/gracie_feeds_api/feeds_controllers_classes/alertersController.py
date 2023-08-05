from gracie_feeds_api import GracieBaseAPI


class alertersController(GracieBaseAPI):
    """Alerters management."""

    _controller_name = "alertersController"

    def addEmailAlerter(self, alertRuleId, email, name, **kwargs):
        """Create new Email alerter for alert rule.

        Args:
            alertRuleId: (string): alertRuleId
            bcc: (array): bcc
            description: (string): description
            email: (array): email
            name: (string): name

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}, 'bcc': {'name': 'bcc', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'email': {'name': 'email', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alerters/addEmailAlerter'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def alerterTypesList(self):
        """Return list of alerters types."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/alerters/alerterTypesList'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def editEmailAlerter(self, alerterId, **kwargs):
        """Edit Email alerter for alert rule.

        Args:
            alerterId: (string): alerterId
            bcc: (array): bcc
            description: (string): description
            email: (array): email

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alerterId': {'name': 'alerterId', 'required': True, 'in': 'query'}, 'bcc': {'name': 'bcc', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'email': {'name': 'email', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alerters/editEmailAlerter'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, alertRuleId):
        """Return list of alerters for alertRule.

        Args:
            alertRuleId: (string): alertRuleId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alerters/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def remove(self, alerterId):
        """Remove existing alerter.

        Args:
            alerterId: (string): alerterId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alerterId': {'name': 'alerterId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alerters/remove'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, alerterId):
        """Return an alerter by ID.

        Args:
            alerterId: (string): alerterId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'alerterId': {'name': 'alerterId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/alerters/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
