"""Helper NLP methods for scraping."""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def single_embedding_ranker(products: list[dict[str, str]], query: str, threshold: float = 0.5) -> list[dict[str, str]]:
    print(products)
    titles = [product["title"] for product in products]
    
    # encodes query and product titles into embeddings all in one list
    embeddings = model.encode([query] + titles)

    # separates the query and title embeddings
    query_emb = embeddings[0].reshape(1, -1)
    title_embs = embeddings[1:]

    # calculates the cosine similarity between the query and each title
    sims = cosine_similarity(query_emb, title_embs)[0]

    ranked = []
    # for each similarity score, if it is above the threshold, add the product to the ranked list
    for sim_score, product in zip(sims, products):
        if sim_score >= threshold:
            product_with_score = product.copy()
            print(product_with_score)
            product_with_score["similarity"] = float(sim_score)
            ranked.append(product_with_score)

    # sort the ranked list by similarity score in descending order
    ranked.sort(key=lambda p: p["similarity"], reverse=True)
    return ranked