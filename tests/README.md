# Tests for Speech Coach Project

This directory contains tests for the Speech Coach project. The test structure reflects the source code structure.

## Structure

```
tests/
├── conftest.py  - common fixtures for tests
└── src/
    └── shared/  - tests for shared components
        ├── services/  - tests for services
        ├── schemas/   - tests for data schemas
        └── messaging/ - tests for messaging components
```

## Running Tests

To run all tests:

```bash
python -m pytest
```

To run tests with code coverage:

```bash
python -m pytest --cov=src
```

To run specific tests:

```bash
python -m pytest tests/src/shared/services/test_audio_service.py
```

## Fixtures

Common fixtures for tests are defined in the `conftest.py` file:

- `event_loop` - fixture for enabling asynchronous tests
- `mock_config` - mock for configuration
- `mock_broker` - mock for message broker
- `temp_file` - fixture for creating a temporary file
- `temp_ogg_file` - fixture for creating a temporary audio file
- `mock_s3_client` - mock for S3 client (MinIO)

## Adding New Tests

When adding new tests, follow these principles:

1. Create tests in the appropriate directories reflecting the project structure
2. Use the `test_` prefix for test files and functions
3. Use fixtures from `conftest.py` for common operations
4. For asynchronous tests, use the `@pytest.mark.asyncio` decorator

## Code Coverage

Aim for test code coverage of at least 80%. Focus mainly on business logic and error handling.
