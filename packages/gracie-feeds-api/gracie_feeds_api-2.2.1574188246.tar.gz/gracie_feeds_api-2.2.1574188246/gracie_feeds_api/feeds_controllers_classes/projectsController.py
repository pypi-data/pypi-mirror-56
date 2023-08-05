from gracie_feeds_api import GracieBaseAPI


class projectsController(GracieBaseAPI):
    """Project is a set of inputs which search results are put in the same database index."""

    _controller_name = "projectsController"

    def add(self, projectName, **kwargs):
        """Create new projects for authenticated user.

        Args:
            isRunning: (boolean): isRunning
            projectName: (string): projectName
            textProcessingPipelineId: (string): If set empty string, the default pipeline will be used.
            ttl: (string): Time To Live.For documents in Elasticsearch.Allows you to specify the minimum time a document should live,after which time the document is deleted automatically.Empty string or null means unlimited time.Example: "1y", "3M", "3w", "1d".The supported time units are: y(year), M(month), w(week), d(day).

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'projectName': {'name': 'projectName', 'required': True, 'in': 'query'}, 'textProcessingPipelineId': {'name': 'textProcessingPipelineId', 'required': False, 'in': 'query'}, 'ttl': {'name': 'ttl', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/add'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def clone(self, newProjectName, projectId):
        """Duplicate project to new name.

        Args:
            newProjectName: (string): newProjectName
            projectId: (string): projectId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'newProjectName': {'name': 'newProjectName', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/clone'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def edit(self, projectId, **kwargs):
        """Edit existing projects by ID.

        Args:
            isRunning: (boolean): isRunning
            name: (string): name
            projectId: (string): projectId
            textProcessingPipelineId: (string): If set empty string, the default pipeline will be used.
            ttl: (string): ttl

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'textProcessingPipelineId': {'name': 'textProcessingPipelineId', 'required': False, 'in': 'query'}, 'ttl': {'name': 'ttl', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/edit'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def list(self):
        """Return the list of projects for authenticated user."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/projects/list'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def processFile(self, file, privacyMode, projectId, **kwargs):
        """Process the text from file. Supported file formats:  - https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            date: (integer): The number of seconds since January 1, 1970, 00:00:00 GMT.
            file: (file): file
            languageId: (string): empty - AutoDetect language from text.
            logging: (boolean): logging
            office365EmailType: (string): office365EmailType
            office365EmailsIncludeMode: (string): office365EmailsIncludeMode
            office365Groups: (array): office365Groups
            office365MailFolder: (string): office365MailFolder
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/processFile'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def processReview(self, privacyMode, productId, productName, projectId, reviewTypeId, **kwargs):
        """Process the review.

        Args:
            author: (string): Person who created the review.
            businessCategories: (array): Business categories.
            businessCoordinatesLatitude: (number): Business coordinates latitude.
            businessCoordinatesLongitude: (number): Business coordinates longitude.
            businessId: (string): Business id.
            businessLocationAddress1: (string): Business location address1.
            businessLocationAddress2: (string): Business location address2.
            businessLocationAddress3: (string): Business location address3.
            businessLocationCity: (string): Business location city.
            businessLocationCountry: (string): Business location country.
            businessLocationState: (string): Business location state.
            businessLocationZipCode: (string): Business location ZIP code.
            businessName: (string): Business name.
            businessPhone: (string): Business phone.
            businessPrice: (integer): Business price.
            businessRating: (number): Business rating.
            businessTransactions: (array): Business transactions.
            businessUrl: (string): Business url.
            checkinCount: (integer): Check-in count.
            coolCount: (integer): Cool count.
            date: (integer): Date the review was posted. The number of seconds since January 1, 1970, 00:00:00 GMT.
            funnyCount: (integer): Funny count.
            helpfulCount: (integer): The number of people that indicated this review was helpful.
            languageId: (string): empty - AutoDetect.
            logging: (boolean): logging
            notHelpfulCount: (integer): The number of people that indicated this review was not helpful.
            options: (array): List of possible options.
            privacyMode: (boolean): In this mode the processed text not saved.
            productId: (string): The product id of the item being reviews.
            productName: (string): The product name.
            projectId: (string): API id of project.
            rating: (number): The review star rating.
            recommended: (boolean): Recommended.
            review: (string): Text of the review.
            reviewTypeId: (string): Amazon, Home depot, Walmart, etc...
            reviewVotesCount: (integer): Review votes count.
            url: (string): Review url.
            verifiedUser: (boolean): Verified user.

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'author': {'name': 'author', 'required': False, 'in': 'query'}, 'businessCategories': {'name': 'businessCategories', 'required': False, 'in': 'query'}, 'businessCoordinatesLatitude': {'name': 'businessCoordinatesLatitude', 'required': False, 'in': 'query'}, 'businessCoordinatesLongitude': {'name': 'businessCoordinatesLongitude', 'required': False, 'in': 'query'}, 'businessId': {'name': 'businessId', 'required': False, 'in': 'query'}, 'businessLocationAddress1': {'name': 'businessLocationAddress1', 'required': False, 'in': 'query'}, 'businessLocationAddress2': {'name': 'businessLocationAddress2', 'required': False, 'in': 'query'}, 'businessLocationAddress3': {'name': 'businessLocationAddress3', 'required': False, 'in': 'query'}, 'businessLocationCity': {'name': 'businessLocationCity', 'required': False, 'in': 'query'}, 'businessLocationCountry': {'name': 'businessLocationCountry', 'required': False, 'in': 'query'}, 'businessLocationState': {'name': 'businessLocationState', 'required': False, 'in': 'query'}, 'businessLocationZipCode': {'name': 'businessLocationZipCode', 'required': False, 'in': 'query'}, 'businessName': {'name': 'businessName', 'required': False, 'in': 'query'}, 'businessPhone': {'name': 'businessPhone', 'required': False, 'in': 'query'}, 'businessPrice': {'name': 'businessPrice', 'required': False, 'in': 'query'}, 'businessRating': {'name': 'businessRating', 'required': False, 'in': 'query'}, 'businessTransactions': {'name': 'businessTransactions', 'required': False, 'in': 'query'}, 'businessUrl': {'name': 'businessUrl', 'required': False, 'in': 'query'}, 'checkinCount': {'name': 'checkinCount', 'required': False, 'in': 'query'}, 'coolCount': {'name': 'coolCount', 'required': False, 'in': 'query'}, 'date': {'name': 'date', 'required': False, 'in': 'query'}, 'funnyCount': {'name': 'funnyCount', 'required': False, 'in': 'query'}, 'helpfulCount': {'name': 'helpfulCount', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'notHelpfulCount': {'name': 'notHelpfulCount', 'required': False, 'in': 'query'}, 'options': {'name': 'options', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'query'}, 'productId': {'name': 'productId', 'required': True, 'in': 'query'}, 'productName': {'name': 'productName', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'rating': {'name': 'rating', 'required': False, 'in': 'query'}, 'recommended': {'name': 'recommended', 'required': False, 'in': 'query'}, 'review': {'name': 'review', 'required': False, 'in': 'query'}, 'reviewTypeId': {'name': 'reviewTypeId', 'required': True, 'in': 'query'}, 'reviewVotesCount': {'name': 'reviewVotesCount', 'required': False, 'in': 'query'}, 'url': {'name': 'url', 'required': False, 'in': 'query'}, 'verifiedUser': {'name': 'verifiedUser', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/processReview'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def processText(self, privacyMode, projectId, text, **kwargs):
        """Process the text.

        Args:
            date: (integer): The number of seconds since January 1, 1970, 00:00:00 GMT.
            fileExt: (string): fileExt
            fileName: (string): fileName
            filterFields: (string): filterFields
            languageId: (string): empty - AutoDetect.
            logging: (boolean): logging
            mimeType: (string): mimeType
            office365EmailType: (string): office365EmailType
            office365EmailsIncludeMode: (string): office365EmailsIncludeMode
            office365Groups: (array): office365Groups
            office365MailFolder: (string): office365MailFolder
            privacyMode: (boolean): In this mode the processed text not saved.
            projectId: (string): projectId
            text: (type): text

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'date': {'name': 'date', 'required': False, 'in': 'query'}, 'fileExt': {'name': 'fileExt', 'required': False, 'in': 'query'}, 'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}}
        parameters_names_map = {}
        api = '/projects/processText'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def remove(self, projectId):
        """Remove existing projects for authenticated user.

        Args:
            projectId: (string): projectId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/remove'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def retrieve(self, projectId):
        """Return the project with specified ID.

        Args:
            projectId: (string): projectId

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/retrieve'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)

    def status(self, id, isRunning):
        """Set existing projects status.

        Args:
            id: (string): id
            isRunning: (boolean): isRunning

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/status'
        actions = ['post']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data)
