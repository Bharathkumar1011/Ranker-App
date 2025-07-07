# 📄 Resume Scoring Engine

Automatically evaluate and rank candidates by matching structured resumes to job descriptions.  
A powerful, interactive web application built with Streamlit, leveraging transformer embeddings, customizable scoring, and real-time visualizations to help recruiters and hiring managers identify top talent.

---

## 🚀 Features

- **Upload multiple resumes** in structured `.json` format  
- **Paste or enter job descriptions** manually  
- **Weighted scoring algorithm** ranks candidates  
- **Interactive Top 5 Candidates** view with dropdown details  
- **Score breakdowns**: Skills, Experience, Education, Keyword Match  
- **Bar chart visualization** with Matplotlib  
- **MiniLM-based embedding models** for semantic matching  
- **Built with Python + Streamlit**  

---

## 📂 Input Format

Upload resume JSON files with this structure:

```json
{
  "Contact Information": {
    "Name": "Aaditya Vijay Hirurkar",
    "Email": null,
    "Phone Number": null
  },
  "Education": {
    "Institution Name": "University of Mumbai",
    "Degree": "Bachelor of Engineering, Information Technology",
    "Graduation Date": "2008"
  },
  "Experience": [
    {
      "Job Title": "Business Analyst Sr. Technical Business Analyst",
      "Dates of Employment": "Jul 2011 to Dec 2013",
      "Description": "Requirement Gathering, Product implementation, etc."
    }
  ],
  "Skills": {
    "Skills": ["Java", "Oracle", "J2EE", "SQL"]
  }
}
```

---

## ⚙️ How It Works

1. **Upload resumes** (JSON format) and enter a job description.  
2. **Resumes are parsed and normalized** (case-insensitive).  
3. **Scoring algorithm** evaluates each candidate:

   | Component             | Weight |
   |-----------------------|--------|
   | Skills Match          | 40%    |
   | Experience Relevance  | 40%    |
   | Education Match       | 10%    |
   | Keyword Match from JD | 10%    |

4. **Transformer embeddings** (e.g., MiniLM) compute semantic similarity between resumes and the job description.  
5. **Top 5 candidates** are ranked and visualized with score breakdowns.

---

## 🖥️ Output

- **Ranked list** of top candidates  
- **Interactive dropdown**: names, file references, scores  
- **Bar chart** comparing key score components  

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Bharathkumar1011/Ranker-stResume-Scoring-Engine-Match-Candidates-with-Job-Descriptionsreamlit.git
cd Ranker-stResume-Scoring-Engine-Match-Candidates-with-Job-Descriptionsreamlit
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys (if needed)

Some embedding models may require API access or downloading pretrained weights.

### 4. Run the App

```bash
streamlit run RankerApp.py
```

Open your browser and visit: [http://localhost:8501](http://localhost:8501)

---

## 📦 Requirements

- `nginx`  
- `streamlit`  
- `sentence-transformers`  
- `matplotlib`  
- `numpy`  

---

## 📁 Input/Output Formats

**Input:**  
Structured JSON resumes with these sections:
- Contact Information  
- Education  
- Experience  
- Skills  

**Output:**  
- Ranked JSON of top candidates  
- Streamlit web interface  
- Bar chart of scores  

---

## 📊 Scoring Breakdown

| Component         | Weight |
|-------------------|--------|
| Skills Match      | 40%    |
| Experience Match  | 40%    |
| Education Match   | 10%    |
| Keyword Match     | 10%    |

---

## 👤 Author

**Bharath Kumar**  
GitHub: [@Bharathkumar1011](https://github.com/Bharathkumar1011)

---

## 🌱 Future Enhancements

- Support for PDF parsing  
- Parsing unstructured resumes  
- Dynamic model selection (SBERT, BERT, etc.)  
- Export top N results to PDF or CSV  

---

## 📜 License

MIT License
