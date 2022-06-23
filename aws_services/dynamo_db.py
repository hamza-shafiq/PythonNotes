import boto3
from botocore.exceptions import ClientError


class DynamoDB:
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.db = boto3.resource("dynamodb")

    def create_table(self, table_name='Devices'):
        table = self.db.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'device_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'data_count',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'device_id',
                    # AttributeType defines the data type. 'S' is string type and 'N' is number type
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'data_count',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                # ReadCapacityUnits set to 10 strongly consistent reads per second
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
            }
        )

        return table

    def load_data(self, dataset, table_name='Devices'):
        _table = self.db.Table(table_name)
        for data in dataset:
            _table.put_item(Item=data)

    def read_data(self, table_name, key=None):
        _table = self.db.Table(table_name)

        try:
            response = _table.get_item(Key={
                'id': '1',
                'other': 'other'
            })
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def update_data(self, table_name, key={"id": 1}):
        _table = self.db.Table(table_name)

        response = _table.update_item(
            Key=key,
            UpdateExpression="set info.info_timestamp=:time, info.temperature=:temp",
            ExpressionAttributeValues={
                ':time': 'info_timestamp',
                ':temp': 'temperature',
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_data(self, table_name, key={"id": 1}):
        _table = self.db.Table(table_name)
        try:
            response = _table.delete_item(
                Key=key,
                # Conditional request
                ConditionExpression="info.info_timestamp <= :value",
                ExpressionAttributeValues={
                    ":value": 'info_timestamp'
                }
            )
        except ClientError as er:
            if er.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(er.response['Error']['Message'])
            else:
                raise
        else:
            return response

    def delete_table(self, table_name):
        _table = self.db.Table(table_name)
        _table.delete()
