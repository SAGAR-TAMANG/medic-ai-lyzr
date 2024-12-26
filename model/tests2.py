from lyzr_agent_api.client import AgentAPI
from lyzr_agent_api.models.environment import EnvironmentConfig, FeatureConfig
from lyzr_agent_api.models.agents import AgentConfig
from lyzr_agent_api.models.chat import ChatRequest

#Initiate Lyzr Agent API Client
client = AgentAPI(x_api_key="sk-default-QisHUr8meLmfZdghTUD33VMKxvUiMOvZ")

# environment_config = EnvironmentConfig(
#        name="Test Environment",
#        features=[
#            FeatureConfig(
#                type="SHORT_TERM_MEMORY",
#                config={},
#                priority=0,
#            )
#        ],
#        tools=[],
#        llm_config={"provider": "openai",
#        "model": "gpt-4o-mini",
#        "config": {
#            "temperature": 0.5,
#            "top_p": 0.9
#        },
#        "env": {
#            "OPENAI_API_KEY": "OPENAI_API_KEY"
#        }},
#    )

# environment = client.create_environment_endpoint(json_body=environment_config)

client.get_environments_endpoint()

# response = client.chat_with_agent(
#    json_body=ChatRequest(
#        user_id="sagar.bdr0000@gmail.com",
#        agent_id="676d025fdec1ba012db54753",
#       #  session_id="676d025fdec1ba012db54753",
#        message="Hey what are you?",
#    )
# )

# import time

# if response.status_code == 429:
#   time.sleep(int(response.headers["Retry-After"]))

# print(response.text)