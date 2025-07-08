import streamlit as st # Streamlit for web app
import json
import re # Regular expressions for text processing
from sentence_transformers import SentenceTransformer, util 
import matplotlib.pyplot as plt
import numpy as np # For plotting
import os # For file handling
null = None

# Improved text normalization that handles nested structures and prioritizes key fields.
def normalize_text(data):
    """Improved text normalization that handles nested structures and prioritizes key fields."""
    if isinstance(data, str):
        return data
    elif isinstance(data, list):
        return " ".join(normalize_text(item) for item in data)
    elif isinstance(data, dict):
        # Prioritize description/role fields
        if "description" in data:
            return normalize_text(data["description"])
        elif "jobTitle" in data or "Job Title" in data:
            return normalize_text(data.get("jobTitle") or data.get("Job Title"))
        else:
            return " ".join(normalize_text(v) for v in data.values())
    else:
        return str(data)

def get_skills(resume):
    """Case-insensitive skill extraction"""
    for key in ["Skills", "skills", "SKILLS"]:
        if key in resume:
            return resume[key]
    return []

# Get experience from resume with case-insensitive handling
def get_experience(resume):
    """Case-insensitive experience extraction"""
    for key in ["Experience", "experience", "EXPERIENCE"]:
        if key in resume:
            return resume[key]
    return {}

# Ensure score is between 0 and 1
def clamp_score(score):
    """Ensure score is between 0 and 1"""
    return max(0.0, min(1.0, float(score)))

# Match resume text to job description using a sentence-transformer model.
def match_resume_to_job(resume_text, job_description, model):
    """
    Compute similarity between resume text and job description using a sentence-transformer model.
    """
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return similarity.item()

# Improved skill matching with synonyms, partial matches, and mandatory skills
def compute_skill_match(skills, job_description):
    """Improved with synonyms, partial matches, and mandatory skills"""
    mandatory_skills = {"python", "sql", "machine learning", "aws", "gcp", "azure"}
    synonyms = {
        "ml": "machine learning", "ai": "artificial intelligence",
        "nlp": "natural language processing", "pytorch": "torch",
        "tensorflow": "tf", "dl": "deep learning", "spark": "apache spark",
    }
    
    job_desc_lower = job_description.lower()
    skill_matches = 0
    
    for skill in skills:
        skill_lower = skill.lower()
        skill_lower = synonyms.get(skill_lower, skill_lower)
        # Check both full and partial matches
        if any(skill_word in job_desc_lower for skill_word in skill_lower.split()):
            skill_matches += 1
    
    # Penalty capped at 50% for missing mandatory skills
    missing_mandatory = max(0, len(mandatory_skills - {s.lower() for s in skills}))
    penalty = min(0.5, 0.1 * missing_mandatory)
    
    return max(0, (skill_matches / max(1, len(mandatory_skills))) - penalty)

# Final ranking function that applies all fixes
def rank_candidates(resumes, job_description, model):
    """Final ranking with all fixes applied"""
    scores = []
    for resume in resumes:
        # Extract data with case-insensitive handling
        skills = get_skills(resume)
        experience = get_experience(resume)
        education = resume.get("Education") or resume.get("education") or {}
        
        # Normalize text
        skills_text = normalize_text(skills)
        experience_text = normalize_text(experience)
        education_text = normalize_text(education)
        
        # Compute scores
        skill_score = clamp_score(match_resume_to_job(skills_text, job_description, model))
        experience_score = clamp_score(match_resume_to_job(experience_text, job_description, model))
        education_score = clamp_score(match_resume_to_job(education_text, job_description, model))
        keyword_score = clamp_score(compute_skill_match(skills, job_description))
        
        # Weighted scoring (adjusted weights)
        total_score = (
            0.4 * skill_score +
            0.4 * experience_score + 
            0.1 * education_score +
            0.1 * keyword_score
        )
        
        # Get candidate name
        name = (
            resume.get("Name") or
            resume.get("contactInformation", {}).get("name") or
            resume.get("Contact Information", {}).get("Name") or
            f"Unknown Candidate {len(scores)+1}"
        )
        
        scores.append({
            "Name": name,
            "Skill Score": skill_score,
            "Experience Score": experience_score,
            "Education Score": education_score,
            "Keyword Match Score": keyword_score,
            "Total Score": clamp_score(total_score)
        })
    
    return sorted(scores, key=lambda x: x["Total Score"], reverse=True)



# Function to plot scores for candidates
def plot_scores(ranked_candidates, top_n=10):
    """
    Visualize candidate scores - returns figure object for Streamlit
    
    Args:
        ranked_candidates: List of candidate dictionaries with scores
        top_n: Number of top candidates to display (default: 10)
    Returns:
        matplotlib.figure.Figure or None if no data
    """
    if not ranked_candidates or top_n <= 0:
        return None

    candidates = ranked_candidates[:top_n]
    
    # Prepare data
    names = [candidate['Name'] for candidate in candidates]
    categories = ['Skill', 'Experience', 'Education', 'Keyword Match']
    scores = {
        'Skill': [candidate['Skill Score'] for candidate in candidates],
        'Experience': [candidate['Experience Score'] for candidate in candidates],
        'Education': [candidate['Education Score'] for candidate in candidates],
        'Keyword Match': [candidate['Keyword Match Score'] for candidate in candidates],
        'Total': [candidate['Total Score'] for candidate in candidates]
    }

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.15
    index = np.arange(len(names))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Plot bars
    for i, (category, color) in enumerate(zip(categories, colors)):
        ax.bar(index + i*bar_width, scores[category], bar_width, 
               label=category, color=color)

    # Plot total score line
    ax.plot(index + 1.5*bar_width, scores['Total'],
            color='black', marker='o', linestyle='-',
            linewidth=2, markersize=8, label='Total Score')

    # Configure plot
    ax.set_xticks(index + 1.5*bar_width)
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_xlabel("Candidates")
    ax.set_ylabel("Scores")
    ax.set_title("Candidate Comparison Scores")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 1.1)
    
    fig.tight_layout()
    return fig  # This is the key change - return the figure

# Set page config
st.set_page_config(
    page_title="Resume Ranking System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit app for ranking resumes based on job description

def main():
    st.title("📄 Resume Ranking System")
    st.markdown("""
    Upload multiple resume JSON files and a job description to rank candidates based on suitability.
    """)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Input Parameters")
        
        # File uploader for multiple JSON files
        uploaded_files = st.file_uploader(
            "Upload Resume JSON Files",
            type=["json"],
            accept_multiple_files=True
        )
        
        # Job description input
        job_description = st.text_area(
            "Job Description",
            height=200,
            placeholder="Paste the job description here..."
        )
        
        # Model selection
        model_name = st.selectbox(
            "Embedding Model",
            options=[
                'paraphrase-multilingual-MiniLM-L12-v2',
                'all-MiniLM-L6-v2',
                'paraphrase-MiniLM-L3-v2'
            ],
            index=0
        )
        
        # Number of candidates to show
        top_n = st.slider(
            "Number of Top Candidates to Display",
            min_value=1,
            max_value=20,
            value=5
        )
        
        process_button = st.button("Rank Candidates")
    
    # Main content area
    if process_button and uploaded_files and job_description:
        with st.spinner("Processing resumes..."):
            try:
                # Load model
                model = SentenceTransformer(model_name)
                
                # Load and parse JSON files
                resumes = []
                file_names = []
                for uploaded_file in uploaded_files:
                    try:
                        resume_data = json.load(uploaded_file)
                        resumes.append(resume_data)
                        file_names.append(uploaded_file.name)
                    except json.JSONDecodeError:
                        st.error(f"Error decoding {uploaded_file.name} - not valid JSON")
                        continue
                
                if not resumes:
                    st.error("No valid resume data found in uploaded files")
                    return
                
                # Rank candidates
                ranked_candidates = rank_candidates(resumes, job_description, model)
                
                # Add file identifiers to names
                for idx, candidate in enumerate(ranked_candidates):
                    file_id = re.sub(r'\.json$', '', file_names[idx])
                    if not candidate['Name'] or candidate['Name'].strip() == "":
                        candidate['Name'] = f"Candidate_{file_id}"
                    else:
                        candidate['Name'] = f"{candidate['Name']} ({file_id})"
                
                # Display results in two columns
                col1, col2 = st.columns([1, 1])
                # Display top candidates
                with col1:
                    st.subheader(f"Top {min(top_n, len(ranked_candidates))} Candidates")
                    
                    for i, candidate in enumerate(ranked_candidates[:top_n], 1):
                        with st.expander(f"#{i}: {candidate['Name']} (Score: {candidate['Total Score']:.2f})"):
                            st.metric("Total Score", f"{candidate['Total Score']:.2f}")
                            st.progress(candidate['Total Score'])
                            
                            st.write("**Detailed Scores:**")
                            cols = st.columns(4)
                            cols[0].metric("Skills", f"{candidate['Skill Score']:.2f}")
                            cols[1].metric("Experience", f"{candidate['Experience Score']:.2f}")
                            cols[2].metric("Education", f"{candidate['Education Score']:.2f}")
                            cols[3].metric("Keywords", f"{candidate['Keyword Match Score']:.2f}")
                
                # Plot scores for visualization
                with col2:
                    st.subheader("Score Visualization")
                    fig = plot_scores(ranked_candidates, top_n=top_n)
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.warning("No candidates to display in the chart.")
                # Download button for results
                st.download_button(
                    label="Download Ranking Results (JSON)",
                    data=json.dumps(ranked_candidates, indent=2),
                    file_name="resume_ranking_results.json",
                    mime="application/json"
                        )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
