from openai import OpenAI

client = OpenAI(api_key=os.getenv("api_key"))

SYSTEM_PROMPT = f"""
    Your name is Jarvis. Your role is to recommend travel plans and transfer knowledge to those who use this app.
    The recommended data is returned in JSON format.
    You should provide the best results to users based on API and OPEN AI results that recommend travel based on their utterances.
    Also, if the request value is foreign data, you have to translate it accordingly and return it.
"""

MESSAGE = [
    {
        'role': 'system',
        'content': SYSTEM_PROMPT
    }
]

def functionCallService(request, recommend: list):
    travel_plan = {
        "startPoint": {
            "name": "start point name",
            "latitude": 0.0,
            "longitude": 0.0
        },
        "endPoint": {
            "name": "end point name",
            "latitude": 0.0,
            "longitude": 0.0
        },
        "pointList": [
            {
                "name": "place 1",
                "latitude": 0.0,
                "longitude": 0.0,
                "message": "place 1 message",
                "status": "restaurant"
            },
        ],
        "message": "travel plan message",
        "pointMessage": "point message",
        "weatherMessage": "weather message"
    }

    PROMPT = f"""
        It is an AI that recommends places where you want to play and eat after listening to the user's voice.
        If the content of the question does not fit the context in which you recommend a place, mark null everywhere except the "Message" column
        Also, the message is not able to recommend a place, so it kindly answers other questions.
        When you recommend it, you should recommend it based on the data I provided
        I'll tell you the latitude and longitude of the starting point, so please write down the location name
        
        I don't want you to go out of JSON format

        The input is as follows
        
        - latitude: starting point latitude
            {request.latitude}
        - longitude: starting point longitude
            {request.longitude}
            
        - weather: weather information
            {request.weather}
        
        - command: user command
            {request.command}
            
        - recommend: A list of recommended places requested by the user. Please recommend a list of recommended places, including restaurant, activity, and tourist 
            {recommend}
        
        I hope the return value comes in JSON form as below.
        If the command value is in a foreign language, please translate it and return it.
        The message column would like you to tell me why you recommended the places in the referral
        And I want you to speak like a friend
        
        {travel_plan}
        
    """
    print(PROMPT)

    MESSAGE.append(
        {"role": "user", "content": PROMPT}
    )


    completion = client.chat.completions.create(
        model='gpt-4o-2024-08-06',
        messages=[{'role': 'user', 'content': PROMPT}],
        temperature=0.0
    )
    return completion.choices[0].message.content
