import os
import random
from datetime import datetime
from utils.request import send_api_request

# Create test_reports folder if it doesn't exist
if not os.path.exists("test_reports"):
    os.makedirs("test_reports")


class BasicFunctionalityTests:
    @staticmethod
    def test_get_version(station_id, file):
        """
        Test command "getVersion": Ensures the API returns a valid version string.
        """
        output = f"Request should return valid version of station {station_id}\n"
        print(output, end='')
        file.write(output)
        try:
            response = send_api_request(station_id, "getVersion")
            assert response["status"] == 200, f"status code: {response['status']} - Incorrect status code"
            assert response["result"] is not None, "Response is None"
            result = response["result"]
            assert isinstance(result["result"], str), "Result is not a string"
            output = "PASSED -- Test for 'getVersion' passed successfully\n\n"
            print(output, end='')
            file.write(output)
        except AssertionError as e:
            output = f"FAILED -- Assertion error: {e}\n\n"
            print(output, end='')
            file.write(output)

    @staticmethod
    def test_get_interval(station_id, file):
        """
        Test command "getInterval": Ensures the API returns a valid interval integer.
        """
        output = f"Request should return valid interval of station {station_id}\n"
        print(output, end='')
        file.write(output)
        try:
            response = send_api_request(station_id, "getInterval")
            assert response["status"] == 200, f"status code: {response['status']} - Incorrect status code"
            assert response["result"] is not None, "Response is None"
            result = response["result"]
            assert isinstance(result["result"], int), "Result is not an integer"
            output = "PASSED -- Test for 'getInterval' passed successfully\n\n"
            print(output, end='')
            file.write(output)
        except AssertionError as e:
            output = f"FAILED -- Assertion error: {e}\n\n"
            print(output, end='')
            file.write(output)

    @staticmethod
    def test_set_values(station_id, payload, file):
        """
        Test command "setValues": Ensures the API returns a valid status after setting values.
        """
        output = f"Request should return valid status on the set operation of {station_id}\n"
        print(output, end='')
        file.write(output)
        try:
            response = send_api_request(station_id, "setValues", payload)
            assert response["status"] == 200, f"status code: {response['status']} - Incorrect status code"
            assert response["result"] is not None, "Response is None"
            result = response["result"]
            assert result["result"] in ["OK", "FAILED"], "Unexpected result"
            output = "PASSED -- Test for 'setValues' passed successfully\n\n"
            print(output, end='')
            file.write(output)
        except AssertionError as e:
            output = f"FAILED -- Assertion error: {e}\n\n"
            print(output, end='')
            file.write(output)


class ErrorHandlingTests:
    @staticmethod
    def test_invalid_command(station_id, file):
        """
        Test for handling invalid command: Ensures the API returns an error for an invalid command.
        """
        output = f"Request with invalid command to station {station_id}\n"
        print(output, end='')
        file.write(output)
        try:
            response = send_api_request(station_id, "invalidCommand")
            assert response["status"] == 400, f"status code: {response['status']} - Incorrect status code"
            assert response["result"] is None, "Response is NOT None"
            output = "PASSED -- Test for handling invalid command passed successfully\n\n"
            print(output, end='')
            file.write(output)
        except AssertionError as e:
            output = f"FAILED -- Assertion error: {e}\n\n"
            print(output, end='')
            file.write(output)

    @staticmethod
    def test_invalid_payload(station_id, file):
        """
        Test for handling invalid payload for setValues: Ensures the API returns an error for an invalid payload.
        """
        output = f"Request with invalid payload for setValues to station {station_id}\n"
        print(output, end='')
        file.write(output)
        try:
            response = send_api_request(station_id, "setValues", "invalidPayload")
            assert response["status"] == 400, f"status code: {response['status']} - Incorrect status code"
            assert response["result"] is None, "Response is NOT None"
            output = "PASSED -- Test for handling invalid payload for setValues passed successfully\n\n"
            print(output, end='')
            file.write(output)
        except AssertionError as e:
            output = f"FAILED -- Assertion error: {e}\n\n"
            print(output, end='')
            file.write(output)


class TestPostRequestCommands:
    station_ids = {1, 2, 3, 4, 5}
    payload = random.randrange(0, 100)

    # Get current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a file name with the specified format
    file_path = os.path.join("test_reports", f"automation_test_{current_time}.txt")

    # Open file in write mode
    with open(file_path, "w") as file:
        for sid in station_ids:
            output = f"--------------------------------------------------\n"
            print(output, end='')
            file.write(output)
            output = f"Test POST request with commands to station {sid}\n"
            print(output, end='')
            file.write(output)
            output = f"--------------------------------------------------\n\n"
            print(output, end='')
            file.write(output)

            BasicFunctionalityTests.test_get_version(sid, file)
            BasicFunctionalityTests.test_get_interval(sid, file)
            BasicFunctionalityTests.test_set_values(sid, payload, file)

            ErrorHandlingTests.test_invalid_command(sid, file)
            ErrorHandlingTests.test_invalid_payload(sid, file)
