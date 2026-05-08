import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.vector_store import vector_store

docs = [
    {
        "id": "gdpr_art5",
        "content": "GDPR Article 5: Personal data must be processed lawfully, fairly, and transparently. It must be collected for specified, explicit, and legitimate purposes and not further processed in a manner that is incompatible with those purposes.",
        "metadata": {"topic": "GDPR", "type": "Regulation"}
    },
    {
        "id": "gdpr_art25",
        "content": "GDPR Article 25: Data protection by design and by default requires controllers to implement appropriate technical and organizational measures to protect data rights from the outset.",
        "metadata": {"topic": "Privacy by Design", "type": "Regulation"}
    },
    {
        "id": "ccpa_rights",
        "content": "CCPA: Consumers have the right to know what personal information is collected, used, shared, or sold, and the right to delete personal information held by businesses.",
        "metadata": {"topic": "CCPA", "type": "Regulation"}
    },
    {
        "id": "data_minimization",
        "content": "Data Minimization Principle: Organizations should only collect and process personal data that is adequate, relevant, and limited to what is necessary in relation to the purposes for which they are processed.",
        "metadata": {"topic": "Data Minimization", "type": "Best Practice"}
    },
    {
        "id": "encryption_std",
        "content": "Encryption Standards: Personal data should be encrypted using strong algorithms like AES-256 at rest and TLS 1.3 in transit to ensure confidentiality and integrity.",
        "metadata": {"topic": "Security", "type": "Technical Standard"}
    },
    {
        "id": "anonymization",
        "content": "Anonymization vs Pseudonymization: Anonymization is irreversible, making the data no longer personal data. Pseudonymization replaces identifiers with artificial identifiers, but allows re-identification with additional information.",
        "metadata": {"topic": "Data De-identification", "type": "Definition"}
    },
    {
        "id": "retention_policy",
        "content": "Data Retention: Personal data should not be kept longer than necessary for the purposes for which it was collected. Clear retention schedules and secure deletion processes must be implemented.",
        "metadata": {"topic": "Retention", "type": "Best Practice"}
    },
    {
        "id": "privacy_by_design",
        "content": "Privacy by Design: Proactive not reactive; Preventative not remedial. Privacy should be embedded into the design and architecture of IT systems and business practices.",
        "metadata": {"topic": "Privacy by Design", "type": "Foundational Principle"}
    },
    {
        "id": "dpia_requirement",
        "content": "DPIA (Privacy Impact Assessment): Required for processing likely to result in high risk to individuals, particularly when using new technologies or processing sensitive data on a large scale.",
        "metadata": {"topic": "DPIA", "type": "Requirement"}
    },
    {
        "id": "purpose_limitation",
        "content": "Purpose Limitation: Personal data must be collected for specific, explicit, and legitimate purposes and not used for anything else without further legal basis or consent.",
        "metadata": {"topic": "GDPR", "type": "Principle"}
    }
]

def seed():
    print("Seeding ChromaDB with domain knowledge...")
    documents = [d["content"] for d in docs]
    metadatas = [d["metadata"] for d in docs]
    ids = [d["id"] for d in docs]
    
    vector_store.add_documents(documents, metadatas, ids)
    print("✅ Successfully seeded 10 documents.")

if __name__ == "__main__":
    seed()
