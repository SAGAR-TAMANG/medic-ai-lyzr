import requests

agent_id = "676d025fdec1ba012db54753"

url = f"https://agent-prod.studio.lyzr.ai//v3/inference/chat/"
headers = {"Content-Type": "application/json", "x-api-key" : "sk-default-QisHUr8meLmfZdghTUD33VMKxvUiMOvZ"}
data = {
  "user_id": "sagar.bdr0000@gmail.com",
  "agent_id": "676d025fdec1ba012db54753",
  "session_id": "676d025fdec1ba012db54753",
  "message": "heyy"
}
response = requests.post(url, headers=headers, json=data)

if response.status_code == 422:
    print(response.json())
    print(response.content.response)
else:
    print(f"Error: {response.status_code} - {response.text}")
    response_data = response.json()
    print(response_data.get('response', ''))
    print(response.json())
