import json
from typing import Optional

import pandas as pd

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "Phonebook"


@app.post("/add_user")
async def add_user(firstname: str, lastname: str, phone_number: str, age: Optional[int] = None):
    try:
        df_phonebook = pd.read_csv('db.csv')
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname', 'Lastname', 'Phone number', 'Age'])

    user_dict = {}
    user_dict["Firstname"] = firstname
    user_dict["Lastname"] = lastname
    user_dict["Phone number"] = phone_number
    if age:
        user_dict["Age"] = age
    else:
        user_dict["Age"] = None

    df_temp = pd.DataFrame([user_dict])
    print(df_phonebook)
    print(df_temp)
    df_phonebook = pd.concat([df_phonebook, df_temp])
    df_phonebook.to_csv('db.csv')
    return 'User added successfully'


@app.get('/get-user')
async def get_user(lastname: str):
    try:
        df_phonebook = pd.read_csv('db.csv')
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname', 'Lastname', 'Phone number', 'Age'])

    found_user = df_phonebook[df_phonebook['Lastname'] == lastname]
    print(found_user)
    print(dict(found_user.iloc[0]))
    if found_user.empty:
        return 'There is no such user'
    return found_user.to_dict(orient='records')
