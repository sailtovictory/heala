# Databricks notebook source
# MAGIC %sql
# MAGIC select count(*) from syntheia.clinicaldata.medications

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from syntheia.clinicaldata.patient_clinical_data

# COMMAND ----------

# MAGIC %sql
# MAGIC select distinct encounter , count(*) from syntheia.clinicaldata.medications
# MAGIC group by encounter order by encounter

# COMMAND ----------

# MAGIC %sql
# MAGIC select distinct encounter , count(*) from syntheia.clinicaldata.patient_clinical_data
# MAGIC group by encounter order by encounter

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.patient_clinical_data where encounter = '007c790e-3579-d673-5695-5baf82d4ce75'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from syntheia.clinicaldata.medications where encounter = '007c790e-3579-d673-5695-5baf82d4ce75'
