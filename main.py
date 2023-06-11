import subprocess
import openai
import urllib.parse
import os

openai.api_key = "" # Key is ignored and does not matter
openai.api_base = "http://34.132.127.197:8000/v1"


# Report issues
def raise_issue(e, model, prompt):
    issue_title = urllib.parse.quote("[bug] Hosted Gorilla: <Issue>")
    issue_body = urllib.parse.quote(f"Exception: {e}\nFailed model: {model}, for prompt: {prompt}")
    issue_url = f"https://github.com/ShishirPatil/gorilla/issues/new?assignees=&labels=hosted-gorilla&projects=&template=hosted-gorilla-.md&title={issue_title}&body={issue_body}"
    print(f"An exception has occurred: {e} \nPlease raise an issue here: {issue_url}")

# Query Gorilla server 
def get_gorilla_response(prompt="I would like to translate from English to French.", model="gorilla-7b-hf-v0"):
  try:
    completion = openai.ChatCompletion.create(
      model=model,
      messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
  except Exception as e:
    raise_issue(e, model, prompt)

def generate(prompt):
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role":"system", "content": "You generate only python code and comment all normal text."},
        {"role": "user", "content": prompt},
        ],
        temperature = 0.2
    )

    return completion.choices[0].message["content"]

prompt = input("What do you want to do?\n")

instructions = get_gorilla_response(prompt)
print(instructions)

openai.api_key = "ENTER KEY HERE" or os.getenv("OPENAI_API_KEY")
openai.api_base = "https://api.openai.com/v1"

code = generate(f"The user wants to {prompt}. Write code to do this following the instructions. What you output will be ran for the user so make sure its python formatting:\n\n" + str(instructions) + "\n\Code in python format: ")
code = code.replace("`", "").replace("python", "")

with open('file.py', 'w') as f:
   f.write(code)

subprocess.call(["python", "file.py"])
