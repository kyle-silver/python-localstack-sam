# Mimicking AWS with Localstack and SAM

When prototyping new projects that are intended to work with AWS services, it&rsquo;s useful to have an option for testing how the new project interacts with the AWS API without needing to provision actual AWS resources. These services can be costly if not deleted after testing is complete, and in a well-managed and highly-regulated environment, provisioning these resources in the first place may be too time-consuming for what is supposed to be a rapid prototype.

Localstack and AWS SAM help alleviate this burden by allowing us to mock AWS resources via Docker. This means all testing is contained locally and cleanup is as easy as shutting down a couple of docker containers.

There are a multitude of free offerings available for testing interactions with AWS, but these two in particular are useful because they offer near-seamless interoperability. This project contains a lambda which uploads a file to S3, and a simple acceptance test suite that verifies its behavior. Other than some environment-specific configuration (which is very minimal), the code that is executing is identical between our local machine and what will actually be deployed in AWS.

## Prerequisites

This demo requires [Docker](https://www.docker.com), [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html), [Localstack](https://localstack.cloud), and [Pipenv](https://pipenv.pypa.io/en/latest/).

```sh
brew install --cask docker
brew tap aws/tap
brew install aws-sam-cli
pip3 install --user pipenv
```

## Running the Demo

Our `SayHello` lambda takes an argument like the following `{"recipient": "John"}` and uploads a file to S3 whose contents are the phrase `Hello, John!`. This demo will walk you through setting up AWS SAM to host the lambda locally, setting up Localstack to mimic S3 locally via docker, and finally run an acceptance test to verify that the lambda works as intended.

First, make sure the Docker daemon is running. Next, navigate to the root of this project and run the following commands. This will activate a virtual environment to manage the python dependencies of the project and then start AWS SAM to host the lambda for local invocations

```console
$ pipenv shell
Launching subshell in virtual environment...
$ make start
```

In a new console window (also at the root of this directory), run the following to start localstack. This will spin up a docker container which will act as our local version of S3. Localstack is capable of mimicking a wide variety of AWS services, such as CloudWatch and SQS.

```console
$ docker compose up
[+] Running 1/1
 ⠿ Container python-localstack-sam_localstack_1  Started
localstack_1  | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initaws.d/buckets.sh
localstack_1  | make_bucket: testbucket
```

From the logs, you can see that an S3 bucket has been registered inside our docker container. The lambda running inside AWS SAM will upload files to this bucket when we run it.

Finally, in a third console window, run the acceptance tests with the following command. From the output, you will see that the test suite invokes the lambda via SAM and then verifies the contents of the file uploaded to S3 by downloading the file from Localstack.

```console
$ pipenv run behave
Feature: Test the greeting lambda # features/greeting.feature:1

  Scenario: A greeting file is uploaded to s3
    Given the greeting file does not already exist
    When the greeting lambda is invoked
    Then the greeting file is created in the test bucket
    And its contents are correct

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
4 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m4.302s
```

If you look back at the AWS SAM logs, you can see that the lambda has been invoked.

```txt
START RequestId: 45e3599a-857b-4c91-b514-a6d26888dffd Version: $LATEST
END RequestId: 45e3599a-857b-4c91-b514-a6d26888dffd
REPORT RequestId: 45e3599a-857b-4c91-b514-a6d26888dffd  Init Duration: 0.11 ms  Duration: 1394.96 ms    Billed Duration: 1400 ms        Memory Size: 128 MB     Max Memory Used: 128 MB
2021-07-05 12:59:31 127.0.0.1 - - [05/Jul/2021 12:59:31] "POST /2015-03-31/functions/SayHello/invocations HTTP/1.1" 200 -
```

Once you have run the test, you can use `Ctrl+C` to shut down SAM and Localstack.
