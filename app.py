#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import numpy as np
import openai
import streamlit as st

df = pd.read_csv("age_gender_bkts.csv",sep=",", encoding='Latin-1')
st.text("Age gender table")
st.dataframe(df.head())

df3=pd.read_csv('test_users.csv')
st.text("test users table")
st.dataframe(df3.head())

df2=pd.read_csv('countries.csv')
st.text("countries table")
st.dataframe(df2.head())

# df4=pd.read_csv('sessions.csv')
# st.text("Sessions table")
# st.dataframe(df4.head())

df5=pd.read_csv('train_users_2.csv')
st.text("train_users_2 table")
st.dataframe(df5.head())


## Querying Data


#df3=pd.read_csv('test_users.csv')
# temp_db = create_engine('sqlite:///:memory:', echo=True)
#Here we push our entire DataFrame to a table called Sales:
# data = df3.to_sql(name='test',con=temp_db)

### Connecting to SQL Database:
#Using SQL Alchemy to establish a connection to this temporary database and query it for the results:
# df3
# with temp_db.connect() as conn:
#     result = conn.execute(text("Select gender from test "))
# result.all()
## OpenAI API

### Set-up Open AI API Key

#Goto account section for the same
#openai.api_key = os.getenv("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")
### Inform GPT about the SQL Table Structure



def create_table_definition_prompt(df,table_name):
    """
    This function returns a prompt that informs GPT that we want to work with SQL Tables
    """

#     prompt = '''### sqlite SQL table, with its properties:
# #
# # test({})
# # with column gender having values:{}
# '''.format(",".join(str(x) for x in df.columns),df['gender'].unique().tolist())
    prompt = '''### sqlite SQL table, with its properties:
#
# table name is {}
# table columns are({})
'''.format(table_name,",".join(str(x) for x in df.columns))

    cat_df3=df.select_dtypes(include=['object'])
    fin_str=''' '''
    for cols in cat_df3.columns:
      if(cat_df3[cols].nunique()<=20):
        fin_str+='''with column {} having values {}
        '''.format(cols,cat_df3[cols].unique().tolist())


    return prompt + fin_str

### Get Natural Language Request:

#Creating a function that grabs the natural language information request:
# def prompt_input():
#     nlp_text = input("Enter information you want to obtain: ")
#     return nlp_text
# nlp_text = prompt_input()


def combine_prompts(df, df2, df3,df5,query_prompt):
    definition1 = create_table_definition_prompt(df,'age_gender')
    definition2 = create_table_definition_prompt(df2,'countries')
    definition3 = create_table_definition_prompt(df3,'test_users')
    #definition4 = create_table_definition_prompt(df4,'sessions')
    definition5 = create_table_definition_prompt(df5,'train_users_2')
    #column_descriptions = get_columns_values(df)
    query_init_string = f"### A query to answer: {query_prompt}\nSELECT"
    return definition1+definition2+definition3+definition5+query_init_string


#GPT will complete the text above, thus we start to notify it to begin a SQL query by writing "\nSELECT"

#Now let's get the response:

### OpenAI API Call

st.title("NLP to SQL")
nlp_text = st.text_input("Provide your text input here","Hello")
button_clicked = st.button("Convert to sql")

#Let's use the Text DaVinci model
openai.api_key = "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"
response = openai.Completion.create(
  model="text-davinci-003",
  #prompt="### sqlite SQL table, with its properties:## test(id,date_account_created,timestamp_first_active,date_first_booking,gender,age,signup_method,signup_flow,language,affiliate_channel,affiliate_provider,first_affiliate_tracked,signup_app,first_device_type,first_browser)#### A query to answer: number of women having iphone deviceSELECT"
  prompt=combine_prompts(df,df2,df3,df5, nlp_text),

  temperature=0,
  max_tokens=150,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["#", ";"]
)


#Building a function to parse the section of the response we want:
def handle_response(response):
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select"+ query
    return query
if button_clicked:
    st.text(handle_response(response))

#Now we just pass that into our Database:

#combine_prompts(df,df2,df3,df4,df5, nlp_text)

