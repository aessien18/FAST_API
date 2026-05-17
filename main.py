from fastapi import FastAPI, HTTPException
import random
import os
import json
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI()


class Applications(BaseModel):
    fullName: str
    email: str
    phone: str
    whatsappNumber: str
    university: str
    course: str
    level: str
    track: str
    motivation: str
    portfolioLink: str
    resumeLink: str
    joinInnovationClub: bool
    status: str
    submittedAt: str
    id: int


application_file = "applications.json"

applications = []

if os.path.exists(application_file):
    with open(application_file, "r") as f:
        applications = json.load(f)


@app.get("/")
async def home():
    return {"message": "API is running"}


@app.get("/get-application")
async def get_all_application():
    return applications


@app.get("/application/{id}")
async def get_application(id: int):
    for application in applications:
        if application["id"] == id:
            return application
    raise HTTPException(404, f"application not found")


@app.post("/add-application")
async def add_application(application: Applications):

    json_application = jsonable_encoder(application)

    json_application["id"] = len(applications) + 2

    applications.append(json_application)

    with open(application_file, "w")as f:

        json.dump(applications, f,)

    return {"message": "Application added successfully",
            "data": json_application}


@app.put("/update-application/{id}")
async def update_application(id: int, application: Applications):
    json_application = jsonable_encoder(application)
    for app in applications:
        if app["id"] == id:
            app.update(json_application)
            with open(application_file, "w") as f:
                json.dump(applications, f)
            return {
                "message": "updated successfully",
                "data": app
            }

    raise HTTPException(status_code=404, detail="Application not found")


@app.delete("/delete-application/{id}")
async def delete_application(id: int, application: Applications):
    json_application = jsonable_encoder(application)
    for app in applications:
        if app["id"] == id:
            applications.remove(app)
            with open(application_file, "w") as f:
                json.dump(applications, f)
            return {
                "message": "deleted successfully",
                "data": app
            }

    raise HTTPException(status_code=404, detail="Application not found")
