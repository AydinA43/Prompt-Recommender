# AI Prompt Recommender

A high-performance REST API recommendation engine built for Printee AI. This microservice analyzes a user's past image generations and intelligently recommends optimized prompts to improve AI output quality.

System Architecture
Data Ingestion: Retrieves user generation history and successful prompt data via Supabase.

Vectorization: Converts prompt text into high-dimensional vector embeddings using Sentence Transformers (all-MiniLM-L6-v2).

Similarity Search: Utilizes FAISS to perform ultra-fast similarity searches, matching the user's historical context with highly relevant new prompt structures.

Tech Stack
Backend: FastAPI, Python

Machine Learning: Sentence Transformers (Embeddings), FAISS (Vector Search)

Database: Supabase (PostgreSQL)

Deployment: Docker support coming soon

## Project Structure
```plaintext
prompt-recommender/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── recommender.py
├── index/
├── .env.example
├── requirements.txt
└── README.md

# Setup Instructions
1. Clone & Setup Environment
Bash
git clone <your-repo-url>
cd prompt-recommender
python -m venv venv

### Windows
venv\Scripts\activate
### Mac/Linux
source venv/bin/activate


2. Install Dependencies
Bash
pip install -r requirements.txt

3. Environment Variables
Copy the example environment file and add your credentials:
Bash
cp .env.example .env
Update .env with your Supabase credentials:

Code snippet
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

4. Build the Prompt Index
Before running the server, build the initial FAISS index with existing prompt data:
Python
from app.recommender import PromptRecommender

rec = PromptRecommender()

#### Fetch real prompts from Supabase or provide a list
prompts = ["A cyberpunk girl...", "Cute fox wizard..."]  

rec.build_index(prompts)

5. Run the Application
Bash
uvicorn app.main:app --reload
View the interactive Swagger documentation at: http://127.0.0.1:8000/docs

## API Endpoints:

GET / → Health check
GET /recommend/{user_id} → Retrieve personalized prompt recommendations
POST /admin/build-index → Rebuild the FAISS index with fresh Supabase data