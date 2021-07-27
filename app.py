import os
from google.api_core.exceptions import InvalidArgument
import dialogflow
from flask import Flask, render_template, request, jsonify
from google.api_core.gapic_v1 import method
from db_utils import insert_conversations, get_conversations, get_conversations_by_date, get_misses_by_date, get_misses
from file_ops import write_fallback_csv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
DIALOGFLOW_PROJECT_ID = 'newagent-jojg'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

#text_to_be_analyzed = "how does covid spread?"

welcome_message = '''Hello! I am a covid bot. I can answer questions related to covid. 
You can ask me questions regarding the symptoms, precautions and other general information on covid'''

app = Flask(__name__,
            template_folder='client/templates',
            static_folder='client/static')


def get_response(text_to_be_analyzed):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        insert_conversations(text_to_be_analyzed, response.query_result.intent.display_name)
        '''if response.query_result.intent.display_name == "Default Fallback Intent":
            write_fallback_csv(text_to_be_analyzed)'''

        return response.query_result.fulfillment_text
    except InvalidArgument:
        raise


@app.route('/')
def index():
    return render_template('chat.html', message=welcome_message)


@app.route('/get_reply', methods=["POST"])
def get_reply():
    text = request.form["text"]
    reply = get_response(text)
    return jsonify({'text': reply})


@app.route('/conversations', methods=["GET", "POST"])
def conversations():
    if request.method == 'GET':
        messages = get_conversations()
        return render_template('conversations.html', messages=messages)
    elif request.method == 'POST':
        from_date = request.form['fromdate']
        to_date = request.form['todate']
        messages = get_conversations_by_date(from_date, to_date)
        return render_template('conversations.html', messages=messages)

@app.route('/misses', methods=["GET", "POST"])
def misses():
    if request.method == 'GET':
        messages = get_misses()
        return render_template('misses.html', messages=messages)
    elif request.method == 'POST':
        from_date = request.form['fromdate']
        to_date = request.form['todate']
        messages = get_misses_by_date(from_date, to_date)
        return render_template('misses.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True, port=3001)
