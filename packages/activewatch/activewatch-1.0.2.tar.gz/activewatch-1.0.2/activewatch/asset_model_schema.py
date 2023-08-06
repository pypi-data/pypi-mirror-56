# -*- coding: utf-8 -*-

AWS_RESOURCE_MAP = {
    "AWS::EC2::Instance": "host",
    "AWS::EC2::SecurityGroup": "sg",
    "AWS::EC2::Subnet": "subnet",
    "AWS::EC2::VPC": "vpc",
    "AWS::EC2::NetworkAcl": "acl",
    "AWS::EC2::RouteTable": "route",
    "AWS::EC2::InternetGateway": "igw",
    "AWS::S3::Bucket": "s3-bucket",
    "AWS::IAM::Role": "role",
    "AWS::KMS::Key": "kms-key"
}

def get_asset_key(deployment_type, native_resource_id, native_resource_type=None, native_account_id = None):
    if deployment_type == "aws":
        if native_account_id is None or native_resource_type is None:
            raise ValueError('Expected native_resource_type and native_account_id for \'aws\' deployment type.')
        return get_aws_asset_key(native_account_id, native_resource_type, native_resource_id)
    else:
        raise ValueError('{} deployment type is not supported by the library. Please submit a PR'.format(deployment))

def get_aws_asset_key(aws_account_id, resource_type, resource_id):
    if resource_type not in AWS_RESOURCE_MAP:
        return None

    parsed_arn = parse_arn(resource_id)
    if AWS_RESOURCE_MAP[resource_type] == "kms-key":
        return "/aws/" + "/".join([parsed_arn['region'], AWS_RESOURCE_MAP[resource_type], parsed_arn['resource']])

    if parsed_arn['region'] is "":
        return "/aws/" + "/".join([aws_account_id, AWS_RESOURCE_MAP[resource_type], parsed_arn['resource']])

    return "/aws/" + "/".join([aws_account_id, parsed_arn['region'],
                                AWS_RESOURCE_MAP[resource_type], parsed_arn['resource']])

def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':', 5)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_type': None
    }
    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/',1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':',1)
    return result
