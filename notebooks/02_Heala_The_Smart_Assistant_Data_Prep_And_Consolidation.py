# Databricks notebook source
# MAGIC %md
# MAGIC source data from https://synthea.mitre.org/downloads

# COMMAND ----------

# MAGIC %md
# MAGIC Four source tables: patients, encounter, medications, providers

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.patients

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.encounters

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.medications

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.providers

# COMMAND ----------

# MAGIC %md
# MAGIC Consolidate data from the tables patient, encounter, medication and provider into a new table patient_clinical_data.
# MAGIC Medications are at encounter level for each patient.

# COMMAND ----------

# MAGIC %sql
# MAGIC create table syntheia.clinicaldata.patient_clinical_data as (
# MAGIC select p.Id as patient_id, BIRTHDATE, DEATHDATE, SSN, DRIVERS, PASSPORT, PREFIX, FIRST, MIDDLE, LAST, SUFFIX, MAIDEN, MARITAL, RACE, ETHNICITY, p.GENDER, BIRTHPLACE, p.ADDRESS, p.CITY, p.STATE, COUNTY, FIPS
# MAGIC ZIP, p.LAT, p.LON, HEALTHCARE_EXPENSES, HEALTHCARE_COVERAGE, INCOME, e.Id as encounter_id, e.START as enc_start, e.STOP as enc_dtop, e.PATIENT as enc_patient, e.ORGANIZATION, PROVIDER, e.PAYER, ENCOUNTERCLASS, e.CODE enc_code,e.DESCRIPTION as enc_desc, BASE_ENCOUNTER_COST, TOTAL_CLAIM_COST, e.PAYER_COVERAGE as enc_payer_coverage, e.REASONCODE as enc_reasoncode, e.REASONDESCRIPTION enc_reasondesc,m.START as med_start_dt, m.STOP as med_stop_dt, m.PATIENT as med_patient, m.PAYER as med_payer, ENCOUNTER, m.CODE med_code, m.DESCRIPTION as med_description, BASE_COST, m.PAYER_COVERAGE
# MAGIC DISPENSES, TOTALCOST, m.REASONCODE, m.REASONDESCRIPTION, 
# MAGIC prov.Id as prov_id, prov.ORGANIZATION prov_organization, prov.NAME, prov.GENDER as prov_gender, SPECIALITY, prov.ADDRESS as prov_address, ENCOUNTERS, PROCEDURES
# MAGIC from syntheia.clinicaldata.patients as p
# MAGIC join syntheia.clinicaldata.encounters as e on p.id = e.PATIENT
# MAGIC join syntheia.clinicaldata.medications as m on p.id = m.PATIENT and m.ENCOUNTER = e.id
# MAGIC join  syntheia.clinicaldata.providers as prov on prov.id= e.provider)
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from syntheia.clinicaldata.patient_clinical_data

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from syntheia.clinicaldata.medications

# COMMAND ----------

# MAGIC %md
# MAGIC Confirming medications are at encounter level.

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.medications m
# MAGIC join syntheia.clinicaldata.encounters e on m.PATIENT = e.patient and m.ENCOUNTER = e.id
