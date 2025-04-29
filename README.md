# MediTalk-AI - README

## Overview

MediTalk-AI is an advanced AI-powered health assistant application that helps users manage their health-related queries. This application integrates multiple agents, including health data collection, medical history retrieval, fitness planning, and hospital search, among others. It leverages cutting-edge AI technologies like OpenAI GPT and plugins for accessing health-related data, such as Pinecone, MySQL, PubMed, and various location and web search APIs.

The goal of MediTalk-AI is to provide users with a comprehensive platform to track health information, receive personalized reports, get fitness and diet advice, and find relevant medical research. It also includes intelligent agents that work together to facilitate user requests, offering a seamless and interactive experience.

---

## Features

1. **Health Data Collection**: Collects and stores user health information in both MySQL and Pinecone.
2. **Medical History Retrieval**: Fetches detailed reports from the health database, including conditions, treatments, medications, and surgeries.
3. **Personalized Health Report Generation**: Generates detailed reports based on user health data, integrating information from MySQL and Pinecone.
4. **Hospital Search**: Allows users to search for hospitals based on their location using a location-based plugin.
5. **Diet Planning**: Provides users with customized daily meal plans based on their dietary needs.
6. **Fitness Planning**: Offers personalized workout plans based on fitness goals.
7. **Medical Research Search**: Helps users search for relevant medical research from PubMed.
8. **Multi-Agent System**: Uses a coordination agent (TriageAgent) that interacts with various specialized agents to fulfill user requests.
9. **AI-Powered Conversation**: Powered by OpenAI GPT-4 for conversational AI capabilities.

---

## Tech Stack

- **Backend**: 
    - **Python** (for AI agents and plugins)
    - **OpenAI GPT-4** (for conversational AI)
    - **Semantic Kernel** (for agent orchestration)
    - **Pinecone** (for vector-based search and storage)
    - **MySQL** (for structured data storage)
    - **Chainlit** (for interactive UI and user messaging)
    - **dotenv** (for loading environment variables)

- **Plugins**:
    - **HealthDataPlugin**: Collects and stores health data.
    - **PineconeSearchPlugin**: Searches user data in the Pinecone vector store.
    - **MySQLConnectorPlugin**: Retrieves data from MySQL database.
    - **WebSearchEnginePlugin**: Performs web searches to find health-related information.
    - **LocationAgentPlugin**: Helps with location-based services (e.g., finding hospitals).
    - **PubMedPlugin**: Searches for medical research on PubMed.
    - **SerpApiLocationSearchPlugin**: Utilizes SerpApi for location-based search, specifically for hospitals.

---
![MIcrosoft hackathon acrhitecture diagram drawio](https://github.com/user-attachments/assets/33ad7a4f-eef8-450a-9d6b-69b949a0c002)
![MIcrosoft hackathon acrhitecture diagram drawio (1)](https://github.com/user-attachments/assets/a9fb88ad-a64d-4ed5-8edb-976574c66a4a)

## Usage

Upon starting the application, you will be greeted with an interactive AI chatbot interface. You can enter various health-related queries, and the system will process the request using the following agents:

1. **Health Data Collector**: Collects and stores user health data in MySQL and Pinecone.
2. **Health Report Generator**: Fetches previous medical history and generates a detailed health report, including conditions, treatments, medications, surgeries, and important notes.
3. **Hospital Search Agent**: Finds hospitals based on user location using the SerpApi Location Search plugin.
4. **Diet Agent**: Creates personalized daily meal plans based on the user's dietary needs.
5. **Fitness Agent**: Generates customized workout plans for users based on their fitness goals.
6. **PubMed Search Agent**: Searches for medical research papers and articles on PubMed to provide users with relevant health information.

The **TriageAgent** coordinates the flow of user queries between agents, ensuring that the appropriate responses are provided. It orchestrates the different agents based on the user's request, ensuring seamless interactions with the system.

---



## Setup & Installation

### Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- `pip` (Python package installer)
- Virtual environment (optional but recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/meditalk-ai.git
cd meditalk-ai
