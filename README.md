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

---

## 🖼️ Screenshots

| Feature                            | Screenshot |
|------------------------------------|------------|
| Chat UI                            | ![UI](https://github.com/user-attachments/assets/364c4083-ad73-440e-9974-656310f75b13) |
| Hospital Search                    | ![Health Report](https://github.com/user-attachments/assets/65296ebd-7555-469b-b92e-ab41e46e7930) |
| Fitness and Diet Planning          | ![Fitness](https://github.com/user-attachments/assets/7e3f714b-9c97-4e92-a246-c0450c0cf7cf) |
| Medical History Retrieval          | ![Hospital](https://github.com/user-attachments/assets/df4fb2af-fa0f-4d36-a1d3-3e24d9187809) |
| Generated Health Report            | ![Screenshot 2025-04-29 201131](https://github.com/user-attachments/assets/c05137d5-2dfa-476a-a18a-02b4e6366463)
| PubMed Search Agent                | ![PubMed](https://github.com/user-attachments/assets/683a5d0e-9b35-4cf9-bf99-d9fafe078e82) |
| Health Data Collection             | ![Diet](https://github.com/user-attachments/assets/12eb469a-c8c4-4e67-8cbe-75bc79ca9b45) |
| Stored Health Data (MySQL view)    | ![DB](https://github.com/user-attachments/assets/eea700aa-88a2-4511-8942-98b5ce43d86b) |
| Agent Logs & Tool Calls            | ![Logs](https://github.com/user-attachments/assets/e86491fd-34b1-41f6-b686-f548a944360d) |


---
## 🏥 Scenario: A User’s Journey with MediTalk-AI

### 👤 Meet Riya, a 32-year-old working professional

Riya recently started experiencing recurring back pain. Being an active individual, she’s worried about her health but also wants to be proactive. She needs:
- A deeper understanding of her current health issues  
- A way to track her medical history and conditions  
- Recommendations for nearby healthcare options  
- Guidance on nutrition and fitness to alleviate her symptoms

---

### 🔹 Step 1: Riya Opens MediTalk-AI

Riya opens **MediTalk-AI** on her mobile device, and the app presents a friendly AI-powered chatbot interface. She types:

> "Hi, I’ve been having back pain lately. Can you help?"

---

### ⚙️ What Happens Behind the Scenes

The **TriageAgent** immediately processes Riya’s query and triggers the relevant agents to provide her with a personalized response.

| **Agent**                    | **Function**                                                                 |
|-----------------------------|------------------------------------------------------------------------------|
| `HealthDataCollectorAgent`  | Collects new symptoms and stores them in MySQL and Pinecone                   |
| `HealthReportGeneratorAgent`| Retrieves her medical history, including previous treatments, surgeries, and medications |
| `HospitalSearchAgent`       | Uses Riya's location and searches for nearby hospitals using SerpApi           |
| `PubMedSearchAgent`         | Retrieves the latest medical research articles on back pain treatment         |
| `DietAgent`                 | Recommends meal plans rich in anti-inflammatory foods                         |
| `FitnessAgent`              | Suggests beginner-friendly exercises to help alleviate back pain              |

---

### 🧾 Step 2: Riya Receives Personalized Health Insights

After a brief pause, **MediTalk-AI** presents Riya with a comprehensive response:
- A summary of her medical history from MySQL and Pinecone, highlighting her past injuries and medications related to back pain  
- A list of hospitals and clinics specializing in orthopedic care, with options to view their ratings, location, and specialties  
- A curated list of recent research articles from PubMed detailing the latest advancements in back pain treatments and preventive care  
- A personalized 7-day anti-inflammatory meal plan based on Riya’s dietary preferences and needs  
- A customized fitness routine, including stretching exercises, posture correction, and gentle back exercises designed to relieve pain

---

### 💬 Step 3: Riya Continues the Interaction

Riya follows up with another question:

> "Can you help me find the best hospital for back pain treatment?"

The system uses the **HospitalSearchAgent** to show hospitals ranked by their specialization in back pain treatments and proximity to Riya's location. MediTalk-AI lists:
- **Hospital A**: Specializes in spine surgery and physiotherapy. Ratings: 4.8/5
- **Hospital B**: Known for its holistic pain management treatments. Ratings: 4.5/5
- **Hospital C**: Features an in-house orthopedic specialist. Ratings: 4.3/5

Riya can click on any of the hospitals to get further details or directions.

---

### 🔄 Step 4: Riya Asks for Further Details

She decides to learn more about one of the hospitals and types:

> "Tell me more about Hospital A and their spine surgery department."

The system pulls detailed information from the **HospitalSearchAgent**, displaying:
- A description of the hospital’s facilities  
- A list of spine surgeons with their qualifications and experience  
- Patient reviews specific to spine surgeries  
- Contact details and the option to book an appointment (though appointment booking is not yet automated)

---

### 🔍 Step 5: Searching for Research Articles

Riya is also curious about recent research on back pain treatments, so she asks:

> "What’s the latest research on treating chronic back pain?"

The **PubMedSearchAgent** retrieves several relevant articles:
- **Article 1**: "Efficacy of Non-Surgical Treatments for Chronic Back Pain"  
- **Article 2**: "Exploring the Role of Posture in Back Pain Relief"  
- **Article 3**: "Advancements in Minimally Invasive Spine Surgery"  

Riya can click on any of the articles to get summaries or even full access if available, helping her stay informed.

---

### ✅ Outcome

By the end of the session, Riya has:
- Gained a detailed understanding of her health, including the possible causes of her back pain  
- Accessed a comprehensive list of nearby hospitals specializing in orthopedic care  
- Reviewed the latest evidence-based research on back pain treatments  
- Received a personalized diet plan and fitness routine to help alleviate her symptoms  
- Explored useful health resources tailored to her specific condition

---

## 🤝 Who Benefits from MediTalk-AI?

### 1. **Individuals with Health Concerns**
   - **Example**: Riya, who is experiencing back pain, benefits from personalized insights, treatment suggestions, and local healthcare provider recommendations.

### 2. **Patients with Chronic Conditions**
   - **Example**: Users with conditions like diabetes or hypertension can track health data, receive reports, and access specialized healthcare providers.

### 3. **Health-conscious Individuals**
   - **Example**: Users seeking fitness or nutrition advice get personalized meal plans, workout routines, and general health guidance.

### 4. **Healthcare Providers**
   - **Benefit**: Medical professionals can utilize the platform to stay updated on the latest research and offer more informed care options based on patient data and needs.

### 5. **Researchers**
   - **Benefit**: Researchers can use the PubMed search functionality to find relevant studies and research papers on health topics, enhancing their work and knowledge.


### 📝 Prerequisites

Ensure the following are installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
