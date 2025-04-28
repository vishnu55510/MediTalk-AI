import asyncio
import hashlib
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents import AuthorRole
from health_data_plugin import HealthDataPlugin
from pinecone_plugin import PineconeSearchPlugin
from mysql_connector_plugin import MySQLConnectorPlugin
from web_search_pluggin import WebSearchEnginePlugin

load_dotenv()


my_sql_pass = os.getenv("MY_SQL_PASS")
search_engine_id= os.getenv("SEARCH_ENGINE_ID")
search_api_key = os.getenv("SEARCH_ENGINE_API")
claude_api_key = os.getenv("ANTHROPIC_API_KEY")

Pincone = PineconeSearchPlugin()
healthdata = HealthDataPlugin()
db = MySQLConnectorPlugin("localhost", "root", my_sql_pass, "health_db")
web = WebSearchEnginePlugin(
    search_engine_id= search_engine_id,
    api_key= search_api_key
)
kernel = Kernel()

llm_service_an = AnthropicChatCompletion(
    ai_model_id="claude-3-5-sonnet-20241022",
    api_key= claude_api_key
)

health_data_collecter = ChatCompletionAgent(
    service=llm_service_an,
    name="HealthDataCollecter",
    instructions=(
    "When you are called store the information in database using `healthdata`"
    "Collect the following user health details:\n"
    "- name (str)\n"
    "- age (str)\n"
    "- gender (str)\n"
    "- treatment_history (str)\n"
    "- medication_history (str)\n"
    "- diagnosis_history (str)\n"
    "- symptoms (str)\n"
    "- allergies (str)\n\n"
    "Ask one by one if needed. Once all data is collected, call the `healthdata` plugin to store it in MySQL and Pinecone."
),
    plugins=[healthdata]
)

pinecone_search_agent = ChatCompletionAgent(
    service = llm_service_an,
    name = "PineconeSearchAgent",
    instructions=(
    "You are a Health Information Agent.\n\n"
    "Your job is to assist users with health-related questions or requests for medical advice.\n\n"
    "When the user asks about symptoms, past conditions, medications, treatments, or seeks health advice:\n"
    "- Use the `Pincone` plugin to search their personal health data stored in the vector database.\n"
    "- Pass the user's query directly to the plugin.\n"
    "- If the plugin returns a score above 0.65, return the response clearly and informatively with treatment.\n"
    "- If the score is below 0.65 generate a response based on your knowledge or perform a web search for relevant health information.\n\n"
    "Do NOT generate health advice on your own if the search score is low.\n"
    "If you need additional information, use web search `web` plugin to find reliable health-related resources.\n\n"
    "Always rely on the plugin’s response if the score is high. If the query is not health-related, politely let the user know you are focused on health-related tasks only."
),
   plugins = [Pincone, web]
)

mysql_query_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="MySQLQueryAgent",
    instructions=(
        "Fetch patient data from the `health_db.health_info` table using `db_plugin`.\n"
        "Convert user queries into SQL, execute, and return clear results."
    ),
    plugins=[db]
)

chat_history = ChatHistory()
conversation_thread = ChatHistoryAgentThread(chat_history=chat_history)

triage_agent = ChatCompletionAgent(
    service=llm_service_an,
    name="TriageAgent",
    instructions=(
        "You are a Triage Agent.\n"
        "- If user says 'register', 'add health data', or similar: trigger `HealthDataCollector`.\n"
        "- If user asks about symptoms, conditions, treatments: trigger `PineconeSearchAgent`.\n"
        "- If user asks for old records, patient info, history: trigger `MySQLQueryAgent`.\n"
        "- If unclear, ask for clarification.\n"
        "Pass the message to the right agent accordingly."
    ),
    plugins=[health_data_collecter, pinecone_search_agent, mysql_query_agent]
)


response_cache = {}

def generate_cache_key(text: str) -> str:
    """Creates a simple hash for a given text input."""
    return hashlib.sha256(text.encode()).hexdigest()

async def chat() -> bool:
    global conversation_thread
    try:
        user_input = input("\U0001F9D1‍\U0001F4BB You:> ")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        return False

    if user_input.strip().lower() == "exit":
        print("\nExiting chat...")
        return False

    # Save user message
    conversation_thread._chat_history.add_user_message(user_input)

    # Get conversation so far
    messages = conversation_thread._chat_history.messages

    # Call Triage agent
    triage_response = await triage_agent.get_response(messages=messages)

    # Save assistant response manually
    assistant_message = ChatMessageContent(
        role=AuthorRole.ASSISTANT,
        content=triage_response.message.content  # 👈 Important fix!
    )
    conversation_thread._chat_history.add_message(assistant_message)

    print(f"\n🩺 SmartHealth AI:\n{triage_response.message.content}")
    return True



async def main():
    print("Welcome to 🧠 Smart Health Navigator!")
    print("Your ONE STOP solution for healthcare, fitness, and medical research.\n")
    while await chat():
        pass

if __name__ == "__main__":
    asyncio.run(main())