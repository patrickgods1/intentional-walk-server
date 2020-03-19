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

    # Test a successful creation of a daily walk
    def test_create_dailywalk(self):

        # Send the request
        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "success", msg=fail_message)
        self.assertEqual(response_data["message"], "Dailywalk recorded successfully", msg=fail_message)
        self.assertEqual(response_data["payload"]["account_id"], self.request_params["account_id"], msg=fail_message)
        self.assertEqual(response_data["payload"]["event_id"], self.request_params["event_id"], msg=fail_message)
        self.assertEqual(response_data["payload"]["date"], self.request_params["date"], msg=fail_message)
        self.assertEqual(response_data["payload"]["steps"], self.request_params["steps"], msg=fail_message)

    # Test creation of a daily walk with an invalid user account
    def test_create_dailywalk_invalidaccount(self):

        self.request_params["account_id"] = "0000000"

        # Send the request
        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "error", msg=fail_message)
        self.assertEqual(
            response_data["message"],
            f'User does not exist for account - {self.request_params["account_id"]}. Please register first!',
            msg=fail_message,
        )

    # Test creation of a daily walk with a missing field
    def test_create_dailywalk_missing_eventid(self):

        del self.request_params["event_id"]

        # Send the request
        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "error", msg=fail_message)
        self.assertEqual(
            response_data["message"], "Required input 'event_id' missing in the request", msg=fail_message,
        )

    # Test creation of a daily walk with a missing field
    def test_create_dailywalk_missing_steps(self):

        del self.request_params["steps"]

        # Send the request
        response = self.client.post(path=self.url, data=self.request_params, content_type=self.content_type)
        # Check for a successful response by the server
        self.assertEqual(response.status_code, 200)
        # Parse the response
        response_data = response.json()
        fail_message = f"Server response - {response_data}"
        self.assertEqual(response_data["status"], "error", msg=fail_message)
        self.assertEqual(
            response_data["message"], "Required input 'steps' missing in the request", msg=fail_message,
        )