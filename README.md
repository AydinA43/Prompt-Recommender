# AI Prompt Recommender

A **FastAPI** recommendation system for AI image generation prompts. It learns from a user's past generations stored in **Supabase** and recommends better prompts using **sentence embeddings** + **FAISS**.

Perfect portfolio project showcasing: FastAPI, Supabase, embeddings (ML), and clean project structure.

## Features

- Personalized prompt recommendations based on user history
- Fast similarity search with FAISS
- Clean REST API with Swagger docs
- Easy to extend with S3 image analysis later

## Tech Stack

- **Backend**: FastAPI
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Search**: FAISS
- **Database**: Supabase
- **Deployment Ready**: Docker support coming soon

## Project Structure
prompt-recommender/
├── app/
│   ├── init.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── recommender.py
├── index/                 
├── .env                   
├── requirements.txt
├── README.md

## Setup Instructions

1. Clone & Setup

```bash
git clone <your-repo-url>
cd prompt-recommender
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

2. Install Dependencies
Bashpip install -r requirements.txt

3. Environment Variables
Copy and fill the .env file:
Bashcp .env.example .env
Edit .env with your real credentials:
envSUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

4. Build the Prompt Index
Python# Run this once (or create an admin script)
from app.recommender import PromptRecommender

rec = PromptRecommender()
rec.load_index()  # or build it

# Example: Build index with some prompts
prompts = ["A cyberpunk girl...", "Cute fox wizard..."]  # Add real ones from DB
rec.build_index(prompts)

5. Run the Application
Bashuvicorn app.main:app --reload
Open: http://127.0.0.1:8000/docs
API Endpoints

GET / → Health check
GET /recommend/{user_id} → Get recommendations
POST /admin/build-index → Rebuild FAISS index

Future Improvements
- Add image analysis from AWS S3 using CLIP

Built as a learning project for Printee AI