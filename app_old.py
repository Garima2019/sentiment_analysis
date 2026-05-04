import streamlit as st
import pickle

from main import clean_text

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# def predict(text):
#     text = clean_text(text)
#     vec = vectorizer.transform([text]).toarray()
#     return model.predict(vec)[0]

# st.title("Sentiment Analysis App")

# user_input=st.text_area("Enter text to analyze", height=100)

# if st.button("Predict"):
#     result = predict(user_input)
    
#     if result == "positive":
#         st.markdown(f"<h3 style='color:green;'>Positive Sentiment</h3>", unsafe_allow_html=True)
#     elif result == "negative":
#         st.markdown(f"<h3 style='color:red;'>Negative Sentiment</h3>", unsafe_allow_html=True)
#     else:
#         st.write("Predicted Sentiment:", result)

# Page config
st.set_page_config(page_title="Sentiment Analyzer", layout="centered")

# Sidebar navigation (THIS is what you asked for)
menu = st.sidebar.radio("Navigation", ["App", "README", "About Me"])

# Prediction function
def predict(text):
    text = clean_text(text)
    vec = vectorizer.transform([text]).toarray()
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec).max()
    return prediction, probability

# -------------------- APP --------------------
if menu == "App":
    st.title("Sentiment Analysis App")
    st.caption("Real-time NLP sentiment prediction using TF-IDF + Logistic Regression")

    user_input = st.text_area("Enter text to analyze", height=100)

    st.markdown("**Try examples:**")
    st.code("This movie was absolutely fantastic!")
    st.code("Worst experience ever, totally disappointing.")

    if st.button("Predict"):
        if not user_input.strip():
            st.warning("Enter some text first.")
        else:
            result, confidence = predict(user_input)

            if result == "positive":
                color = "green"
                message = "Positive Sentiment"
            elif result == "negative":
                color = "red"
                message = "Negative Sentiment"
            else:
                color = "gray"
                message = result

            st.markdown(
                f"<h2 style='color:{color};'>{message}</h2>",
                unsafe_allow_html=True
            )

            st.metric("Confidence", f"{confidence*100:.2f}%")

            st.markdown("**Processed Text:**")
            st.code(clean_text(user_input))

            with st.expander("Technical Details"):
                st.write("Vector shape:", vectorizer.transform([clean_text(user_input)]).shape)

