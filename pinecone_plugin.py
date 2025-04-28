from semantic_kernel.functions.kernel_function_decorator import kernel_function
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
api_key = os.getenv("PINCONE_API_KEY")

class PineconeSearchPlugin:
    def __init__(self):
        self.model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key= google_api_key
        )
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index("health-info-index")

    @kernel_function(
        name="search_similar_patients",
        description="Search Pinecone for similar patients and return complete info"
    )
    def search_similar_patients_kernel(self, query_text: str, top_k: int = 3) -> str:
        try:
            query_vector = self.model.embed_query(query_text)
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_values=False,
                include_metadata=True
            )

            if not results["matches"]:
                return "❌ No similar patients found."

            # Group matches by patient_id
            patients = {}
            for match in results["matches"]:
                metadata = match.get("metadata", {})
                pid = metadata.get("patient_id", "unknown")

                if pid not in patients:
                    patients[pid] = {
                        "name": metadata.get("name", "N/A"),
                        "age": metadata.get("age", "N/A"),
                        "gender": metadata.get("gender", "N/A"),
                        "treatment_history": metadata.get("treatment_history", "N/A"),
                        "medication_history": metadata.get("medication_history", "N/A"),
                        "diagnosis_history": metadata.get("diagnosis_history", "N/A"),
                        "symptoms": metadata.get("symptoms", "N/A"),
                        "allergies": metadata.get("allergies", "N/A"),
                        "score": match["score"]
                    }

            # Format full patient info
            response = "🔍 Top Matched Patients:\n"
            for pid, info in patients.items():
                response += (
                    f"\n🆔 Patient ID: {pid}\n"
                    f"📊 Match Score: {info['score']:.3f}\n"
                    f"👤 Name: {info['name']}\n"
                    f"🎂 Age: {info['age']}\n"
                    f"⚥ Gender: {info['gender']}\n"
                    f"💊 Medication: {info['medication_history']}\n"
                    f"🏥 Diagnosis: {info['diagnosis_history']}\n"
                    f"🩺 Treatment: {info['treatment_history']}\n"
                    f"🤧 Symptoms: {info['symptoms']}\n"
                    f"⚠️ Allergies: {info['allergies']}\n"
                    f"{'-'*40}\n"
                )

            return response

        except Exception as e:
            return f"❌ Error: {str(e)}"
