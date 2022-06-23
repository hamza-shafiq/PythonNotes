import boto3


class SQS:
    def __init__(self, access_key, access_secret, region, queue_url):
        self.aws_access_key_id = access_key
        self.aws_secret_access_key = access_secret
        self.region = region
        self.queue_url = queue_url

    def send_message(self, message):
        sqs = boto3.client('sqs', region_name=self.region,
                           aws_access_key_id=self.aws_access_key_id,
                           aws_secret_access_key=self.aws_secret_access_key)
        try:
            # Send message to SQS queue
            response = sqs.send_message(
                QueueUrl=self.queue_url,
                DelaySeconds=0,
                MessageAttributes={},
                MessageBody=(
                    message
                ),
                MessageGroupId='AeyJjb21wYW55IjoiYWNxdS5jbyIsInByb2plY3QiOiJhcGktZXRsIiwiIjoiIn0'
            )

            return response['MessageId']

        except Exception as e:
            print("Exception occur while sending message to SQS. Error: {}".format(str(e)))

        return None

    def receive_message(self, remove_after_read=False):
        sqs = boto3.client('sqs', region_name=self.region,
                           aws_access_key_id=self.aws_access_key_id,
                           aws_secret_access_key=self.aws_secret_access_key)
        message_list = []
        try:
            # Receive message from SQS queue
            response = sqs.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=10,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=100,
                WaitTimeSeconds=0
            )
            if "Messages" in response:
                fetched_messages = response["Messages"]
                for msg in fetched_messages:
                    message_list.append({
                        "MessageId": msg["MessageId"],
                        "Body": msg["Body"],
                    })

                    if remove_after_read:
                        receipt_handle = msg['ReceiptHandle']
                        self.delete_message(sqs, receipt_handle)

        except Exception as e:
            print("Exception occur while fetching message from SQS. Error: {}".format(str(e)))

        return message_list

    def delete_message(self, sqs, receipt_handle):
        try:
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
        except Exception as e:
            print("Exception occur while deleting message from SQS. Error: {}".format(str(e)))


if __name__ == "__main__":
    sqs_instance = SQS(access_key="", access_secret="", region="", queue_url="")

    # # Send message to SQS
    # message = "Alpha Beta Gamma"
    # msg_queued = sqs_instance.send_message(message=message)
    #
    # # Fetch messages from SQS
    # messages = sqs_instance.receive_message(remove_after_read=False)
