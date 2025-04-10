from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

# needs refactoring
def embedding_ranker(products: list[list[dict[str, str]]], query: str, threshold: float = 0.5):
    #product_list = [item for sublist in products for item in sublist]
    print(products)
    titles = [product["title"] for product in products]
    embeddings = model.encode([query] + titles)

    query_emb = embeddings[0].reshape(1, -1)
    title_embs = embeddings[1:]

    sims = cosine_similarity(query_emb, title_embs)[0]

    ranked = []
    for sim_score, product in zip(sims, products):
        if sim_score >= threshold:
            product_with_score = product.copy()
            product_with_score["similarity"] = float(sim_score)
            ranked.append(product_with_score)

    ranked.sort(key=lambda p: p["similarity"], reverse=True)
    return ranked

