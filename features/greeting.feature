Feature: Test the greeting lambda

    Scenario: A greeting file is uploaded to s3
        Given the greeting file does not already exist
        When the greeting lambda is invoked
        Then the greeting file is created in the test bucket
        And its contents are correct