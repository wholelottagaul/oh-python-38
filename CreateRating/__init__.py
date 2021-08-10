import json
import uuid
from datetime import datetime
import azure.functions as func
import requests


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    try:
        rating = req.get_json()
    except ValueError:
        pass

    if rating:
        if not validateForeignKey("https://serverlessohapi.azurewebsites.net/api/GetProduct", {'productId': rating['productId']}):
            return func.HttpResponse(
                "Invalid Product Id",
                status_code=400
            )
        
        if not validateForeignKey("https://serverlessohapi.azurewebsites.net/api/GetUser", {'userId': rating['userId']}):
            return func.HttpResponse(
                "Invalid User Id",
                status_code=400
            )
            
        rating['id'] = str(uuid.uuid4())
        rating['timestamp'] = str(datetime.now())

        ratingAsJson = json.dumps(rating)

        doc.set(func.Document.from_json(ratingAsJson))
        
        return func.HttpResponse(
            ratingAsJson,
            status_code=200
        )            
    else:
        return func.HttpResponse(
             "No rating object found",
             status_code=400
        )

def validateForeignKey(url, params):
    result = requests.get(url, params=params)
    return result.status_code == 200        
