# HEALA - A Smart Personal Assistant For Your Health Visits
![alt text](https://github.com/sailtovictory/heala/blob/main/UI/PHOTO-2024-06-10-15-01-52.jpg)

"""
# Project Documentation

## Overview

What if healthcare companies can help their customers by providing them access to summarized visit notes, prescriptions, alerts, doctor information. All this exists today then what is new? 

An app that listens to the questions of the healthcare customers and answers them based on the encounters, medications and provider information. 

ENGLISH IS THE NEW CODING LANGUAGE - Take advantage and create conversational methods to answer simple questions. Keep the customers aware of the prescription they need to take. Alert them on their appointments. Answer their questions related to their visits especailly for the people who needs assistance.


What is my current prescription? 

What is the name of my doctor I visited six months ago?

Did I take my medication this morning?

These are easy questions but are they easy questions to people who needs assistance? This project aims to be your personal assistant to answer your queries related to your recent health visits. The idea is to allow healthcare companies manage the health and lives of their patients by creating a simple app and sharing with their customers. This app will summarize their recent visits, any active prescriptions, alert for medication to be taken.


## Components
- **Function Output**: Utilizes `generate_response(patient_id, question)` to generate a text response. THis uses dbrx_instruct model for summarization.
- **Convert the answer to audio feedback**: Converts the generated text response into audio using the `text_to_audio` function, which employs the gTTS library.

## Data Sources
https://synthea.mitre.org/downloads

## Dependencies
- gTTS: Google's Text-to-Speech API, used for converting text responses into audio.
- IPython.display: Used for displaying the audio file within the notebook.

## Usage
1. Call `generate_response(patient_id, question)` to get a text response.
2. Pass the text response to `text_to_audio(text)` to get an audio representation.
3. Use `display(audio_output)` to play the audio within the notebook.
