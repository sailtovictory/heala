# Databricks notebook source
dbutils.widgets.text("patient_id", "12345", "Enter Patient ID")
dbutils.widgets.text("question", "what is my current prescription", "Enter your question")

# COMMAND ----------

patient_id = dbutils.widgets.get("patient_id")
question = dbutils.widgets.get("question")
print(patient_id,question)

# COMMAND ----------

# DBTITLE 1,Install Required Libraries
pip install flask transformers torch databricks-genai-inference gtts


# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Sample Code to generate response
#sample code.
from databricks_genai_inference import ChatCompletion

response = ChatCompletion.create(model="databricks-dbrx-instruct",
                                 messages=[{"role": "system", "content": "You are a helpful assistant.Patient 12345 data: Visit on 2023-06-01 with Dr. Vidya: Patient complained of headache and nausea.. Prescriptions: Ibuprofen 200mg twice a day. Visit on 2023-06-15 with Dr. Krishna: Follow-up visit. Headache has subsided.. Prescriptions: Ibuprofen 200mg once a day. Alert on 2023-06-10: Prescription for Ibuprofen needs to be renewed"},
                                           {"role": "user","content": "who are my active doctors?"}],
                                 max_tokens=128)
print(f"response.message:{response.message}")


# COMMAND ----------

# DBTITLE 1,Sample Data
import json
# No need to import SparkSession for this operation

# Assuming dbutils is available in your environment. If not, you might need to import it.
# from pyspark.dbutils import DBUtils
# dbutils = DBUtils(spark)

patient_data = [
    {
        "patient_id": "12345",
        "visits": [
            {
                "date": "2023-06-01",
                "doctor": "Dr. Krishna",
                "notes": "Patient complained of headache and nausea.",
                "prescriptions": [
                    {
                        "medication": "Ibuprofen",
                        "dosage": "200mg",
                        "frequency": "twice a day"
                    }
                ]
            },
            {
                "date": "2023-06-15",
                "doctor": "Dr. Vidya",
                "notes": "Follow-up visit. Headache has subsided.",
                "prescriptions": [
                    {
                        "medication": "Ibuprofen",
                        "dosage": "200mg",
                        "frequency": "once a day"
                    }
                ]
            }
        ],
        "alerts": [
            {
                "date": "2023-06-10",
                "message": "Prescription for Ibuprofen needs to be renewed."
            }
        ]
    }
]



# COMMAND ----------

# DBTITLE 1,Prompt Engineering Function
from databricks_genai_inference import ChatCompletion

def generate_response(patient_id, question):
    # Load patient data from DBFS
    

    patient_info = next((p for p in patient_data if p["patient_id"] == patient_id), None)
    if not patient_info:
        return "Patient data not found."

    context = ""
    for visit in patient_info.get("visits", []):
        context += f"Visit on {visit['date']} with {visit['doctor']}: {visit['notes']}. Prescriptions: " + \
                   ", ".join([f"{p['medication']} {p['dosage']} {p['frequency']}" for p in visit['prescriptions']]) + ". "
    
    for alert in patient_info.get("alerts", []):
        context += f"Alert on {alert['date']}: {alert['message']}. "

    inputContent = f"Patient {patient_id} data: You are an AI assistant. This tool does not recommend any treatment plan. you are simply summarizing answers to health questions like, active prescription, active doctors, dates visited. Most importantly, if the patient id dose not matchm, refrain from providing any info.{context} "
    promptContent = f"Question: {question}"
    
    response = ChatCompletion.create(model="databricks-dbrx-instruct",
                                 messages=[{"role": "system", "content": inputContent},
                                           {"role": "user","content": promptContent}],
                                 max_tokens=128)
#print(f"response.message:{response.message}")
    
    return response.message
    #return prompt

# COMMAND ----------

# DBTITLE 1,Function Output
generate_response(patient_id,question)

# COMMAND ----------

# DBTITLE 1,Convert the answer to audio feedback


from gtts import gTTS
import IPython.display as ipd

def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    tts.save("/tmp/output.mp3")
    return ipd.Audio("/tmp/output.mp3")

response_text = generate_response(patient_id, question)
audio_output = text_to_audio(response_text)
display(audio_output)
