# Emotional Wellness Chatbot

An AI-powered emotional wellness chatbot that converses naturally like a friend while analyzing emotional states using the clinically validated PHQ-9 framework.

## Features
- Natural conversational interface powered by Qwen2.5-72B via Hugging Face
- PHQ-9 based emotional state classification using fine-tuned BERT
- Crisis detection with immediate helpline resources
- Automatic wellness suggestions based on emotional patterns
- 14-day rolling emotional trend tracking via MySQL

## Architecture
User Message
│
▼
Crisis Check (keyword + LLM context verification)
│
▼
Chatbot Reply (Qwen2.5-72B)
│
▼
BERT Classifier (fine-tuned on GoEmotions → PHQ-9)
│
▼
MySQL Storage + Aggregator
│
▼
Risk Scorer → Resource Suggestion
## Tech Stack
- **LLM**: Qwen2.5-72B-Instruct via Hugging Face Inference API
- **Classifier**: BERT fine-tuned on GoEmotions dataset mapped to PHQ-9 categories
- **Backend**: FastAPI + SQLAlchemy + MySQL
- **Frontend**: Streamlit
- **Framework**: PHQ-9 (Patient Health Questionnaire)

## Setup

1. Clone the repo

2. Create virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```
3. Create `.env` file:
HUGGINGFACE_TOKEN=your_token_here

4. Create MySQL database:
```sql
CREATE DATABASE emotions_db;
```
5. Run backend:
```bash
cd backend
uvicorn api:app --reload
```
6. Run frontend:
```bash
streamlit run app.py
```

## Disclaimer
This tool provides emotional support and risk signals only. It is not a substitute for professional mental health diagnosis or treatment.

## Crisis Resources (India)
- iCall: 9152987821
- Vandrevala Foundation: 1860-2662-345
- AASRA: 91-22-27546669

## Future Development

### User Profile System
- Secure login and registration with auto-generated unique user IDs
- Profile collection on signup: name, age group, gender
- Per-user session history stored and linked to profile
- Suggestions personalized based on age group and gender (e.g. different coping resources for teenagers vs adults)
- Conversation history summarized and injected into chatbot context for continuity across sessions

### Personalized Intelligence
- Long-term emotional trend analysis per user (weekly/monthly reports)
- Chatbot adapts tone and suggestions based on user profile and past patterns
- Resource recommendations weighted by what has worked for similar profiles

### Security and Data Protection
- Password hashing using bcrypt
- JWT-based authentication for all API endpoints
- AES-256 encryption for all stored messages and emotional data at rest
- HTTPS enforcement in production
- Role-based access control (user vs admin)
- Automatic session expiry and token refresh
- Rate limiting on all endpoints to prevent abuse
- GDPR-compliant data deletion — users can request full data wipe
- Audit logs for all data access events
- No plaintext sensitive data stored anywhere in the system