def send_sms(self):
    try:
        response = self.sns_resource.meta.client.publish(
            PhoneNumber=phone_number, Message=message
        )
        message_id = response["MessageId"]
        logger.info("Published message to %s.", phone_number)
    except ClientError:
        logger.exception("Couldn't publish message to %s.", phone_number)
        raise
    else:
        return message_id
