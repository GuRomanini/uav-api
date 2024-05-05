import requests
from qilocal.utils import Mock
from os import environ as env


class TestMockServer:
    mock = Mock()
    mock.clear()
    url = f'http://{env["SERVER_LOCALHOST"]}:1080/'

    def test_expectation_from_json_file(self):
        self.mock.load_expectations("tests/expectations/test.json")
        response = requests.get(self.url + "test_path")
        assert response.status_code == 200

    def test_expectation_from_json_object(self):

        self.mock.generate_expectation(
            method="POST",
            endpoint="/test_path",
            response_json={"hello": "world"},
            status_code=200,
        )

        response = requests.post(self.url + "test_path")
        assert response.status_code == 200
