from gracie_feeds_api import GracieBaseAPI


class textProcessingPipelineController(GracieBaseAPI):
    """Text Processing Pipeline Controller"""

    _controller_name = "textProcessingPipelineController"

    def add(self, name, pipeline, **kwargs):
        """Create new text processing pipeline for authenticated user.

        Args:
            description: (string): description
            name: (string): name
            pipeline: (string): pipeline

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'pipeline': {'name': 'pipeline', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/textProcessingPipeline/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def default(self):
        """Returns default text processing pipeline."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/textProcessingPipeline/default'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def edit(self, name, pipeline, textProcessingPipelineId, **kwargs):
        """Edit existing text processing pipeline by ID.

        Args:
            description: (string): description
            name: (string): name
            pipeline: (string): pipeline
            textProcessingPipelineId: (string): textProcessingPipelineId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'pipeline': {'name': 'pipeline', 'required': True, 'in': 'query'}, 'textProcessingPipelineId': {'name': 'textProcessingPipelineId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/textProcessingPipeline/edit'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self, **kwargs):
        """Return the list of text processing pipeline for authenticated user.

        Args:
            withPipeline: (boolean): withPipeline

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'withPipeline': {'name': 'withPipeline', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/textProcessingPipeline/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def remove(self, textProcessingPipelineId):
        """Remove existing text processing pipeline for authenticated user.

        Args:
            textProcessingPipelineId: (string): textProcessingPipelineId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'textProcessingPipelineId': {'name': 'textProcessingPipelineId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/textProcessingPipeline/remove'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, textProcessingPipelineId):
        """Return the text processing pipeline with specified ID.

        Args:
            textProcessingPipelineId: (string): textProcessingPipelineId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'textProcessingPipelineId': {'name': 'textProcessingPipelineId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/textProcessingPipeline/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
