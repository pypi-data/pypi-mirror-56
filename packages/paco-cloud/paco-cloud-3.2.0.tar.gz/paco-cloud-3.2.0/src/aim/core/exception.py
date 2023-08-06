from enum import Enum

AimErrorCode = Enum(
    'AimErrorCode',
    '\
Unknown TemplateValidationError InvalidNumberOfArguments StackInProgress \
BadConfigFiles StackDoesNotExist StackOutputMissing InvalidStackName \
WaiterError')

class AimException(Exception):
    def __init__(self, code, message=None):
        super().__init__()
        self.code = code
        if message != None:
            self.message = message
        else:
            self.set_message(code)

    def set_message(self, code):
        if code == AimErrorCode.Unknown:
            self.message = "Unknown error"
        elif code == AimErrorCode.TemplateValidationError:
            self.message = "A CloudFormation template failed to validate"
        elif code == AimErrorCode.InvalidNumberOfArguments:
            self.message = "Invalid number of arguments"
        elif code == AimErrorCode.StackInProgress:
            self.message = "The stack is already in progress"
        elif code == AimErrorCode.BadConfigFiles:
            self.message = "Config files can not be understood."
        elif code == AimErrorCode.StackDoesNotExist:
            self.message = "Stack does not exist."


class StackException(AimException):
    def __init__(self, code, message=None):
        super().__init__(code, message)

    def get_error_str(self):
        error_str =  "StackException: " + self.code.name + ": " + self.message
        return error_str

class AimBucketExists(Exception):
    "S3 Bucket already exists"

class UnsupportedCloudFormationParameterType(Exception):
    "Unsupported Parameter Type"

class CloudFormationParameterAimRefMissingDotExtension(Exception):
    "Parameters with aim.ref values need to match <Name>.<OutputName> format."

class InvalidLogSetConfiguration(Exception):
    "Invalid Log Set configuration"

class AimUnsupportedFeature(Exception):
    "Feature does not yet exist"

class InvalidAIMScope(Exception):
    "AIM Reference not valid in this context."
