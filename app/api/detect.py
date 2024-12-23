from fastapi import APIRouter, Request
from pydantic import BaseModel
from model.QA_model import QA_model as model
from model.combine import multi_user
router = APIRouter()

model_name = "deepset/xlm-roberta-large-squad2"
model = model(model_name, model_name)

# Define a Pydantic model to parse the incoming JSON data
class MessageData(BaseModel):
    timeMessage: str
    collectedText: str


# Define an endpoint to handle the incoming data
@router.post("/submit-data")
async def submit_data(data: MessageData):
    # Access timeMessage and collectedText from the request
    time_message = data.timeMessage
    collected_text = data.collectedText

    # For demonstration, print or process the data as needed
    print("Time Message:", time_message)
    time = time_message.split(" ")
    print(time[0])
    h = time[0] if time[0].isdigit() else 0
    m = time[1] if time[1].isdigit() else 0
    print(time[1])
    time = int(h) * 60 + int(m)
    messages = collected_text.split("\n")[:-1]
    print("Collected Text:", messages)
    # Return a response
    r = multi_user(model, messages, time)
    result= [[] for _ in range(7)]
    for i in range(7):
        result[i] = group_numbers(r[i],time )
    print(result)
    return result

def group_numbers(list, time):
    """
    get all time continus in time
    """
    result = []
    if list == []:
        return[-1]
    list = sorted(list)
    grouped = []
    current_group = []

    for number in list:
        lower_bound = (number + 1 + time) + 540
        upper_bound = (number + 1 + time ) +  1440

        if not current_group:
            current_group.append(number)
        else:
            last_number = current_group[-1]
            last_lower_bound = (number + 1 + time ) +  540
            last_upper_bound = (number + 1 + time ) +  1440

            if lower_bound <= last_upper_bound:
                current_group.append(number)
            else:
                grouped.append(current_group)
                current_group = [number]

    if current_group:
        grouped.append(current_group)
    for gr in grouped:
        print(gr[0])
        result.append( (gr[0] +  540, gr[-1]  +  540 + 1 + time) )
    return result
# Run the FastAPI server using: uvicorn script_name:app --reload
