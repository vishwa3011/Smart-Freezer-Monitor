from twilio.rest import Client

#account_sid = your id on twilio
#auth_token = token given by twilio
client = Client(account_sid, auth_token)

def send():
    message = client.messages.create(
                                  #to='a mobile number',
                                  #from_=' mobile number',
                                  body="Alert! Your freezer has been opened for over 2 minutes! Ignore if freezer is being filled."
                              )

    print(message.sid)
