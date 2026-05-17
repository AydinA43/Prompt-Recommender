from app.recommender import PromptRecommender
import sys

def main():
    print("Building prompt index from Supabase")
    
    rec = PromptRecommender()
    
    # Fetch ALL unique prompts from your database
    response = rec.supabase.table("user_generations") \
        .select("prompt") \
        .execute()
    
    all_prompts = [item['prompt'] for item in response.data if item.get('prompt')]
    unique_prompts = list(set(all_prompts))
    
    print(f"Found {len(unique_prompts)} unique prompts.")
    
    if len(unique_prompts) == 0:
        print("No prompts found in database!")
        return
    
    rec.build_index(unique_prompts)
    print("Index built successfully!")

if __name__ == "__main__":
    main()
