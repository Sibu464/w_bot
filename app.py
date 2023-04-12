from flask import Flask, request,session,render_template
from PIL import Image
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
testArray=[]
app.secret_key ="Sbu"
def description():
    resp=MessagingResponse()
    if 'description' not in session:
        session['description']="_" #no description given yet      
        res="Please provide a description of the problem"
        return res
    elif session['description']=="_":
        msg=request.form.get('Body')
        session['description']=str(msg)
        res="Thank for the description"
        return res
        
@app.route('/incoming', methods=['POST'])
           
def incoming():
    greeting="Welcome to e-Joburg Whatsapp chat services, how can we help you?\n Please select one of the options below:\n"
    options="1-Report a problem\n 2-Enquire about a logged fault status." 
    msg=request.form.get('Body')   
    resp=MessagingResponse()
    id=request.form['From']

    if id not in testArray:
        testArray.append(id)
        resp.message(greeting+options)
        return str(resp)
    elif 'option' not in session and id in testArray and msg not in ['1','2']:
        resp.message("Please select a valid option\n"+options)
        return str(resp)
    elif msg=='1':
        session['option']='1'
        resp=MessagingResponse()
        session['description']="_" #no description given yet      
        res="Please provide a description of the problem"
        resp.message(res)
        return str(resp)
    elif msg=='2':
        session['option']='2'
        resp=MessagingResponse()
        session['description']="_" #no description given yet      
        res="Feature under development"
        resp.message(res)
        return str(resp)

    if session['description']=='_':
       session['description']=msg
       res="Thank you for providing the description of the problem.\n Please provide a picture of the fault for analysis" 
       resp.message(res)
       return str(resp)
    if session['description']!='_' and len(session['description'])>0:
        if 'MediaUrl0' in request.form:
            media_url = request.form['MediaUrl0']
            session['image']=media_url
            resp.message("Thanks for the image!, please provide the location\n\n Note: the image can be obtained from: "+str(media_url))
            return str(resp)
        else:
             return str(resp.message('Please provide a picture of the fault. A picture'))

    if 'image' in session:
        if 'Latitude' in request.form:
            latitude = request.form['Latitude']
            longitude = request.form['Longitude']
            session['location']=(latitude,longitude)
            session['address']=str(request.form.get('Address'))
            resp.message("Thank you, location received at "+session['address'])
            return str(resp)
        else:
            resp.message("Please send the correct data.")
            return str(resp)


    
    

    
@app.route('/webhook', methods=['GET'])
def get_webhook():
    return 'This is a webhook for receiving SMS messages.'
    
@app.route('/dashboard', methods=['GET'])
def get_dash():
    return render_template('index.html')
if __name__ == '__main__':
    app.run()
