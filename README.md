# 🧠 AI Accelerate Hack – KULeuven 2025  

This repository contains our project developed for the **AI Accelerate Hackathon** hosted by **Google** & **KULeuven** in 2025.  

Our goal was to build an **AI-powered voice assistant** capable of understanding natural spoken questions from clients and returning precise, contextual answers extracted from ING Belgium’s FAQ datasets — combining **speech processing**, **semantic similarity**, and a **real business use case**.  

---

## 🚀 Vision  

> Use AI to build a real-world conversational banking assistant — a system that can **understand**, **reason**, and **respond** naturally to customer questions while maintaining business relevance and measurable impact.

The assistant enables users to ask questions **orally** (via microphone), automatically extracts the **intent and theme**, retrieves the **most relevant chunk of knowledge**, and replies **instantly** with the right answer — all powered by NLP and vector similarity.  

---
### 🎥 Demo Video  

👉 A video demonstration of our prototype is available here:  
**[📺 Click here to watch the demo]([https://www.youtube.com/watch?v=KRAxs6d5dfU])**  


## 🧩 Core Features  

| Component | Description |
|------------|--------------|
| 🗣 **Speech-to-Text (STT)** | Converts the client’s voice question into text using **Google Cloud Speech-to-Text API** |
| 🔊 **Text-to-Speech (TTS)** | Reads the AI’s answer aloud for a natural user experience |
| 🧠 **NLP Theme Extraction** | Uses **Sentence Transformers** to find the main theme of the user’s question |
| 🔍 **Semantic Matching** | Combines **TF-IDF** and **cosine similarity** to locate the most relevant FAQ chunk |
| 🗄️ **MySQL Database** | Stores customer profiles, questions, and logs for later analytics |
| 📂 **Knowledge Base** | Extracts information from structured ING FAQ files (Excel chunks) |
| 🖥️ **Streamlit Interface** | Simple and intuitive web UI for demonstration and testing |

---

## ⚙️ Tech Stack  

**Languages & Frameworks:**  
- 🐍 Python 3.11  
- 🎨 Streamlit (UI / prototype interface)

**Libraries:**  
- `numpy`, `pandas`, `matplotlib`  
- `scikit-learn`, `sentence-transformers`  
- `TfidfVectorizer`, `cosine_similarity`  
- `mysql-connector-python` (MySQL connector)  
- `google-cloud-speech` (Speech-to-Text API)  
- `google-cloud-texttospeech` (Text-to-Speech API)

**Database:**  
- MySQL (structured storage for customer and query logs)

**Cloud Services:**  
- Google Cloud Platform (Speech-to-Text & Text-to-Speech APIs)

---

## 🧠 How It Works  

### 🔹 1. Speech-to-Text (STT)

The client asks a question orally (e.g. *“Mon enfant a 15 ans, quel compte ING est adapté ?”*).  
The system records the voice and converts it into text using **Google Cloud Speech-to-Text**.

```python
query = controller.get_model().speech_to_text(path_input_file)
```

### 🔹 2. Theme Extraction (NLP)
The query text is embedded using SentenceTransformer (all-MiniLM-L6-v2) to detect the most relevant theme.
We compute cosine similarities between the query vector and predefined theme vectors.

```python
best_theme, best_score = controller.load_matching(themes, query)
```

**Example:**
Detected theme: 
“Jeunes & mineurs : compte mineur, autorisation parentale, Kids/Teens, enfants”
Confidence: 0.42

### 🔹 3. Finding the Relevant FAQ Chunk  

After detecting the theme, the model searches the most relevant text file among hundreds of FAQ chunks extracted from **ING Belgium’s help center**.  

```python
res = controller.find_relevant_chunks_xlsx(
    x_path, best_theme, sheet_name=0, top_k=5, use_embeddings=False
)
```

Each chunk contains FAQ pairs (### Question + Answer). The algorithm uses TF-IDF or SentenceTransformer embeddings to rank similarity between the theme and chunk content.

### 🔹 4. Matching the User Question to the FAQ Question  

For every candidate chunk, the system compares the **user query** to each **FAQ question** inside the chunk using **TF-IDF vectors** and **cosine similarity**.  
It then selects the question with the **highest semantic similarity**.  

We keep the most probable match across all chunks:

```python
best_q, score, ans = controller.fun(fname, query)
if score > best_global["score"]:
    best_global.update({
        "chunk": fname,
        "question": best_q,
        "reponse": ans,
        "score": score
    })
```


### 🔹 5. Response Generation & Text-to-Speech
The assistant displays the answer and uses Google Cloud Text-to-Speech to read it aloud.
All interactions can also be stored in the MySQL database for analytics and continuous improvement.

**Question detected: Enfants entre 8–17 ans ?**
Answer: Ouvrez un compte ING Go to 18 gratuit — carte adaptée, contrôle parental disponible.


### 🧮 Example Flow


| Step                                                               |
|--------------------------------------------------------------------|
| 1️⃣ User says: “Mon enfant a 15 ans, quel compte ING est adapté ?” |
| 2️⃣ STT → text transcription                                       |
| 3️⃣ NLP → theme detection via SentenceTransformer                  |
| 4️⃣ Chunk retrieval → best file identified                         |
| 5️⃣ FAQ matching → “Enfants entre 8–17 ans ?”                      |
| 6️⃣ Response → “Ouvrez un compte ING Go to 18 gratuit.”            |
| 7️⃣ Bot voice  → Text-to-Speech reads the response                 |


### 💾 Database Layer  

The system connects to a **MySQL database** to store and query client data.  

```sql
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthdate DATE,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    address VARCHAR(255),
    segment_code VARCHAR(10)
);
```

Example query to check if a customer exists:

```sql
SELECT customer_id 
FROM customers
WHERE name = %s AND birthdate = %s;
```

### ⚙️ Installation & Run  

```bash
# Clone the repository
git clone https://github.com/MINOU1080/hackathon-ia.git
cd hackathon-ia

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit interface
streamlit run src/main.py
```

### 💡 Innovation & Creativity
**Why It’s Innovative:**  
🎤 **Voice-first interface:** clients can ask questions naturally using speech  
🧠 **Hybrid AI:** combines SentenceTransformers embeddings and TF-IDF similarity  
🔁 **Adaptive pipeline:** modular flow from voice → text → NLP → response  
🔉 **Conversational experience:** Text-to-Speech makes the bot feel human  

This system bridges AI comprehension and banking needs, showing how real-world FAQ systems can become interactive and intelligent.  

### 🏁 Summary
Our project bridges AI, voice interaction, and banking use cases into a single prototype capable of understanding and answering natural spoken questions.
By combining Google Cloud APIs, Sentence Transformers, TF-IDF, and MySQL, we built an assistant that is both intelligent and business-ready — a real demonstration of how AI can enhance modern banking customer experience.






