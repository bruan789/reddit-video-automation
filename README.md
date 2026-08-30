# Reddit Content Curation Pipeline 🚀

**Developed by:** Samuel ([@bruan789](https://github.com/bruan789)) at **ALEXAM Tech Studio**  
**Project for:** Historias Diarias (Social Media Brand)

---

## 📌 Overview (Notice for Reddit API Reviewers)
This repository contains a **read-only** Python automation application designed to optimize the content curation workflow for the **Historias Diarias** Facebook page. 

The application securely connects to the Reddit API using **PRAW** (Python Reddit API Wrapper) to fetch trending stories from specific communities. It exclusively reads text data (Titles, Selftext, and URLs) to be processed later into narrated videos using local Text-to-Speech (TTS) and video rendering tools.

**Key API Compliance Points:**
* **Strictly Read-Only:** The application does NOT post, comment, upvote, downvote, or interact with users in any way. It only fetches public text.
* **Rate Limit Adherence:** Fully complies with Reddit's API guidelines by utilizing PRAW's built-in rate limit handling.
* **Proper Attribution:** All final video content generated through this pipeline includes clear, on-screen credits to the original Reddit author, the specific subreddit, and the Reddit platform, driving traffic back to the source.
* **Secure Credentials:** Authentication credentials (Client ID, Secret) are stored locally using environment variables (`.env`) and are never hardcoded or exposed publicly.

---
---

## 💻 Manual de Uso Interno (Spanish)

# ALEXAM Tech Studio
Aplicación inicial para obtener y preparar historias de Reddit.

### Instalación

Desde esta carpeta, ejecuta:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
