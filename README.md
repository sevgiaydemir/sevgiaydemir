# TECHNICAL PORTFOLIO: AUTOMATION INFRASTRUCTURE

**Name:** Sevgi AYDEMIR  
**Title:** Software Engineer (SDET)  
**Subtitle:** Mobile Automation, API Validation & System Reliability  
**Contact:** Brooklyn, NY | sevgiaydemir.dev@gmail.com

---
### Overview

This portfolio highlights selected examples of automation infrastructure, mobile testing, API validation, and system reliability work that I designed and maintained.

To protect proprietary information, project-specific names and implementation details have been generalized while preserving the underlying technical concepts and architecture.

## Project 1: Mobile Automation Framework (Python / Pytest-BDD / Appium)

I designed and maintained a mobile automation framework used to validate end-to-end workflows across Android applications, backend services, and connected devices.

### The framework focuses on:
 - Multi-device test execution
 - Fault recovery and crash handling
 - Scalable automation architecture
 - Connectivity and synchronization validation
 - End-to-end system reliability

### Parallel Execution & Assertion Handling
One challenge with multi-device automation is ensuring failures occurring inside worker threads correctly fail the overall test run.

To address this, I implemented a custom execution layer that runs validations in parallel while collecting and propagating failures back to the primary execution thread.

```
@staticmethod
def driver_runner_raise_assertion(function: callable, drivers: list, function_name: str, *args, **kwargs) -> None:

   exceptions = []

   def run_and_catch(driver):
       try:
           function(driver, *args, **kwargs)
       except Exception as e:
           exceptions.append(e)

   threads = [
       threading.Thread(target=run_and_catch, args=(driver,))
       for driver in drivers
   ]

   for thread in threads:
       thread.start()
   for thread in threads:
       thread.join()

   if exceptions:
       # raise the first one for test failure
       raise exceptions[0]
```
### Smart Waiting & Recovery Mechanism
To improve execution stability and reduce unnecessary wait times, I built a custom polling mechanism that continuously evaluates application state while detecting unexpected crashes.

When failures occur, the framework automatically performs recovery actions and restores the test environment.

```
@staticmethod
def incremental_wait(driver, locator, element_name='not_defined', time_to_wait=10, increment=0.5):

   time_since_start = 0
   while time_since_start <= time_to_wait:
       time_since_start += increment

       try:
           if Helpers.is_element_present(driver, locator, element_name, 0.1):
               return

       except NoSuchElementException:
          sleep(increment)

       except TimeoutException:
           logging.error(f"TimeoutException occurred while waiting for element {element_name}")
           udid = driver.capabilities['udid']

           if Helpers.is_app_crashed(udid):
               logging.info(f"App on device {udid} crashed. Restarting the app...")
               Helpers.relaunch_app(driver)
               Helpers.open_plugin(driver)
               logging.info(f"App on device {udid} was crashed and has been restarted. Returning False.")
               return False

           logging.info("App did not crash, but Timeout occurred. Returning False.")
           return False

   raise TimeoutError(f"Element {locator} not found after {time_to_wait} seconds")
   ```
### Additional Framework Capabilities

#### The framework also includes:

 - Dynamic multi-device session management
 - Application crash detection and recovery
 - Connectivity simulation using ADB
 - Version-aware test execution
 - Map and location validation utilities
 - Secure communication and synchronization testing
 - Parallel execution across multiple devices

### Example BDD Scenario
The framework uses Pytest-BDD to validate end-to-end synchronization and secure communication workflows.

```
Scenario: Verify removed users cannot receive group messages

Given I create a group with multiple users
When I remove UserC from the group
And UserA sends a message
Then UserC should not receive the message
And UserB should successfully receive it
```

## Project 2: Backend API Validation Framework (JS / Mocha / Chai / Supertest)
I contributed to a backend validation framework responsible for testing authentication, authorization, device management, synchronization workflows, and API reliability.

### The framework focuses on:

 - API contract validation
 - Authentication and authorization
 - Schema verification
 - Data integrity testing
 - Negative and boundary testing

### Authentication & Request Management
I created reusable request handlers that centralize authentication and request configuration, reducing duplication and simplifying maintenance.

```
class RequestManager {
   constructor() {
      this.baseHeaders = {
         "Content-Type": "application/json",
         "Accept": "application/json"
      };
   }
   getHeaders(accessToken = "") {
      return {
         ...this.baseHeaders,
         Authorization: `Bearer ${accessToken}`
      };
   }
}
```

### API Contract Validation
The framework validates positive, negative, and boundary scenarios to ensure API routing, response contracts, and business rules behave as expected.

```
it("GET firmware download URL", async () => {
   const response = await request(BASE_URL)
      .get("/api/v3/firmware/64/nxp/download-url")
      .set(headers);

   expect(response.status).to.equal(200);
   expect(response.body).to.have.property("url");
});
```

### Dynamic Payload Generation
To increase coverage and reduce manual test maintenance, I built reusable payload generators that create realistic device and health-check data sets.

```
async createDeviceHealthCheckPayload(data) {

   return [{
      id: random.intNumber(1,1000).toString(),
      firmware_version: random.generateSemanticString(),
      battery_level: random.intNumber(0,100),
      temperature: random.intNumber(-100,500)
   }]; 
}
```

### Negative Validation Testing
The framework automatically generates invalid payload combinations to verify backend validation rules and error handling behavior.

#### Examples include:

 - String values in numeric fields
 - Boolean values in numeric fields
 - Object and array injection
 - Invalid schema combinations
 - Boundary value violations

This approach helped identify backend validation defects and inconsistencies in API contracts before production deployment.

### Technologies Used

- Python
- JavaScript
- Pytest-BDD
- Appium
- Mocha
- Chai
- Supertest
- Android Debug Bridge (ADB)


