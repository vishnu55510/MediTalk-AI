import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion 
from dotenv import load_dotenv
load_dotenv()
# Plugins
from location_plugin import LocationAgentPlugin
from mysql_connector_plugin import MySQLConnectorPlugin
from web_search_pluggin import WebSearchEnginePlugin
from pubmed_plugin import PubMedPlugin  # Ensure this is implemented correctly

my_sql_pass = os.getenv("MY_SQL_PASS")
search_engine_id= os.getenv("SEARCH_ENGINE_ID")
search_api_key = os.getenv("SEARCH_ENGINE_API")
claude_api_key = os.getenv("ANTHROPIC_API_KEY")

# Plugin setup
Location = LocationAgentPlugin()
db = MySQLConnectorPlugin("localhost", "root", my_sql_pass, "doc_app")
web = WebSearchEnginePlugin(
    search_engine_id= search_engine_id,
    api_key= search_api_key
)
pubmed = PubMedPlugin()

# Kernel setup
kernel = Kernel()

# LLM service
llm_service_an = OpenAIChatCompletion(
    ai_model_id="gpt-4.1-mini",
    api_key=openai_api_key
)

# --------------------------
# Define all Agents
# --------------------------

Location_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="LocationAgent",
    instructions=(
        "You help retrieve the user's location using the Location plugin.\n"
        "If plugin fails or information is insufficient, ask the user directly.\n"
        "Return the city and country in a readable format."
    ),
    plugins=[Location]
)

hospital_search_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="HospitalSearchAgent",
    instructions=(
        "Use the WebSearch plugin to find hospitals or clinics in the provided location.\n"
        "List the hospital name, address, and website link (if available).\n"
        "If user is looking to book an appointment, guide them to the Booking Agent.\n"
        "Be brief and informative."
    ),
    plugins=[web]
)

pubmed_search_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="PubmedSearchAgent",
    instructions=(
        "You assist users by finding relevant medical research from PubMed.\n"
        "Use the PubMed plugin (`esearch`, `efetch`) to:\n"
        "1. Search using the user's medical query.\n"
        "2. Fetch the top articles' titles, abstracts, and PubMed links.\n"
        "3. Return each article with a brief summary and a link to the article on PubMed.\n\n"
        "Return the information in this format:\n"
        "• Title\n   Abstract (2–3 lines)\n  Link\n\n"),
    plugins=[pubmed]
)



diet_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="DietAgent",
    instructions=(
        "You are a diet planner.\n"
        "Create a daily meal plan based on the user's dietary restrictions, allergies, or fitness goals.\n"
        "Include meals for breakfast, lunch, dinner, and snacks.\n"
        "Give a short reason why this meal plan suits the user's goals."
    )
)

fitness_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="FitnessAgent",
    instructions=(
        "You are a fitness coach.\n"
        "Create a customized workout plan with warm-up, core exercises, and cool-down stretches.\n"
        "Tailor the plan to user's goals like weight loss, muscle gain, or endurance.\n"
        "Keep it detailed and easy to follow."
    )
)

triage_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="TriageAgent",
    instructions=(
        "You are the main assistant managing the SmartHealth conversation.\n\n"
        "Detect the user's intent: Book Appointment, Search Hospital, Get Fitness Plan, Diet Advice, or Research Medical Info.\n"
        "Use LocationAgent to get user's location if needed.\n"
        "Use HospitalSearchAgent to get hospital suggestions.\n"
        "Use PubmedSearchAgent for medical literature.\n"
        "Use DietAgent or FitnessAgent when the user mentions food, exercise, fitness or health goals.\n\n"
        "Coordinate all agents smoothly and keep the chat friendly and helpful."
    ),
    plugins=[hospital_search_agent, Location_agent, pubmed_search_agent, diet_agent, fitness_agent]
)

# --------------------------
# Chat history (shared across all agents)
# --------------------------
chat_history = ChatHistory()
thread = ChatHistoryAgentThread(chat_history=chat_history)

# --------------------------
# Chat loop
# --------------------------
async def chat() -> bool:
    global thread
    try:
        user_input = input("\U0001F9D1‍\U0001F4BB You:> ")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        return False

    if user_input.strip().lower() == "exit":
        print("\nExiting chat...")
        return False

    # Triage agent handles input and calls other agents via plugins
    triage_response = await triage_agent.get_response(messages=user_input, thread=thread)
    print(f"\n🩺 SmartHealth AI:\n{triage_response}")
    return True

# --------------------------
# Main async runner
# --------------------------
async def main():
    print("Welcome to 🧠 MediTalk-AI!")
    print("Your ONE STOP solution for healthcare, diet, fitness, and research.\n")
    while await chat():
        pass

if __name__ == "__main__":
    asyncio.run(main())
