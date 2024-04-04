import os
import json
from dotenv import load_dotenv

from openai import OpenAI

from src import config as C

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_from_single_content(content):

    system_prompt = '''
            Your role involves processing and analyzing markdown data extracted from various web pages of a company. Your primary task is to parse this markdown data and organize it into a structured JSON format that categorizes information into specified fields.

            Required Output: The output should be a JSON object that encapsulates detailed information about the company. The JSON structure should adhere to the following schema, with specific fields populated by the data extracted from the markdown content. If certain information is not available within the provided markdown, please use "Not Provided" as the value for those fields.

            {
                "Organization Name": "Name of the Company",
                "Website URL": "https://www.example.com",
                "Logo URL": "https://www.example.com/logo.png",
                "Employee Count": 100,
                "Domain Name": "example.com",
                "Industry Type": "Industry Sector",
                "Geography Served": ["List", "Of", "Geographies"],
                "Business Model": "Type of Business Model",
                "Types Of Clients": ["Client Type 1", "Client Type 2"],
                "Contact Email": "contact@example.com",
                "Social Media Profiles": {
                    "LinkedIn": "LinkedIn URL",
                    "Twitter": "Twitter URL",
                    "Facebook": "Facebook URL"
                },
                "Address": "Company Address",
                "Revenue Estimate": "Annual Revenue",
                "OrganisationCreationDate": "YYYY-MM-DD",
                "Description": "Brief description of the company, its mission, and core values.",
                "Notes": "Any additional notes or important information to be highlighted."
            }

            Fields Explained:
            Organization Name: The legal name of the company.
            Website URL: The official website URL.
            Logo URL: Direct URL to the company's logo.
            Employee Count: Total number of employees.
            Domain Name: Internet domain name.
            Industry Type: Sector or industry the company operates in.
            Geography Served: List of geographic regions where services are offered.
            Business Model: The company's approach to generating revenue.
            Types Of Clients: Categories of clients served.
            Contact Email: Primary contact email address.
            Social Media Profiles: URLs to the company's social media profiles.
            Address: Physical address of the company's headquarters.
            Revenue Estimate: An estimate of the company's annual revenue.
            OrganisationCreationDate: The date the company was founded.
            Description: A detailed description of the company's business, objectives, and unique selling propositions.
            Notes: Additional relevant information or context about the company.

    '''

    user_prompt = f'''

          Carefully review the markdown data provided below. Extract relevant information and populate the JSON schema accordingly. Ensure accuracy and completeness to the best of your ability, and use "Not Provided" for any missing details.

          <content>
          {content}
          </content>
    '''

    # Create the conversation messages with the system prompt and the user query
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = client.chat.completions.create(
        model=C.OPENAI_MODEL,
        response_format={ "type": "json_object" },
        messages=messages
        )
    
    # Extract the response content
    response_content = response.choices[0].message.content
    # Remove the markdown code block notation and leading/trailing backticks
    cleaned_response = response_content.replace("```json", "").replace("```", "").strip()

    # Attempt to parse the cleaned response as JSON
    try:
        response_json = json.loads(cleaned_response)
        # print(json.dumps(response_json, indent=4))
        return response_json
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None
    

def extract_from_more_content(content, response):
    # Placeholder for actual implementation
    # This should process additional content segments and return a response
    return f"Processed additional segment: {len(content.split())} tokens"

def extract_contents(content_segments):
    responses = {}
    
    if len(content_segments) == 1:
        # If there's only one segment, process it with extract_from_single_content
        response = extract_from_single_content(content_segments[0])
    elif len(content_segments) > 1:
        # If there are multiple segments, process the first with extract_from_single_content
        response = extract_from_single_content(content_segments[0])
        
        # Process the rest of the segments with extract_from_more_content iteratively
        for segment in content_segments[1:]:
            response = extract_from_more_content(segment, response)
    
    return responses