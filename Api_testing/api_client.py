from datetime import datetime, date
from typing import Optional, Union

import allure
from assertpy import assertpy
from pydantic import json
from requests import Session
from requests.auth import HTTPBasicAuth

from GD_QA_Portfolio2025.Api_testing.response_models import ApiError, CatBreedsResponse


class ApiClient(Session):
    def __init__(self, base_url: str, token: Optional[str] = None):
        super(ApiClient, self).__init__()  # python extended clasess
        self.base_url = base_url
        self.token = token
        self.headers = {}

    def find_cats_data(self, json_data, status_code: int = 200, method: str = 'GET') -> Union[CatBreedsResponse, ApiError]:
        response = self.execute_request('/breeds?limit=5', method, json_data, status_code)
        return self.get_response_body(response, CatBreedsResponse)

    def execute_request(
            self,
            path: str,
            method: str,
            json_data: Optional[dict] = None,
            status_code: int = 200,
            login: str = 'user',
            password: str = 'pass'

    ):
        url = f"{self.base_url}{path}"
        # add token sending via header when it will be in the system
        response = self.request(
            url=url,
            method=method,
            auth=HTTPBasicAuth(login, password),
            headers=self.headers
        )
        data = response.json()
        print(response.request.url)
        print(response.request.method)
        print(response.request.headers)
        print(data)
        assertpy.assert_that(response.status_code).is_equal_to(status_code)
        allure.attach(f"Response passed validation: {data}", name="Response",
                      attachment_type=allure.attachment_type.JSON)
        return response

    def get_response_body(self, response, model):
        response_data = response.json()
        if response.status_code < 400:
            return model(**response_data)
        return ApiError(**response_data)


