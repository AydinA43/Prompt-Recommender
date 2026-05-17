from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .recommender import PromptRecommender
from .schemas import RecommendResponse

app = FastAPI(title="AI Prompt Recommender", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = PromptRecommender()

@app.on_event("startup")
async def startup_event():
    recommender.load_index()

@app.get("/")
async def root():
    return {"message": "AI Image Prompt Recommender API is running!"}

@app.get("/recommend/{user_id}", response_model=RecommendResponse)
async def recommend(user_id: str, n: int = 8):
    recs = recommender.recommend(user_id, n)
    return {"recommendations": recs, "user_id": user_id}

# Optional: Build index endpoint (admin only)
@app.post("/admin/build-index")
async def build_index(prompts: List[str]):
    recommender.build_index(prompts)
    return {"status": "Index built successfully"}