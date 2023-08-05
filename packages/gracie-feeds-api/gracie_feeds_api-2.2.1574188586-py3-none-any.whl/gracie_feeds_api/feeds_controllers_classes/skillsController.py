from gracie_feeds_api import GracieBaseAPI


class skillsController(GracieBaseAPI):
    """Skill"""

    _controller_name = "skillsController"

    def list(self, skillsetId):
        """Return list of skills.

        Args:
            skillsetId: (string): skillsetId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'skillsetId': {'name': 'skillsetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skill/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, skillId):
        """Retrieve existing skill.

        Args:
            skillId: (string): skillId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skill/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
