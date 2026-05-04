import streamlit as st
import pickle
from main import clean_text

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentiScope · Sentiment Analyzer",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,wght@0,300;0,400;0,600;1,300&display=swap');

/* ── base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 { font-family: 'Space Mono', monospace; }

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f0f0f;
    border-right: 1px solid #1e1e1e;
}
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
section[data-testid="stSidebar"] .stRadio label { font-family: 'Space Mono', monospace; font-size: 0.82rem; letter-spacing: 0.06em; }

/* ── hero banner ── */
.hero {
    background: linear-gradient(135deg, #0a0a0a 0%, #111827 60%, #1a2744 100%);
    border: 1px solid #1f2f4a;
    border-radius: 12px;
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(59,130,246,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}
.hero-sub { color: #8b9ab0; font-size: 0.95rem; margin: 0; font-weight: 300; }

/* ── section headings ── */
.section-heading {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3b82f6;
    margin: 2rem 0 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e2a3a;
}

/* ── profile card ── */
.profile-card {
    background: #0f1623;
    border: 1px solid #1e2f47;
    border-radius: 12px;
    padding: 2rem;
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
    margin-bottom: 1.5rem;
    transition: border-color 0.2s;
}
.profile-card:hover { border-color: #3b82f6; }
.avatar {
    width: 72px; height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; flex-shrink: 0;
}
.profile-name {
    font-family: 'Space Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.2rem;
}
.profile-role {
    color: #3b82f6;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0 0 0.7rem;
}
.profile-bio { color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin: 0 0 1rem; }
.link-row { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.link-chip {
    background: #1e293b;
    border: 1px solid #334155;
    color: #94a3b8 !important;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    text-decoration: none;
    font-family: 'Space Mono', monospace;
    transition: all 0.15s;
}
.link-chip:hover { background: #1d4ed8; border-color: #3b82f6; color: #fff !important; }

/* ── stat grid ── */
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card {
    background: #0f1623;
    border: 1px solid #1e2f47;
    border-radius: 10px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.stat-value { font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #3b82f6; }
.stat-label { color: #64748b; font-size: 0.75rem; margin-top: 0.25rem; letter-spacing: 0.05em; }

/* ── info box ── */
.info-box {
    background: #0f1623;
    border: 1px solid #1e2f47;
    border-left: 3px solid #3b82f6;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.7;
    margin-bottom: 1rem;
}
.info-box b { color: #e2e8f0; }
.info-box a { color: #3b82f6; text-decoration: none; }
.info-box a:hover { text-decoration: underline; }

/* ── tag pill ── */
.tag { display: inline-block; background: #1e2a3a; border: 1px solid #2a3f5c; color: #60a5fa; padding: 0.15rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-family: 'Space Mono', monospace; margin: 0.15rem; }

/* ── doc section ── */
.doc-card {
    background: #0f1623;
    border: 1px solid #1e2f47;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.doc-card h4 { font-family: 'Space Mono', monospace; font-size: 0.9rem; color: #f1f5f9; margin: 0 0 0.6rem; }
.doc-card p, .doc-card li { color: #94a3b8; font-size: 0.88rem; line-height: 1.7; }
.doc-card ol, .doc-card ul { padding-left: 1.2rem; margin: 0; }
.step-num { display: inline-block; background: #1d4ed8; color: #fff; font-family: 'Space Mono', monospace; font-size: 0.7rem; border-radius: 4px; padding: 0.1rem 0.45rem; margin-right: 0.5rem; }

/* ── contact row ── */
.contact-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem; }
.contact-item { color: #94a3b8; font-size: 0.88rem; }
.contact-item a { color: #3b82f6; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding:1rem 0 1.5rem; border-bottom:1px solid #1e1e1e; margin-bottom:1rem;">
  <div style="font-family:'Space Mono',monospace; font-size:1rem; font-weight:700; color:#f8fafc; letter-spacing:-0.02em;">🔬 SentiScope</div>
  <div style="font-size:0.7rem; color:#475569; letter-spacing:0.12em; text-transform:uppercase; margin-top:0.2rem;">NLP · Sentiment</div>
  <div style="font-size:0.7rem; color:#334155; font-family:'Space Mono',monospace;">v1.0.0 · IMDB Dataset</div>
  <div style="font-size:0.7rem; color:#334155; margin-top:0.2rem;">TF-IDF + Logistic Regression</div>             
</div>
""", unsafe_allow_html=True)
# st.sidebar.markdown("""
# <div style="position:absolute; bottom:2rem; left:1rem; right:1rem; border-top:1px solid #1e1e1e; padding-top:1rem;">
#   <div style="font-size:0.7rem; color:#334155; font-family:'Space Mono',monospace;">v1.0.0 · IMDB Dataset</div>
#   <div style="font-size:0.7rem; color:#334155; margin-top:0.2rem;">TF-IDF + Logistic Regression</div>
# </div>
# """, unsafe_allow_html=True)

menu = st.sidebar.radio("Navigate", ["App", "Documentation", "About Me"], label_visibility="collapsed")





# ─── Predict helper ─────────────────────────────────────────────────────────
def predict(text):
    text = clean_text(text)
    vec = vectorizer.transform([text]).toarray()
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec).max()
    return prediction, probability


# ════════════════════════════════════════════════════════════════════════════
# APP PAGE
# ════════════════════════════════════════════════════════════════════════════
if menu == "App":
    st.markdown("""
    <div class="hero">
      <div class="hero-label">🔬 NLP Inference</div>
      <div class="hero-title">Sentiment<br>Analyzer</div>
      <p class="hero-sub">Real-time positive / negative classification powered by TF-IDF + Logistic Regression</p>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area("Paste or type your review below", height=100, placeholder="e.g. This film was a masterpiece of storytelling...")

    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        if st.button("✅ Positive example", use_container_width=True):
            user_input = "This movie was absolutely fantastic! Best I've seen all year."
    with col_ex2:
        if st.button("❌ Negative example", use_container_width=True):
            user_input = "Worst experience ever. Completely disappointing and boring."

    if st.button("Run Analysis →", type="primary", use_container_width=True):
        if not user_input.strip():
            st.warning("Please enter some text first.")
        else:
            result, confidence = predict(user_input)
            color = "#22c55e" if result == "positive" else "#ef4444"
            icon  = "▲" if result == "positive" else "▼"
            label = "POSITIVE" if result == "positive" else "NEGATIVE"

            st.markdown(f"""
            <div style="background:#0f1623;border:1px solid {color}33;border-left:4px solid {color};
                        border-radius:10px;padding:1.5rem 1.5rem 1rem;margin:1.5rem 0 0.5rem;">
              <div style="font-family:'Space Mono',monospace;font-size:0.65rem;letter-spacing:0.2em;
                          color:{color};margin-bottom:0.4rem;">PREDICTION</div>
              <div style="font-family:'Space Mono',monospace;font-size:2rem;font-weight:700;color:{color};">
                {icon} {label}
              </div>
              <div style="color:#64748b;font-size:0.85rem;margin-top:0.3rem;">
                Confidence: <b style="color:#f1f5f9;">{confidence*100:.1f}%</b>
              </div>
            </div>
            """, unsafe_allow_html=True)

            conf_int = int(confidence * 100)
            bar_color = "#22c55e" if result == "positive" else "#ef4444"
            st.markdown(f"""
            <div style="background:#1e293b;border-radius:999px;height:6px;margin-bottom:1.5rem;overflow:hidden;">
              <div style="width:{conf_int}%;background:{bar_color};height:100%;border-radius:999px;transition:width 0.4s;"></div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 Processed text & vector info"):
                cleaned = clean_text(user_input)
                st.code(cleaned, language="text")
                st.caption(f"Vector shape: {vectorizer.transform([cleaned]).shape} · Non-zero features: {vectorizer.transform([cleaned]).nnz}")


# ════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION PAGE
# ════════════════════════════════════════════════════════════════════════════
elif menu == "Documentation":
    st.markdown("""
    <div class="hero">
      <div class="hero-label">📖 Docs</div>
      <div class="hero-title">Technical<br>Documentation</div>
      <p class="hero-sub">Architecture, data pipeline, model training, and deployment guide</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Overview ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-card">
      <h4>What is SentiScope?</h4>
      <p>SentiScope is a lightweight, production-ready sentiment analysis web application
      built with Streamlit. It classifies free-form text — movie reviews, product feedback,
      social media posts — as <b style="color:#22c55e">positive</b> or
      <b style="color:#ef4444">negative</b> in real time, along with a confidence score.</p>
      <p style="margin-top:0.8rem;">The model is trained on the IMDB Movie Reviews dataset (50 k samples) and achieves
      <b style="color:#f1f5f9;">~88–90 % accuracy</b> on held-out test data.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Tech Stack ────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Tech Stack</div>', unsafe_allow_html=True)
    tech = [
        ("🐍 Python 3.10+", "Core language for training and serving."),
        ("📊 pandas / NumPy", "Data loading, cleaning, and array manipulation."),
        ("🤖 scikit-learn", "TF-IDF vectorizer and Logistic Regression classifier."),
        ("🌐 Streamlit", "Interactive web application framework."),
        ("💾 pickle", "Serialisation of trained model and vectorizer artifacts."),
    ]
    for name, desc in tech:
        st.markdown(f"""
        <div class="doc-card" style="display:flex;gap:1rem;align-items:center;padding:0.9rem 1.2rem;">
          <div style="font-family:'Space Mono',monospace;font-size:0.88rem;color:#f1f5f9;min-width:170px;">{name}</div>
          <div style="color:#64748b;font-size:0.85rem;">{desc}</div>
        </div>""", unsafe_allow_html=True)

    # ── Data Pipeline ─────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Data Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-card">
      <h4>Preprocessing steps</h4>
      <ol>
        <li><span class="step-num">01</span><b style="color:#e2e8f0;">Lower-case</b> — convert all characters to lowercase.</li>
        <li><span class="step-num">02</span><b style="color:#e2e8f0;">Strip non-alpha</b> — remove punctuation, digits, and special characters via regex <code style="color:#7dd3fc;">[^a-zA-Z]</code>.</li>
        <li><span class="step-num">03</span><b style="color:#e2e8f0;">TF-IDF vectorisation</b> — transform cleaned text into a 5 000-feature numeric vector. Each dimension represents the term-frequency × inverse-document-frequency weight for one token.</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)

    # ── Model ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Model</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-card">
      <h4>Logistic Regression</h4>
      <p>A binary Logistic Regression classifier from scikit-learn (default L2 regularisation, <code style="color:#7dd3fc;">solver='lbfgs'</code>, <code style="color:#7dd3fc;">max_iter=100</code>).
      The model outputs both a class label (<i>positive</i> / <i>negative</i>) and a probability score via <code style="color:#7dd3fc;">predict_proba</code>, used as the confidence metric in the UI.</p>
      <p style="margin-top:0.8rem;"><b style="color:#e2e8f0;">Train / test split:</b> 80 % / 20 % with <code style="color:#7dd3fc;">random_state=42</code> for reproducibility.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Performance ───────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Performance</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    metrics = [("~89%", "Accuracy"), ("~89%", "Precision"), ("~89%", "Recall")]
    for col, (val, lbl) in zip([c1, c2, c3], metrics):
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-value">{val}</div>
              <div class="stat-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="margin-top:0.5rem;">
      Evaluated on 10 000 held-out IMDB reviews. Results may vary slightly depending on the scikit-learn
      version and platform due to floating-point differences in the L-BFGS solver.
    </div>
    """, unsafe_allow_html=True)

    # ── File Structure ────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">File Structure</div>', unsafe_allow_html=True)
    st.code("""sentiment-analyzer/
├── app.py               # Streamlit front-end
├── main.py              # Training script + clean_text()
├── model.pkl            # Serialised Logistic Regression
├── vectorizer.pkl       # Serialised TF-IDF vectorizer
├── IMDB Dataset.csv     # Raw dataset (not committed to Git)
└── requirements.txt     # Python dependencies""", language="text")

    # ── Run Locally ───────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Run Locally</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-card">
      <h4>Setup instructions</h4>
      <ol>
        <li><span class="step-num">01</span>Clone the repository: <code style="color:#7dd3fc;">git clone https://github.com/garima2019/sentiment-analyzer</code></li>
        <li><span class="step-num">02</span>Install dependencies: <code style="color:#7dd3fc;">pip install -r requirements.txt</code></li>
        <li><span class="step-num">03</span>Download the IMDB dataset from Kaggle and place <code style="color:#7dd3fc;">IMDB Dataset.csv</code> in the root folder.</li>
        <li><span class="step-num">04</span>Train the model: <code style="color:#7dd3fc;">python main.py</code> (generates <code style="color:#7dd3fc;">model.pkl</code> and <code style="color:#7dd3fc;">vectorizer.pkl</code>)</li>
        <li><span class="step-num">05</span>Launch the app: <code style="color:#7dd3fc;">streamlit run app.py</code></li>
      </ol>
    </div>
    """, unsafe_allow_html=True)

    st.code("pip install streamlit scikit-learn pandas numpy", language="bash")

    # ── API note ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Extending the Project</div>', unsafe_allow_html=True)
    ideas = ["Replace Logistic Regression with a fine-tuned BERT / DistilBERT model", "Add neutral class using a 3-class labelled dataset", "Expose a REST endpoint with FastAPI for programmatic access", "Add SHAP explainability to highlight influential tokens", "Deploy to Streamlit Community Cloud or HuggingFace Spaces"]
    for idea in ideas:
        st.markdown(f'<div class="tag">→</div> <span style="color:#94a3b8;font-size:0.88rem;">{idea}</span><br>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ABOUT ME PAGE
# ════════════════════════════════════════════════════════════════════════════
elif menu == "About Me":
    st.markdown("""
    <div class="hero">
      <div class="hero-label">👩‍💻 Author</div>
      <div class="hero-title">About<br>the Builder</div>
      <p class="hero-sub">The developer and researcher behind SentiScope</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Profile card ─────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Developer</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="profile-card">
      <div class="avatar">👩‍💻</div>
      <div style="flex:1;">
        <div class="profile-name">Garima Agrawal</div>
        <div class="profile-role">ML Engineer · NLP Researcher</div>
        <p class="profile-bio">
          Passionate about building intelligent, data-driven systems that turn raw information into
          actionable insight. Specialises in natural language processing, feature engineering, and
          deploying machine-learning models through clean, accessible interfaces. Currently focused
          on bridging the gap between research and production ML.
        </p>
        <div class="link-row">
          <a class="link-chip" href="https://github.com/garima2019" target="_blank">⌥ GitHub</a>
          <a class="link-chip" href="https://www.linkedin.com/in/garima-agrawal-291a78185/" target="_blank">◈ LinkedIn</a>
          <a class="link-chip" href="https://garimaagw01.wixsite.com/garima_portfolio" target="_blank">◉ Portfolio</a>
          <a class="link-chip" href="mailto:garima.agw01@gmail.com">✉ Email</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Skills ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Skills & Tools</div>', unsafe_allow_html=True)
    skill_groups = {
        "Machine Learning": ["scikit-learn", "XGBoost", "Logistic Regression", "Decision Trees", "Ensemble Methods"],
        "NLP": ["TF-IDF", "NLTK", "spaCy", "Transformers", "Text Classification"],
        "Python Ecosystem": ["pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter"],
        "Deployment": ["Streamlit"],
    }
    for group, skills in skill_groups.items():
        tags = "".join(f'<span class="tag">{s}</span>' for s in skills)
        st.markdown(f"""
        <div class="doc-card" style="padding:0.9rem 1.2rem;">
          <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#3b82f6;letter-spacing:0.1em;margin-bottom:0.5rem;">{group.upper()}</div>
          <div>{tags}</div>
        </div>""", unsafe_allow_html=True)

    # ── Project stats ─────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Project at a Glance</div>', unsafe_allow_html=True)
    stats = [("50 k", "Reviews trained on"), ("~89%", "Test accuracy"), ("5 000", "TF-IDF features")]
    cols = st.columns(3)
    for col, (val, lbl) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-value">{val}</div>
              <div class="stat-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # ── Dataset ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Dataset</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
      <b>IMDB Movie Reviews Dataset</b> — 50 000 highly polar movie reviews (25 k positive, 25 k negative)
      sourced from the Internet Movie Database. Widely used as a benchmark for binary sentiment classification.<br><br>
      <a href="https://www.kaggle.com/code/lakshmi25npathi/sentiment-analysis-of-imdb-movie-reviews" target="_blank">
        🔗 View on Kaggle →
      </a>
    </div>
    """, unsafe_allow_html=True)

    # ── Mission ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Mission</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
      I build intelligent, data-driven tools that help people <b>understand language at scale</b>.
      SentiScope demonstrates how classical ML — when paired with thoughtful preprocessing and a
      clean interface — can deliver real utility without the complexity of deep learning.<br><br>
      My goal is always the same: make machine learning <b>accessible, explainable, and production-ready</b>.
    </div>
    """, unsafe_allow_html=True)

    # ── Contact ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-heading">Get in Touch</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="doc-card">
      <h4>Open to collaborations, feedback & opportunities</h4>
      <div class="contact-row">
        <div class="contact-item">✉ <a href="mailto:garima.agw01@gmail.com">garima.agw01@gmail.com</a></div>
        <div class="contact-item">⌥ <a href="https://github.com/garima2019" target="_blank">github.com/garima2019</a></div>
        <div class="contact-item">◈ <a href="https://www.linkedin.com/in/garima-agrawal-291a78185/" target="_blank">linkedin.com/in/garima-agrawal-291a78185</a></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
