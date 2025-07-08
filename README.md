# 📄 Resume Scoring Engine

Automatically evaluate and rank candidates by matching structured resumes to job descriptions.  
A powerful, interactive web application built with Streamlit, leveraging transformer embeddings, customizable scoring, and real-time visualizations to help recruiters and hiring managers identify top talent.

---


![Streamlit RnkerApp ouput screenshot](https://github.com/user-attachments/assets/c41ca8bf-956e-4864-a2ce-7ab848a84bfd)


## 🚀 Features

<table>
  <tr>
    <th colspan="2" style="text-align:left; padding-bottom: 8px;">🔹 <strong>Input</strong></th>
  </tr>
  <tr>
    <td style="padding-right: 40px;">📂 <strong>Upload multiple resumes</strong></td>
    <td>📝 <strong>Paste job descriptions </strong></td>
  </tr>
  <tr><td colspan="2" style="height: 20px;"></td></tr> <!-- Spacer row -->

  <tr>
    <th colspan="2" style="text-align:left; padding-bottom: 8px;">🔸 <strong>Output</strong></th>
  </tr>
  <tr>
    <td style="padding-right: 40px;">🧾 <strong>Scorecards per candidate</strong></td>
    <td>📊 <strong>Bar chart visualization</strong></td>
  </tr>
</table>


---
## 📂 Inputs 

### 📁 Input-1: Multiple `.json` Resume Files

These structured `.json` files are **automatically generated** using the  
**AI-Resume-Parser-Structured-Data-Extraction-Tool** from PDFs.

The source PDFs for these resumes are **retrieved** using the  
**RAG-Powered-Candidate-Retrieval-System-with-Contextual-Reranking-Tool**,  
which selects relevant resumes from a large dataset via **vector retrieval** and **contextual reranking**.

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
## Input-2: Job Description Input (String Format)
### 🧾 Example Format: 

User-provided job description in string data type:

```
job_description = """Looking for candidate with 3+ years of experience.  
Must have strong skills in Python (Scikit-learn, TensorFlow, PyTorch), SQL (Spark/Hadoop/ETL), and cloud platforms (AWS/GCP/Azure).  
Experience in NLP, LLMs, GenAI, statistical analysis, and data visualization (Tableau/Power BI) is preferred.  
Remote or based in Mumbai, Bangalore, or Pune."""
```

## 📂Outputs
### 🖼️ App Screenshot

Here’s what the Resume Ranking System looks like in action:

![Streamlit RnkerApp ouput screenshot](https://github.com/user-attachments/assets/c41ca8bf-956e-4864-a2ce-7ab848a84bfd)

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

   > 🛠️ **Note:** These weights are fully customizable.  
                   Users can adjust them based on their specific hiring priorities to influence the final scoring output.

5. **Transformer embeddings** (e.g., MiniLM) compute semantic similarity between resumes and the job description.  
6. **All given candidates** are ranked and visualized with score breakdowns.

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
- `Python`
- `streamlit`  
- `sentence-transformers`  
- `matplotlib`  
- `numpy`  

---


## 👤 Author

**Bharath Kumar**  
GitHub: [@Bharathkumar1011](https://github.com/Bharathkumar1011)

---

## ⚠️ Limitations

- ⚖️ **Model variability**: Changing the selected transformer model may lead to **different scoring behaviors**, as each model interprets semantics differently.  
- 🧩 **Input sensitivity**: Missing or mislabeled fields (e.g., `Skills`, `Experience`, `Education`) in the JSON resumes can **negatively impact scoring** or cause certain candidates to be undervalued.  
- 📊 **No fine-tuning yet**: The models are general-purpose and not fine-tuned specifically for resume/job-matching use cases.  
- 🧠 **Keyword scoring is approximate**: Synonym handling is basic and not exhaustive — some key domain-specific terms may be missed.


---
## 🌱 Future Enhancements

- Support for PDF parsing  
- Parsing unstructured resumes  
- Dynamic model selection (SBERT, BERT, etc.)  
- Export top N results to PDF or CSV  

---

## 📜 License

MIT License
