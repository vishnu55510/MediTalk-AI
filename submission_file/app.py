import asyncio
import os
import chainlit as cl
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion  # Correct: Using OpenAI, not Anthropic

# Plugins
from health_data_plugin import HealthDataPlugin
from pinecone_plugin import PineconeSearchPlugin
from mysql_connector_plugin import MySQLConnectorPlugin
from web_search_pluggin import WebSearchEnginePlugin
from location_plugin import LocationAgentPlugin
from pubmed_plugin import PubMedPlugin  # Ensure correctly implemented
from SerpApiLocationSearchPlugin import SerpApiLocationSearchPlugin
# ----------------- Load environment variables -----------------
load_dotenv()

my_sql_pass = os.getenv("MY_SQL_PASS")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")
search_api_key = os.getenv("SEARCH_ENGINE_API")
openai_api_key = os.getenv("OPEN_API_KEY")  # Correct: rename from claude_api_key to openai_api_key
serp_api_key = os.getenv("SERP_API_KEY")
# ----------------- Plugin Setup -----------------
pinecone_plugin = PineconeSearchPlugin()
health_data_plugin = HealthDataPlugin()
mysql_plugin = MySQLConnectorPlugin(host="localhost", user="root", password=my_sql_pass, database="health_db")
web_search_plugin = WebSearchEnginePlugin(search_engine_id=search_engine_id, api_key=search_api_key)
location_plugin = LocationAgentPlugin()
pubmed_plugin = PubMedPlugin()
serp_api_location_search_plugin = SerpApiLocationSearchPlugin(api_key=serp_api_key)
# ----------------- Kernel Setup -----------------
kernel = Kernel()

# ----------------- LLM Service (OpenAI) -----------------
llm_service = OpenAIChatCompletion(
    ai_model_id="gpt-4.1-mini",
    api_key=openai_api_key
)

# ----------------- Agents Setup -----------------
health_data_collector = ChatCompletionAgent(
    service=llm_service,
    name="HealthDataCollector",
    instructions="""
You are HealthDataCollector. Your task is to collect user health data and store it in MySQL table `health_info` and Pinecone.
Collect the following fields:
- id, name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies, created_at
Use the `health_data_plugin` to gather the data and store it in both MySQL (structured) and Pinecone (vectorized).
""",
    plugins=[health_data_plugin]
)

pinecone_search_agent = ChatCompletionAgent(
    service=llm_service,
    name="PineconeSearchAgent",
    instructions="Assist users with health-related questions using Pinecone for personal data.",
    plugins=[pinecone_plugin, web_search_plugin]
)

health_report_agent = ChatCompletionAgent(
    service=llm_service,
    name="HealthReportAgent",
    instructions=(
        "You are a professional Report Generater. "
        "Your task is to fetch the patient's all previous medical history from MySQL database table name `health_info` and use `pinecone_plugin` to search in Vecter database and generate a detailed report, "
        "Fields: id, name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies, created_at. "
        "well-organized health report including conditions, treatments, medications, surgeries, and important notes."
    ),
    plugins=[mysql_plugin, pinecone_plugin]
)

mysql_query_agent = ChatCompletionAgent(
    service=llm_service,
    name="MySQLQueryAgent",
    instructions=(
        "Use the `mysql_plugin` to query the `health_info` table. "
        "Fields: id, name, age, gender, treatment_history, medication_history, "
        "diagnosis_history, symptoms, allergies, created_at. "
        "Respond with relevant patient data based on the user query."
    ),
    plugins=[mysql_plugin]
)

# location_agent = ChatCompletionAgent(
#     service=llm_service,
#     name="LocationAgent",
#     instructions="Help retrieve the user's location using the Location plugin.",
#     plugins=[location_plugin]
# )

hospital_search_agent = ChatCompletionAgent(
    service=llm_service,
    name="HospitalSearchAgent",
    instructions="Utilize the `serp_api_location_search_plugin` to search for hospitals based on the provided location. Retrieve and provide the relevant hospital details along with their location"
    "Steps:1. Use `location_plugin` to detect or confirm the user’s location.2. Use `serp_api_location_search_plugin` to find hospitals matching the required specialization and location.3. Return a list of hospitals with: Name, Address, Specialization (if available), and Contact/Website.",
    plugins=[serp_api_location_search_plugin, location_plugin]
)


pubmed_search_agent = ChatCompletionAgent(
    service=llm_service,
    name="PubMedSearchAgent",
    instructions="Assist users by finding relevant medical research from PubMed.",
    plugins=[pubmed_plugin]
)

diet_agent = ChatCompletionAgent(
    service=llm_service,
    name="DietAgent",
    instructions="You are a diet planner. Create a daily meal plan based on the user's dietary needs."
)

fitness_agent = ChatCompletionAgent(
    service=llm_service,
    name="FitnessAgent",
    instructions="You are a fitness coach. Create a customized workout plan based on the user's fitness goals."
)

triage_agent = ChatCompletionAgent(
    service=llm_service,
    name="TriageAgent",
    instructions="Detect the user's intent and coordinate with other agents to fulfill their needs.",
    plugins=[
        hospital_search_agent,
        pubmed_search_agent,
        diet_agent,
        fitness_agent,
        pinecone_search_agent,
        health_data_collector,
        mysql_query_agent,
        health_report_agent
    ]
)

# ----------------- Conversation History -----------------
chat_history = ChatHistory()
conversation_thread = ChatHistoryAgentThread(chat_history=chat_history)

# ----------------- Chainlit Event Handlers -----------------
@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content.strip()

    if user_input.lower() == "exit":
        await cl.Message(content="Exiting chat... 🛑").send()
        return

    # Add message to chat history
    conversation_thread._chat_history.add_user_message(user_input)

    # Get full chat history as message list
    full_conversation = conversation_thread._chat_history.messages

    # Pass full history to the triage agent
    triage_response = await triage_agent.get_response(messages=full_conversation)

    # Add agent response to history
    conversation_thread._chat_history.add_assistant_message(triage_response.message.content)

    # Send response back to UI
    await cl.Message(content=f"🩺 MediTalk-AI: {triage_response.message.content}").send()


@cl.on_chat_start
async def on_chat_start():
    global conversation_thread
    conversation_thread = ChatHistoryAgentThread(chat_history=ChatHistory())
    await cl.Message(content="👋 Welcome to 🧠 MediTalk-AI!").send()


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Welcome to 🧠 MediTalk-AI!").send()

# ----------------- Main Entry Point -----------------
if __name__ == "__main__":
    cl.run()
