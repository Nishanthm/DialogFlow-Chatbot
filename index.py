from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
from bs4 import BeautifulSoup
import requests
from flip_amzon import get_prod_disc 
from product_scrape import get_bank_disc
from sqlconnect import insert_item
from sqlconnect import insert_bank
from sqlconnect import get_high

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# run Flask app
if __name__ == "__main__":
    app.run()
@app.route('/webhook', methods=['POST'])
def get_movie_detail():
    data = request.get_json(silent=True)
    reply = {
        "fulfillmentText":"I will take a short nap..."}
    if data['queryResult']['intent']['displayName'] == "passshow":
        reply = {
        "fulfillmentText":get_high() }
    elif data['queryResult']['intent']['displayName'] == "bankoffer":
    	bank = data['queryResult']['parameters']['bank']
        #sqlconnect.insert_bank(bank)
    	reply = {
        "fulfillmentText":get_bank_disc(bank) }
    elif data['queryResult']['intent']['displayName'] == "product offer":
    	product = data['queryResult']['parameters']['any']
        #sqlconnect.insert_item(product)
    	reply = {
        "fulfillmentText":get_prod_disc(product) }
    else:
    	reply = {
        "fulfillmentText":"I will take a short nap..."}

    return jsonify(reply)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    return jsonify(response_text)