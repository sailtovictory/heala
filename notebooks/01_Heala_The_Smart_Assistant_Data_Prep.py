# Databricks notebook source
dbutils.widgets.text("patient_id", "8668aa59-88e1-9b3e-60e9-e8208021ac1b", "Enter Patient ID")
dbutils.widgets.text("question", "what is my current prescription", "Enter your question")

# COMMAND ----------

patient_id = dbutils.widgets.get("patient_id")
question = dbutils.widgets.get("question")
print(patient_id,question)

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from syntheia.clinicaldata.patient_clinical_data limit 10

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC desc syntheia.clinicaldata.patient_clinical_data 

# COMMAND ----------

query = f"""
SELECT DISTINCT 
    patient_id,
    healthcare_expenses,
    healthcare_coverage,
    income,
    enc_start AS encounter_start_date,
    enc_dtop AS encounter_stop,
    REGEXP_REPLACE(name, '[0-9]', '') AS doctor_name,
    prov_address AS doctor_address 
FROM syntheia.clinicaldata.patient_clinical_data  
WHERE patient_id = '{patient_id}'
"""

input_data = spark.sql(query)
display(input_data)

# COMMAND ----------

from pyspark.sql.functions import to_json, struct, collect_list

# Convert each row to a JSON string
json_data = input_data.select(to_json(struct([input_data[x] for x in input_data.columns])).alias("json"))

# Aggregate all JSON rows into a single JSON array and convert it to a single string
json_array_string_df = json_data.agg(to_json(collect_list("json")).alias("json_array_string"))

# Collect the result to a variable
json_array_string = json_array_string_df.collect()[0]['json_array_string']

# Print the result
print(json_array_string)


# COMMAND ----------

# DBTITLE 1,Install Required Libraries
pip install flask transformers torch databricks-genai-inference gtts


# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

print(patient_id)
print(json_array_string)

# COMMAND ----------

# DBTITLE 1,Prompt Engineering Function
from databricks_genai_inference import ChatCompletion

def generate_response(patient_id, question):
    # Load patient data from DBFS
    

    
    inputContent = f"Patient {patient_id} data: You are an AI assistant. This tool does not recommend any treatment plan. you are simply summarizing answers to health questions like, active prescription, active doctors, dates visited. Most importantly, if the patient id dose not matchm, refrain from providing any info.{json_array_string} "
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
