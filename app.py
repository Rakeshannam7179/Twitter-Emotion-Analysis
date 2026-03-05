import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Multimodal Emotion Analysis", layout="wide")

st.title("🎭 Multimodal Emotion Analysis")
st.markdown("Analyze emotions from **Text** and **Images** using a fused AI model.")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("Backend API URL", "http://localhost:8000/analyze_multimodal")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Inputs")
    text_input = st.text_area("Enter text to analyze", height=150, placeholder="I am feeling great today!")
    image_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg", "webp", "tiff", "bmp"])
    
    if image_file:
        st.image(image_file, caption="Preview", width=300)
    
    analyze_btn = st.button("Analyze Emotions", type="primary")

if analyze_btn:
    if not text_input and not image_file:
        st.warning("Please enter some text OR upload an image.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # Construct payload based on available inputs
                files = {}
                data = {}
                
                if image_file:
                     files = {"image": ("uploaded_image.jpg", image_file.getvalue(), image_file.type)}
                if text_input:
                    data["text"] = text_input
                
                response = requests.post(api_url, data=data, files=files if files else None)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    with col2:
                        st.subheader("Results")
                        
                        # Display Final Emotion
                        final_emotion = result.get("final_emotion", "Unknown")
                        st.success(f"Final Prediction: **{final_emotion.upper()}**")
                        
                        # Tabs for details
                        tab1, tab2, tab3 = st.tabs(["Fused Scores", "Text Scores", "Image Scores"])
                        
                        with tab1:
                            st.caption("Weighted fusion of text and image scores")
                            st.bar_chart(result.get("fused_scores", {}))
                        
                        with tab2:
                            st.caption("RoBERTa Model Result")
                            st.json(result.get("text_scores", {}))
                            
                        with tab3:
                            source = result.get("meta", {}).get("emotion_source", "Unknown")
                            st.caption(f"Image Analysis Source: {source.title()}")
                            st.json(result.get("image_scores", {}))
                            
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}. Is the backend running?")

# New Hashtag Analysis Feature
st.divider()
st.header("🔍 Hashtag Emotion Trend")
st.markdown("Analyze the collective emotion of recent tweets for a specific hashtag.")

h_col1, h_col2 = st.columns([1, 2])

with h_col1:
    h_tag = st.text_input("Enter Hashtag", placeholder="#AI")
    h_count = st.slider("Number of tweets to analyze", 5, 50, 10)
    h_analyze_btn = st.button("Analyze Hashtag", type="secondary")

if h_analyze_btn:
    if not h_tag:
        st.warning("Please enter a hashtag.")
    else:
        with st.spinner(f"Scraping and analyzing tweets for {h_tag}..."):
            try:
                h_response = requests.post("http://localhost:8000/analyze_hashtag", json={"hashtag": h_tag, "count": h_count})
                if h_response.status_code == 200:
                    h_result = h_response.json()
                    
                    with h_col2:
                        total = h_result.get("total_analyzed", 0)
                        if total == 0:
                            st.error(h_result.get("message", "No tweets found or scraping failed."))
                        else:
                            st.subheader(f"Results for {h_tag}")
                            st.success(f"Successfully analyzed **{total}** tweets.")
                            
                            # Emotion Distribution
                            percentages = h_result.get("emotions_percentage", {})
                            dominant = max(percentages, key=percentages.get) if percentages else "None"
                            
                            st.write(f"Dominant Emotion: **{dominant.upper()}**")
                            
                            # Bar chart for distribution
                            import pandas as pd
                            if percentages:
                                df = pd.DataFrame({
                                    'Emotion': list(percentages.keys()),
                                    'Percentage': list(percentages.values())
                                })
                                st.bar_chart(df.set_index('Emotion'))
                            
                            # Show some sample tweets and their emotions
                            with st.expander("View Sample Analyzed Tweets"):
                                for item in h_result.get("results", []):
                                    st.markdown(f"**Emotion: {item['dominant_emotion'].upper()}**")
                                    st.text(item['text'])
                                    st.divider()
                else:
                    st.error(f"Error: {h_response.status_code} - {h_response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
