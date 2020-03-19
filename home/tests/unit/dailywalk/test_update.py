from django.test import Client, TestCase


class ApiTestCase(TestCase):
    def setUp(self):
        # Test client
        self.client = Client()
        # Create a user
        response = self.client.post(
            path="/api/appuser/create",
            data={
                "name": "Abhay Kashyap",
                "email": "abhay@blah.com",
                "zip": "72185",
                "age": 99,
                "account_id": "12345",
            },
            content_type="application/json",
        )

        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "success", msg=fail_message)
        self.assertEqual(response_data["message"], "App User registered successfully", msg=fail_message)

        # Details for Daily walk even creation
        self.url = "/api/dailywalk/create"
        # Request parameters
        self.request_params = {"account_id": "12345", "event_id": "8888", "date": "2020-02-22", "steps": 500}
        # Content type
        self.content_type = "application/json"

        # Create a daily walk
        # Send the request
        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "success", msg=fail_message)
        self.assertEqual(response_data["message"], "Dailywalk recorded successfully", msg=fail_message)

    # Test creation of a daily walk for the same date twice with an update param
    def test_update_dailywalk_success(self):

        # Send the second request but ensure its an update
        self.request_params["steps"] = 1000
        self.request_params["update"] = True

        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "success", msg=fail_message)
        self.assertEqual(
            response_data["message"], f"Steps updated successfully for {self.request_params['date']}", msg=fail_message
        )

    # Test creation of a daily walk for the same date twice without an update param
    def test_update_dailywalk_failure(self):

        # Send the second request but ensure its an update
        self.request_params["steps"] = 1000

        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "error", msg=fail_message)
        self.assertEqual(
            response_data["message"],
            f"Steps already logged for {self.request_params['date']}. To update, please send 'update': True in input params",
            msg=fail_message,
        )