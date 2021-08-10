import logging
import json
import uuid
from datetime import datetime
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        rating = req.get_json()
    except ValueError:
        pass

    if rating:
        rating.id = str(uuid.uuid4())
        rating.timestamp = datetime.now()

        return func.HttpResponse(
             json.dumps(rating),
             status_code=200
        )
        return 
    else:
        return func.HttpResponse(
             "No rating object found",
             status_code=400
        )

