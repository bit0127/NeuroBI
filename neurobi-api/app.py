from chalice import Chalice
from openai import OpenAI
# from chalicelib.bi_reporting import fetch_sample_data
from chalicelib.secret_manager import get_openai_api_key
import pandas as pd

app = Chalice(app_name='neuro-bi-api')

# CORS settings for the whole app
app.api.cors = {
    "allow_origins": ["http://localhost:3000"],  # You can replace "*" with specific domains for added security
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed methods
    "allow_headers": ["Content-Type", "Authorization"],  # Allowed headers
}



def fetch_sample_data():
    # Mock function to simulate data fetching
    return pd.DataFrame({
        "Year": [2020, 2021, 2022],
        "Passengers": [50000, 60000, 70000],
        "Revenue": [1000000, 1200000, 1400000]
    })

@app.route('/bi-insights', methods=['POST'], content_types=['application/json'], cors=True)
def bi_insights():
    request = app.current_request
    request_data = request.json_body
    user_query = request_data.get("query", "Analyze the passenger traffic trends")

    # Fetch and process data
    df = fetch_sample_data()
    summary = df.describe().to_string()

    # Get OpenAI API key
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)

    # Call OpenAI API for insights
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that provides business intelligence insights."},
            {"role": "user", "content": f"Given this business data summary: {summary}, {user_query}"}
        ],
    )

    ai_response = response.choices[0].message.content
    return {"insights": ai_response}

# @app.lambda_function(name="openai_chat")
# def openai_chat_lambda(event, context):
#     # Extract query from event payload
#     user_query = event.get("query", "Hello, how can I help you?")

#     # Get OpenAI API key
#     api_key = get_openai_api_key()
    
#     # Create an OpenAI client (NEW API FORMAT)
#     client = OpenAI(api_key=api_key)

#     # Call OpenAI API
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": user_query}],
#     )

#     # Extract and return response
#     ai_response = response.choices[0].message.content
#     return {"response": ai_response}

