import uuid
import os
import mysql.connector
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("PINCONE_API_KEY")
# --- Pinecone Initialization ---
pc = Pinecone(api_key=api_key)
index_name = "health-info-index"
# pc.delete_index("health-info-index")
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# --- Google Embedding Model Initialization ---
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key="AIzaSyA0rXUVJ-tCBxl2ia8zxb14maqB3v4NPxQ"
)

# --- Database Connection ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishnu007",
        database="health_db"
    )

# --- Store Health Info in MySQL ---
def store_health_info_mysql(name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO health_info (
        name, age, gender, treatment_history, medication_history,
        diagnosis_history, symptoms, allergies
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies))
    conn.commit()
    cursor.close()
    conn.close()

# --- Create Embedding Vectors --
# --- Vector Embeddings Creation ---
def create_category_vectors(patient_id, name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies):
    fields = {
        "symptoms": symptoms,
        "diagnosis": diagnosis_history,
        "medication": medication_history
    }

    vectors = []
    for category, content in fields.items():
        if content.strip() == "":
            continue

        vector = embedding_model.embed_query(content)
        vector_id = f"{patient_id}_{category}"
        vectors.append({
            "id": vector_id,
            "values": vector,
            "metadata": {
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "category": category,
                "text": content,
                "treatment_history": treatment_history,
                "medication_history": medication_history,
                "diagnosis_history": diagnosis_history,
                "symptoms": symptoms,
                "allergies": allergies
            }
        })

    return vectors



# --- Store Vectors in Pinecone ---
def store_vectors_in_pinecone(vectors):
    index.upsert(vectors=vectors)

# --- Pipeline Function ---
def process_and_store_health_data(name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies):
    store_health_info_mysql(name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies)

    patient_id = str(uuid.uuid4())
    vectors = create_category_vectors(patient_id, name, age, gender, treatment_history, medication_history, diagnosis_history, symptoms, allergies)
    store_vectors_in_pinecone(vectors)

    return patient_id, len(vectors)

# --- Plugin Class ---
class HealthDataPlugin:

    @kernel_function(
        description="Store user health data in MySQL and Pinecone",
        name="store_health_info"
    )
    def store_health_info_kernel(
        self,
        name: str,
        age: str,
        gender: str,
        treatment_history: str,
        medication_history: str,
        diagnosis_history: str,
        symptoms: str,
        allergies: str
    ) -> str:
        try:
            patient_id, vec_count = process_and_store_health_data(
                name, age, gender,
                treatment_history, medication_history,
                diagnosis_history, symptoms, allergies
            )
            return f"✅ Stored info for '{name}' with Patient ID: {patient_id} and {vec_count} semantic vectors."
        except Exception as e:
            return f"❌ Error: {str(e)}"
