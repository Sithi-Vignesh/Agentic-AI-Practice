from sentence_transformers import SentenceTransformer

def dot_product(A, B):
    return sum(a * b for a, b in zip(A, B))

def norm(A):
    return (sum(a * a for a in A)) ** 0.5

def cosine_similarity(A, B):
    return dot_product(A, B) / (norm(A) * norm(B))


sentences= [
    "the Anime of the year 2026 is My Hero Academia",
    "the Anime of the year 2025 is Solo Leveling",
    "Haikyuu is a anime based on Volleyaball",
    "Volleyball in my favorite sport",
    "i love playing football and basketball",
    "i have played FIFA26 game in my friend's laptop",
    "me and my friend played split-fiction game a while back",
    "i have Asus Zenbook and my friend has Lenovo LOQ",
    "Asus zenbook has Ryzen 5800hs processor",
    "the price of RAMs and Processor have increases exponentially in the past 2 years"
]
query = "which sport do i play?"

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
embedding = model.encode(query)


final_list = []
for i in range (10):
    final_list.append((cosine_similarity(embedding, embeddings[i]),sentences[i]))

final_list.sort()
final_list = final_list[::-1]

for i in range(3):
        print(final_list[i][1])