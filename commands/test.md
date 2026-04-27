Generate tests for: $ARGUMENTS

Process:
1. Read the target file/function
2. Identify the testing framework already used in the project (check package.json / existing test files)
3. Write tests covering:
   - Happy path (normal inputs)
   - Edge cases (empty, null, zero, max values)
   - Error cases (invalid input, network failure, etc.)
   - Boundary conditions

Rules:
- Match the existing test file style exactly
- Use mocks only for external dependencies (network, DB, filesystem)
- Each test has a clear, descriptive name
- No test should depend on another test's state
- Place tests in the correct directory for this project

Output: complete test file ready to run.
