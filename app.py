from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
testArray=[]
app.secret_key = request.form['From']
def description():
    resp=MessagingResponse()
    if 'description' not in session:
        session['description']="_" #no description given yet      
        resp.message("Please provide a description of the problem")
        return str(resp)
    elif session['description']=="_":
        msg=request.form.get('Body')
        session['description']=msg
        resp.message("Thank for the description")
        return str(resp)
        
@app.route('/incoming', methods=['POST'])

            
def incoming():
    greeting="Welcome to e-Joburg Whatsapp chat services, how can we help you?\n Please select one of the options below:"
    options="1-Report a problem\.n 2-Enquire about a logged fault status." 
    msg=request.form.get('Body')   
    resp=MessagingResponse()
    id=request.form['From']
    if id not in testArray:
        testArray.append(id)
        resp.message(greeting)
        return str(resp+options)
    elif msg not in ['1','2']:
        resp.message("Please select a valid option\n"+options)
        return str(resp)
    elif msg=='1':
        description()
        
        
        
    

    
@app.route('/webhook', methods=['GET'])
def get_webhook():
    return 'This is a webhook for receiving SMS messages.'
    
@app.route('/dashboard', methods=['GET'])
def get_dash():
    return 'Dashboard route.'
if __name__ == '__main__':
    app.run()
