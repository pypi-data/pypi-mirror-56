# Integration test

This test suite performs an end to end test case defined as:



- Setup test requirements:
  - Provision an instance of **PreVeil Collection Server**
  - Provision an instance of **PreVeil Crypto Server** (client daemon)
  - Provision an instance of **Load Generator** tool
  - Provision an instance of **Relay** tool
- Setup organizational prerequisites:
  - Create a user
  - Create an organization for user
  - Create an export group for the organization
- Relay tool configuration
  - Migrate/setup relay's database
  - Configure the tool to point to volume-based  configuration file
  - Configure exporter account
  - Configure approver accounts
  - Start the relay process
- Generate load on the organization:
  - Generate email load with an adjustable frequency
    - TODO: randomize email protocol versions, contents, validity, ...
  - Add members to organization with an adjustable frequency
  - TODO: change export group with an an adjustable
- At last stop the load generator, and **expect a successful relay** to volume:
  -  Fetch all the server messages of all the members of the organization, including the deleted ones.
  - Expect to see them all stored in the volume.





## Running the test suite
To run the test you can do `python -m tests.integration_test`. This will perform the scneraio described above in an isolated context identified with an id. Test takes about 2 minutes by default. You can adjust load generator's frequencies by specifying coresponding environment variables.

You can continue a stoped test by `python -m tests.integration_test -i ${test-id}`.

To see full usage, do `python -m tests.integration_test --help`.





















