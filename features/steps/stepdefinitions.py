import json
import tempfile
from behave import given, when, then


@given("the greeting file does not already exist")
def delete_greeting_file(context):
    context.s3.delete_object(Bucket="testbucket", Key="test.txt")


@when("the greeting lambda is invoked")
def invoke_lambda(context):
    context.lambda_client.invoke(
        FunctionName="SayHello",
        InvocationType="RequestResponse",
        Payload=json.dumps({"recipient": "test"})
    )


@then("the greeting file is created in the test bucket")
def check_bucket(context):
    testbucket = context.s3.list_objects(Bucket="testbucket")
    key = next((key for key in testbucket["Contents"] if key["Key"] == "test.txt"), None)
    assert key is not None


@then("its contents are correct")
def verify_contents(context):
    with tempfile.TemporaryFile() as f:
        context.s3.download_fileobj("testbucket", "test.txt", f)
        f.seek(0)
        contents = f.read().decode("utf-8")
        print(contents)
        assert contents == "Hello, test!"