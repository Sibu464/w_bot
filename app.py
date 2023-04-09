from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    msg=request.form.get('Body')
    resp=MessagingResponse()
    resp.message("Welcome to the City of Joburg bot {}".format(msg))
    return str(resp)
    
@app.route('/webhook', methods=['GET'])
def get_webhook():
    return 'This is a webhook for receiving SMS messages.'

if __name__ == '__main__':
    app.run()
