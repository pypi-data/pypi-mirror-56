from gracie_feeds_api import GracieBaseAPI


class logoutController(GracieBaseAPI):
    """Logout."""

    _controller_name = "logoutController"

    def logout(self):
        """logout"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/logout'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
