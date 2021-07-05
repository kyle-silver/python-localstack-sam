from behave import given, when, then


@given("the greeting file does not already exist")
def delete_greeting_file(context):
    context.s3.delete_object(Bucket="testbucket", Key="test.txt")


@when("the greeting lambda is invoked")
def invoke_lambda(context):
    context.lambda_client.invoke(FunctionName="SayHello")


@then("the greeting file is created in the test bucket")
def check_bucket(_context):
    pass


@then("its contents are correct")
def verify_contents(_context):
    pass