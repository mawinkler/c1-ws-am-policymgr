import requests
from errors import (
    CloudOneError,
    CloudOneHttp400Error,
    CloudOneHttp500Error,
    CloudOneHttpError,
    RequestConnectionError,
)


class CloudOneConnector:
    """CloudOneConnector - handles the connection to Cloud One"""

    def __init__(self):
        # API credentials are mounted to /etc
        self.c1_url = open("/etc/cloudone-credentials/c1_url", "r").read().rstrip("\n")
        self.api_key = (
            open("/etc/cloudone-credentials/api_key", "r").read().rstrip("\n")
        )

    def get(self, endpoint, variable: str, **data):
        """Send an HTTP GET request to Cloud One and check response for errors.

        Args:
            component (Component): Calling component
            variable (str): Attribute to get from server.

        """
        url = self._url(endpoint, variable=variable)
        return self._get(url, **data)

    def _get(self, url, **data):
        """Send an HTTP GET request to Cloud One and check response for errors.

        Args:
            component (Component): Calling component
            variable (str): Attribute to get from server.

        """
        data.update(self._base_data_for_request())
        try:
            response = requests.get(
                url, headers=self._header_data_for_request(), params=data
            )
            self.__check_error(response)
        except IOError as exc:
            _LOGGER.error(f"Connection to {url} failed")
            raise exc

        return response.json()  # ["Value"]

    def post(self, endpoint, variable: str, **data):
        """Send an HTTP POST request to Cloud One and check response for errors.

        Args:
            component (Component): Calling component
            variable (str): Attribute to set on server.
            **data: Data to send with request.

        """
        url = self._url(endpoint, variable=variable)
        return self._post(url, **data)

    def _post(self, url, **data):
        """Send an HTTP POST request to Cloud One and check response for errors.

        Args:
            component (Component): Calling component
            variable (str): Attribute to set on server.
            **data: Data to send with request.

        """
        data = data["data"]
        response = requests.post(
            url, headers=self._header_data_for_request(), json=data
        )
        self.__check_error(response)
        return response.json()

    def delete(self, endpoint, variable: str, **data):
        """Send an HTTP DELETE request to Cloud One and check response for errors.

        Args:
            component (Component): Calling component
            variable (str): Attribute to get from server.

        """
        url = self._url(endpoint, variable=variable)
        return self._delete(url, **data)

    def _delete(self, url, **data):
        """Send an HTTP DELETE request to Cloud One and check response for errors.

        Args:
            component (Component): Calling component
            variable (str): Attribute to get from server.

        """
        data.update(self._base_data_for_request())
        try:
            response = requests.delete(
                url, headers=self._header_data_for_request(), params=data
            )
            self.__check_error(response)
        except IOError as exc:
            _LOGGER.error(f"Connection to {url} failed")
            raise exc

        return response.json()  # ["Value"]

    def _header_data_for_request(self):
        """Add header data for requets."""
        return {
            "Content-type": "application/json",
            "Authorization": f"ApiKey {self.api_key}",
            "api-version": "v1",
        }

    def _base_data_for_request(self):
        """Add additional data for requets."""
        return {}

    # @staticmethod
    def _url(self, endpoint, variable: str):
        """Composes the URL for the given API endpoint of Workload Security.

        Args:
            component (Component): Calling endpoint
            variable (str): Additional attribute, typically an ID.

        """
        url = "https://workload." + "/".join([self.c1_url, "api", endpoint, variable])
        # variable,
        return url

    @staticmethod
    def __check_error(response: requests.Response):
        """Check response from Rest server for Errors.

        Args:
            response (Response): Response from Rest server to check.

        """
        if response.status_code == 400:
            _LOGGER.error(f"HTTP 400 error, ({response.text}) for {response.url}")
            raise CloudOneHttp400Error(response.text)
        elif response.status_code == 500:
            _LOGGER.error(f"HTTP 500 error, ({response.text}) for {response.url}")
            raise CloudOneHttp500Error(response.text)
        # j = response.json()
        # pp(j)
        # if j["ErrorNumber"] != 0:
        #     _LOGGER.error(f'Error, code={j["ErrorNumber"]}, msg={j["ErrorMessage"]}')
        #     raise CloudOneError(j["ErrorNumber"], j["ErrorMessage"])
