# 🧠 MediTalk-AI

## 📘 Overview

**MediTalk-AI** is an advanced AI-powered health assistant application that allows users to manage health-related activities through intelligent conversations. It integrates multiple autonomous agents to handle tasks like collecting health data, generating reports, planning fitness and diets, searching for hospitals, and accessing medical research.

This platform leverages cutting-edge technologies such as **OpenAI GPT-4**, **Semantic Kernel**, **MySQL**, **Pinecone**, **Chainlit**, and **PubMed**.

---

## ✨ Features

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 🗂️ Health Data Collection      | Stores health info in MySQL and Pinecone                                    |
| 📄 Medical History Retrieval   | Retrieves conditions, treatments, medications, and surgeries                |
| 📊 Personalized Reports        | Combines data from MySQL & Pinecone to generate summaries                   |
| 🏥 Hospital Search             | Finds hospitals based on user location                                      |
| 🥗 Diet Planning               | Provides daily meal plans tailored to user needs                            |
| 🏋️ Fitness Planning            | Custom workouts based on goals                                              |
| 🔍 PubMed Research Search      | Finds medical articles using PubMed                                         |
| 🤖 Multi-Agent Coordination    | Uses TriageAgent to delegate to specialized agents                          |
| 💬 Conversational AI           | GPT-4 powered natural interaction                                           |

---

## 🧰 Tech Stack

### 💻 Backend

- **Python**
- **OpenAI GPT-4**
- **Semantic Kernel**
- **MySQL**
- **Pinecone**
- **Chainlit**
- **dotenv**

### 🔌 Plugins

| Plugin                        | Purpose                                                         |
|------------------------------|-----------------------------------------------------------------|
| `HealthDataPlugin`           | Collects and stores user health data                           |
| `PineconeSearchPlugin`       | Vector-based health data search                                |
| `MySQLConnectorPlugin`       | Retrieves structured data                                      |
| `WebSearchEnginePlugin`      | Finds health information online                                |
| `LocationAgentPlugin`        | Helps with hospital/location services                          |
| `PubMedPlugin`               | Fetches articles from PubMed                                   |
| `SerpApiLocationSearchPlugin`| Uses SerpApi to search for hospitals                           |

---

## 🧠 Architecture Diagram

![Architecture Diagram](https://github.com/user-attachments/assets/33ad7a4f-eef8-450a-9d6b-69b949a0c002)

---

## 🚀 Usage

Once launched, users interact via a conversational interface. The **TriageAgent** coordinates other agents to fulfill user queries:

| Agent                     | Functionality                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| `Health Data Collector`   | Captures and stores user data into MySQL and Pinecone                        |
| `Health Report Generator` | Produces summaries of past treatments, conditions, and health history        |
| `Hospital Search Agent`   | Finds nearby hospitals using SerpApi and location plugin                     |
| `Diet Agent`              | Plans meals based on user dietary needs                                      |
| `Fitness Agent`           | Generates workout plans aligned to health goals                              |
| `PubMed Search Agent`     | Searches PubMed for related medical research articles                        |

---

## 🖼️ Screenshots

| Feature                            | Screenshot |
|------------------------------------|------------|
| Chat UI                            | ![UI](https://github.com/user-attachments/assets/364c4083-ad73-440e-9974-656310f75b13) |
| Generated Health Report            | ![Health Report](https://github.com/user-attachments/assets/65296ebd-7555-469b-b92e-ab41e46e7930) |
| Fitness and Diet Planning          | ![Fitness](https://github.com/user-attachments/assets/7e3f714b-9c97-4e92-a246-c0450c0cf7cf) |
| Hospital Search Result             | ![Hospital](https://github.com/user-attachments/assets/df4fb2af-fa0f-4d36-a1d3-3e24d9187809) |
| PubMed Search Agent                | ![PubMed](https://github.com/user-attachments/assets/683a5d0e-9b35-4cf9-bf99-d9fafe078e82) |
| Personalized Meal Plan             | ![Diet](https://github.com/user-attachments/assets/12eb469a-c8c4-4e67-8cbe-75bc79ca9b45) |
| Stored Health Data (MySQL view)    | ![DB](https://github.com/user-attachments/assets/eea700aa-88a2-4511-8942-98b5ce43d86b) |
| Agent Logs & Tool Calls            | ![Logs](https://github.com/user-attachments/assets/e86491fd-34b1-41f6-b686-f548a944360d) |

---

## ⚙️ Setup & Installation

### 📝 Prerequisites

Ensure the following are installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
