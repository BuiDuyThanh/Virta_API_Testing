# VIRTA - API Testing
## Test Plan

### **Automation tests:**

**Basic Functionality Tests**
1. Test command "getVersion"
2. Test command "getInterval"
3. Test command "setValues" with payload

**Error Handling Tests**
1. Test invalid command
2. Test invalid payload


### **Exploratory tests**

**API Endpoints Tests**
1. Test station id not from 1 to 5
2. Test valid station ids with command "getVersion"
3. Test valid station ids with command "getInterval"

**Payload Tests**
1. Test payload not integer
2. Test payload not exist
3. Test valid payload with command "setValues"
4. Test valid payload with command "getVersion"
5. Test valid payload with command "getInterval"


_You **can** combine them_

## How To Run

Automation tests: 
run `tests/automation_tests.py`

Exploratory tests: 
run `tests/exploratory_tests.py`