from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.secret_key = "Sbu"

testArray = []

@app.route('/incoming', methods=['POST'])
def incoming():
    greeting = "Welcome to e-Joburg Whatsapp chat services, how can we help you?\n Please select one of the options below:\n"
    options = "1-Report a problem\n 2-Enquire about a logged fault status."
    msg = request.form.get('Body')
    resp = MessagingResponse()
    id = request.form['From']

    if id not in testArray:
        testArray.append(id)
        resp.message(greeting + options)
        return str(resp)

    if 'option' not in session and id in testArray and msg not in ['1', '2']:
        resp.message("Please select a valid option\n" + options)
        return str(resp)

    if msg == '1':
        session['option'] = '1'
        session['description'] = '_'
        resp.message("Please provide a description of the problem")
        return str(resp)

    if msg == '2':
        session['option'] = '2'
        session['description'] = '_'
        resp.message("Feature under development")
        return str(resp)

    if session['description'] == '_':
        session['description'] = msg
        resp.message("Thank you for providing the description of the problem.\n Please provide a picture of the fault for analysis")
        return str(resp)

    if 'MediaUrl0' in request.form:
        media_url = request.form['MediaUrl0']
        session['image'] = media_url
        resp.message("Thanks for the image! Please provide the location\n\nNote: the image can be obtained from: " + str(media_url))
        return str(resp)
    elif 'MediaUrl0' not in request.form and 'image' not in session and 'description' in session:
        resp.message("You did not send an image, please try again.")
        return str(resp)

    if 'Latitude' in request.form and 'Longitude' in request.form:
        latitude = request.form['Latitude']
        longitude = request.form['Longitude']
        session['location'] = (latitude, longitude)
        session['address'] = str(request.form.get('Address'))
        resp.message("Thank you, location received at " + session['address'])
        return str(resp)
    

    #resp.message("Please provide a picture of the fault.")
    return str(resp)

#
if __name__ == '__main__':
    app.run()
