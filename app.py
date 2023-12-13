# #fastapi[all]
# openai
# pydantic
# python-dotenv
# uvicorn app:app --host 0.0.0.0 --port 10000



from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

tools= [
    {
        "type": "function",
        "function": {
            "name": "categorizeEmail",
            "description": "Categorizes an email into a color category, and provide a reasoning, the next action, and an email draft response.",
            "parameters": {
                "type": "object",
                "properties": {                                       
                    "color": {
                        "type": "string",
                        "description": "The color that the email should be categorized as."
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "Try to explain the reasoning behind the categorization."
                    },
                    "nextAction": {
                        "type": "string",
                        "description": "Try to list the next action that should be taken."
                    },
                    "draftResponse": {
                        "type": "string",
                        "description": "Try to create a draft response to the email."
                    }
                },
                "required": ["color", "reasoning", "nextAction","draftResponse"]
            }
        }
    }
]

email = """Parker, Elaine R. (NYC x4563) Elaine.Parker@legalpartners.com Lee, Alexander ALEE@HEALTHNET.ORG; HealthPatents HealthPatents@healthnet.org; Johnson, William T. (BOS x3507) William.Johnson@legalpartners.com; Smith, Eric M. (LAX x2208) Eric.Smith@legalpartners.com; Bailey, Thomas E. tebailey@medgroup.org MEDCORP 2022-190-02; Richardson; IDS Reference Request; Action Required; LegalPartners 158462.05678; (Blue); [LP-LLP-ACTIVE.FID54837216] ""U.S. Application 19/658,452
            Based on PCT/US2023/025345 filed April 18, 2023 (LegalPartners 158462.04965)
            SYSTEM AND METHOD FOR EARLY DETECTION OF DIABETES
            Filing Date - October 10, 2023
            Inventors - Alexander J. Richardson, Priya S. Kumar, and John E. Williams
            Applicant - The Medical Health Group
            MEDCORP 2022-190-02
            LegalPartners 158462.05678
            Dear Colleagues:
            In preparing an Information Disclosure Statement for the above referenced application, we were unable to obtain a copy of the following references:
            CHEN et al., """"Enhanced analysis of pancreatic islet cell imaging using novel imaging techniques (Conference Presentation)"""" May 10, 2018.
            KUMAR et al., """"High-resolution imaging of the pancreas: An innovative approach to diagnosing diabetes"""" Journal of Endocrine Research, Vol. 53, Issue 4, October 2011, 745-749.
            LEE et al., """"Machine learning algorithms for the diagnosis of early-stage diabetes,"""" 2017 Fourth International Conference on Advances in Biomedical Engineering, Toronto, Canada, 2017, pp. 1-4, doi: 10.1109/ICABE.2017.8321254.
            Please forward us a copy of the reference if you or the inventors have one available. Alternatively, with your approval, we can request our library to obtain a copy at a nominal fee.
            Finally, please be aware that an applicant for a patent has a continuous duty to disclose to the USPTO all information known to the applicant to be material to the patentability of the subject matter claimed in the application. Please let us know if you are aware of any publications or references that might be material to the patentability of this application.
            As always, please let us know if you have any questions or concerns.
            Best,
            Elaine
            legalpartners
            """

prompt = f"""Please categorize this email according to the color category rules below and provide reasoning, next actions, and if applicable, provide an email draft response. (ie. if the email is a Black email, return "Black". Or if two colors apply, categorize as "Black, Blue".): 

    Black emails:
    Notice of Application Publications, Notices of Allowance, Patent Issue Notifications, Issued Patents 

    Blue emails:
    Annuity/Maintenance Fee Payment Reminders, Application Abandonment and Case Closing Instructions 

    Green emails: Documents requiring inventor(s)/attorney signatures - Declarations, Assignments, Powers of Attorney, USPTO Notice of Assignment Recordation's, Terminal Disclaimers 

    Grey emails:
    New Application filings and related documents - Filing Receipts, Notice to File Missing Parts, Updated Filing Receipts 

    Eggplant emails:
    Invention Disclosures and Related Documents 

    Orange emails:
    Law Firm Docket Reports, Portfolio Transfer Requests and Related Documents, Inventorship Corrections and Changes, Misc. Database Update Requests, Final Office Action Notifications, In-house Attorney Prior Art Search Documents 

    Purple emails:
    Government compliance/federal funding related documents - (NIH Final Invention Statement & Certification, DoD Inventions & Subcontracts Report, LLS Disclosure Form) Post-award searches 

    Red emails:
    Prior Art Requests for Information Disclosure Statements 

    Yellow emails: No-action Patent Related Correspondence for Filing with A Specific Application - Office Actions From Preferred Law Firms

    Please provide a reasoning for your categorization


    Here is the email: {email}"""

messages = [{"role": "user", "content": prompt}]

response1 = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=messages,
    tools = tools,
    tool_choice="auto")


# print(response1)

# # # Assuming 'response1' is the object you have, we access the color and print it. 

# for choice in response1.choices:
#     if hasattr(choice, 'message') and choice.message.tool_calls:
#         for tool_call in choice.message.tool_calls:
#             if hasattr(tool_call, 'function') and tool_call.function.arguments:
#                 arguments = json.loads(tool_call.function.arguments)
#                 color = arguments.get("color", "No color found")
#                 print("The Color is:", color)




class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    prompt = f"""Please categorize this email according to the color category rules below and provide reasoning, next actions, and if applicable, provide an email draft response. (ie. if the email is a Black email, return "Black". Or if two colors apply, categorize as "Black, Blue".): 

    Black emails:
    Notice of Application Publications, Notices of Allowance, Patent Issue Notifications, Issued Patents 

    Blue emails:
    Annuity/Maintenance Fee Payment Reminders, Application Abandonment and Case Closing Instructions 

    Green emails: Documents requiring inventor(s)/attorney signatures - Declarations, Assignments, Powers of Attorney, USPTO Notice of Assignment Recordation's, Terminal Disclaimers 

    Grey emails:
    New Application filings and related documents - Filing Receipts, Notice to File Missing Parts, Updated Filing Receipts 

    Eggplant emails:
    Invention Disclosures and Related Documents 

    Orange emails:
    Law Firm Docket Reports, Portfolio Transfer Requests and Related Documents, Inventorship Corrections and Changes, Misc. Database Update Requests, Final Office Action Notifications, In-house Attorney Prior Art Search Documents 

    Purple emails:
    Government compliance/federal funding related documents - (NIH Final Invention Statement & Certification, DoD Inventions & Subcontracts Report, LLS Disclosure Form) Post-award searches 

    Red emails:
    Prior Art Requests for Information Disclosure Statements 

    Yellow emails: No-action Patent Related Correspondence for Filing with A Specific Application - Office Actions From Preferred Law Firms

    Please provide a reasoning for your categorization


    Here is the email: {content}"""

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # Parsing and extracting the required information from the response
    try:
        tool_call_response = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call_response.function.arguments)

        color = arguments.get("color", "No color provided")
        reasoning = arguments.get("reasoning", "No reasoning provided")
        nextAction = arguments.get("nextAction", "No next action provided")
        draftResponse = arguments.get("draftResponse", "No draft response provided")

    except (IndexError, AttributeError, json.JSONDecodeError) as e:
        return {"error": f"An error occurred while processing the response: {e}"}

    # Returning the extracted values
    return {
        "color": color,
        "reasoning": reasoning,
        "nextAction": nextAction,
        "draftResponse": draftResponse
    }


