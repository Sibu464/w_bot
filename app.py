from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_message = request.values.get("key","fuck").lower()
    the_data=request.get_json()
    if the_data['key']=='hello':
    
        return 'ngiyaphendula as a server'
    
    resp = MessagingResponse()
    if 'hello' in incoming_message:
        resp.message("Hi there!")
    elif 'goodbye' in incoming_message:
        resp.message("See you later!")
    else:
        resp.message("you said: "+incoming_message)
    
    #return str(resp)
    
@app.route('/webhook', methods=['GET'])
def get_webhook():
    return 'This is a webhook for receiving SMS messages.'

if __name__ == '__main__':
    app.run()
