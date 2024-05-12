import os
import random
from datetime import datetime
from utils.request import send_api_request
from resources.test_data import invalid_payload, valid_payload


# a superclass represents a test suite for basic api endpoint, command testing
class TestAPIEndpoints:
    station_ids = {1, 2, 3, 4, 5}

    def __init__(self):
        self.test_cases = [
            self.test_station_id_integers_outside_1to5,
            self.test_valid_station_ids_get_version,
            self.test_valid_station_ids_get_interval
        ]

    # run_tests method runs all exploratory test cases
    def run_tests(self, output_file):
        output_file.write(f"Test run date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        output_file.write("Running API endpoint tests:\n")
        for test_case in self.test_cases:
            test_case(output_file)

    # test station id which is integer and not from 1 to 5
    def test_station_id_integers_outside_1to5(self, f):
        print("Testing station IDs that are integers not belonging to 1 to 5...")
        print("Request should return status code 200 and empty result")
        random_id = random.choice([num for num in range(0, 100) if num not in self.station_ids])
        self.make_api_request_and_assert(random_id, "getVersion", empty_response=True, output_file=f)

    # test command "getVersion" for station id from 1 to 5
    def test_valid_station_ids_get_version(self, f):
        print("Testing valid station IDs (1 to 5) using getVersion command...")
        print("Request should return status code 200 and valid version")
        for sid in self.station_ids:
            self.make_api_request_and_assert(sid, "getVersion", expected_type=str, output_file=f)

    # test command "getInterval" for station id from 1 to 5
    def test_valid_station_ids_get_interval(self, f):
        print("Testing valid station IDs (1 to 5) using getInterval command...")
        print("Request should return status code 200 and valid interval")
        for sid in self.station_ids:
            self.make_api_request_and_assert(sid, "getInterval", expected_type=int, output_file=f)

    # helper method helping define parameters of a request, writing test log
    def make_api_request_and_assert(self, sid, command, payload=None, expected_type=None, empty_response=False,
                                    output_file=None):
        response = send_api_request(sid, command)
        status_code = response.get("status")
        result = response.get("result", {})
        output_file.write(f"Station id: {sid}, command: {command}, payload: {payload}\n")
        output_file.write(f"Status code: {status_code}\n")
        output_file.write(f"Result: {result}\n")

        try:
            assert status_code == 200, f"status code: {status_code} - Incorrect status code"
            if empty_response:
                assert not result, "Response is not empty"
            elif expected_type:
                assert isinstance(result.get("result"), expected_type), f"Result is not a {expected_type}"
            output_file.write("PASS -- Correct status code and Response\n\n")
            print("PASS -- Correct status code and Response\n")
        except AssertionError as e:
            output_file.write(f"FAIL -- {e}\n\n")
            print(f"FAIL -- {e}\n")


# a subclass of TestAPIEndpoints represents a test suite for payload testing
class TestPayload(TestAPIEndpoints):
    def __init__(self):
        super().__init__()
        self.test_cases += [
            self.test_payload_not_integer,
            self.test_no_payload,
            self.test_valid_payloads_set_values,
            self.test_command_getVersion_with_payload,
            self.test_command_getInterval_with_payload
        ]

    # test invalid payload
    def test_payload_not_integer(self, f):
        print("Testing payloads that are NOT integers...")
        print("Request should NOT return result and status code 400 when payload is non-integer")
        for sid in self.station_ids:
            for key, value in invalid_payload.items():
                print(f"Station ID: {sid}, Payload: {key}")
                self.make_api_request_and_assert(sid, "setValues", value, expected_status=400, empty_response=True,
                                                 output_file=f)

    # test payload not exist
    def test_no_payload(self, f):
        print("Testing payloads that do NOT exist...")
        print("Request should NOT return result and status code 400 when payload does not exist")
        for sid in self.station_ids:
            self.make_api_request_and_assert(sid, "setValues", expected_status=400, empty_response=True, output_file=f)

    # test command setValues with valid payload
    def test_valid_payloads_set_values(self, f):
        print("Testing setting valid payloads for setValues command...")
        print("Request should return status code 200 and result as a string")
        for sid in self.station_ids:
            self.make_api_request_and_assert(sid, "setValues", valid_payload, expected_type=str, output_file=f)

    # test command getVersion with valid payload
    def test_command_getVersion_with_payload(self, f):
        print("Testing command getVersion with payloads...")
        print("Request should NOT return result and status code 400 when payload sent with command getVersion")
        for sid in self.station_ids:
            self.make_api_request_and_assert(sid, "getVersion", valid_payload, expected_status=400, empty_response=True,
                                             output_file=f)

    # test command getInterval with valid payload
    def test_command_getInterval_with_payload(self, f):
        print("Testing command getInterval with payloads...")
        print("Request should NOT return result and status code 400 when payload sent with command getInterval")
        for sid in self.station_ids:
            self.make_api_request_and_assert(sid, "getInterval", valid_payload, expected_status=400,
                                             empty_response=True, output_file=f)

    # customized make_api_request_and_assert from superclass
    def make_api_request_and_assert(self, sid, command, payload=None, expected_type=None, expected_status=200,
                                    empty_response=False, output_file=None):
        response = send_api_request(sid, command, payload)
        status_code = response.get("status")
        result = response.get("result", {})
        output_file.write(f"Station id: {sid}, command: {command}, payload: {payload}\n")
        output_file.write(f"Status code: {status_code}\n")
        output_file.write(f"Result: {result}\n")

        try:
            assert status_code == expected_status, f"status code: {status_code} - Incorrect status code"
            if empty_response:
                assert not result, "Response is not empty"
            elif expected_type:
                assert isinstance(result.get("result"), expected_type), f"Result is not a {expected_type}"
            output_file.write("PASS -- Correct status code and Response\n\n")
            print("PASS -- Correct status code and Response\n")
        except AssertionError as e:
            output_file.write(f"FAIL -- {e}\n\n")
            print(f"FAIL -- {e}\n")


# Create test_reports directory if it doesn't exist
if not os.path.exists("test_reports"):
    os.makedirs("test_reports")

# Run the tests and write results to a file
test_results_file = f"test_reports/exploratory_test_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
with open(test_results_file, 'w') as f:
    test_payload = TestPayload()
    test_payload.run_tests(f)
