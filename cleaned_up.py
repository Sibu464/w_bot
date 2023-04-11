from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.secret_key = "Sbu"

# Array to keep track of users who have interacted with the chatbot
users = []

# Options available to users
options = "1-Report a problem\n2-Enquire about a logged fault status."

@app.route('/incoming', methods=['POST'])
def incoming():
    # Welcome message sent to new users
    welcome_message = f"Welcome to e-Joburg WhatsApp chat services, how can we help you?\nPlease select one of the options below:\n{options}"

    # Create a MessagingResponse object
    resp = MessagingResponse()

    # Get the user ID and message
    user_id = request.form['From']
    message = request.form.get('Body')

    if user_id not in users:
        # Add new user to the list of users
        users.append(user_id)
        resp.message(welcome_message)
    else:
        if 'option' not in session:
            # User has not selected an option yet
            if message in ['1', '2']:
                # User selected a valid option
                session['option'] = message

                if session['option'] == '1':
                    # User selected to report a problem
                    session['description'] = ""  # Reset description
                    resp.message("Please provide a description of the problem")
                else:
                    # User selected to enquire about a logged fault status
                    resp.message("Feature under development")
            else:
                # User did not select a valid option
                resp.message(f"Please select a valid option\n{options}")
        else:
            # User has already selected an option
            if session['option'] == '1':
                # User is reporting a problem
                if session['description'] == "":
                    # User has not provided a description yet
                    session['description'] = message
                    resp.message("Thank you for providing the description of the problem. Please provide a picture of the fault for analysis.")
                elif 'MediaUrl0' in request.form:
                    # User has provided a picture
                    session['image'] = request.form['MediaUrl0']
                    resp.message(f"Thanks for the image! Please provide the location.\n\nNote: The image can be obtained from: {session['image']}")
                #else:
                    # User has not provided a picture yet
                    #resp.message("Please provide a picture of the fault.")
            else:
                # User is enquiring about a logged fault status
                resp.message("Feature under development")

    if session.get('image') and ('Latitude' in request.form):
        # User has provided a picture and location
        session['location'] = (request.form['Latitude'], request.form['Longitude'])
        session['address'] = request.form.get('Address')
        resp.message(f"Thank you! Location received at {str(session['location'][0])}")

    return str(resp)

@app.route('/webhook', methods=['GET'])
def get_webhook():
    return 'This is a webhook for receiving SMS messages.'

@app.route('/dashboard', methods=['GET'])
def get_dash():
    return 'Dashboard route.'

if __name__ == '__main__':
    app.run()
