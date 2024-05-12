# This is a sample Python script.
import os
from datetime import datetime
from tests.automation_tests import TestPostRequestCommands
from tests.exploratory_tests import TestPayload
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():

    # Determine the directory for test reports
    report_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests", "test_reports")
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    # Run the exploratory tests and write results to a file
    exploratory_test_results_file = os.path.join(report_directory, f"exploratory_test_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    with open(exploratory_test_results_file, 'w') as f:
        test_payload = TestPayload()
        test_payload.run_tests(f)


"""    automated = TestPostRequestCommands()
    automated.run_tests()

    expl = TestPayload()
    expl.run_tests()"""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
