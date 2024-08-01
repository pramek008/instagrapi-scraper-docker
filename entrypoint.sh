#!/bin/bash

# Start the Flask app
gunicorn -b 0.0.0.0:5000 app.app:app &

# Start ngrok
ngrok authtoken 2d1erBbjPCew1TB2eIzUkPyVdns_RBVH8pULVYP2A5bV1PDy
ngrok http 5000
