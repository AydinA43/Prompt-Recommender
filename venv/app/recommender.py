import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import pandas as pd
from supabase import create_client, Client
from .config import settings

class PromptRecommender:
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.prompt_list: List[str] = []

    def fetch_user_history(self, user_id: str) -> pd.DataFrame:
        response = self.supabase.table("user_generations") \
            .select("prompt, rating, created_at") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(100) \
            .execute()
        return pd.DataFrame(response.data)

    def build_index(self, all_prompts: List[str]):
        """Call this once when starting the app or daily"""
        self.prompt_list = list(set(all_prompts))
        embeddings = self.model.encode(self.prompt_list, normalize_embeddings=True).astype(np.float32)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        
        # Save index
        faiss.write_index(self.index, "index/prompt_index.faiss")
        with open("index/prompt_list.pkl", "wb") as f:
            pickle.dump(self.prompt_list, f)

    def load_index(self):
        try:
            self.index = faiss.read_index("index/prompt_index.faiss")
            with open("index/prompt_list.pkl", "rb") as f:
                self.prompt_list = pickle.load(f)
        except:
            print("Index not found. Build it first.")

    def recommend(self, user_id: str, n: int = 8) -> List[Dict]:
        df = self.fetch_user_history(user_id)
        
        if len(df) == 0:
            # Cold start
            return [{"prompt": p, "similarity": 0.8, "reason": "Popular prompt"} 
                   for p in self.prompt_list[:n]]
        
        # Get user embedding
        prompts = df['prompt'].tolist()
        ratings = df['rating'].fillna(0.7).values
        embeddings = self.model.encode(prompts, normalize_embeddings=True)
        user_vec = np.average(embeddings, axis=0, weights=ratings/ratings.sum())
        user_vec = user_vec.reshape(1, -1).astype(np.float32)

        # Search
        distances, indices = self.index.search(user_vec, n * 3)
        
        recommendations = []
        seen = set(df['prompt'].tolist())
        
        for i, idx in enumerate(indices[0]):
            prompt = self.prompt_list[idx]
            if prompt in seen:
                continue
            recommendations.append({
                "prompt": prompt,
                "similarity": float(distances[0][i]),
                "reason": "Based on your past generations"
            })
            if len(recommendations) >= n:
                break
                
        return recommendations