import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime
import json
import re

# Page config
st.set_page_config(
    page_title="Fintech Flash ⚡ India",
    page_icon="📱",
    layout="wide"
)

# Custom CSS for sketch-style design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kalam:wght@300;400;700&display=swap');
    
    .main-header {
        font-family: 'Kalam', cursive;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .flashcard {
        font-family: 'Kalam', cursive;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 3px solid #333;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 8px 8px 0px #333;
        transform: rotate(-1deg);
        transition: transform 0.3s ease;
        color: white;
    }
    
    .flashcard:nth-child(even) {
        transform: rotate(1deg);
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .flashcard:nth-child(3n) {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .flashcard:hover {
        transform: rotate(0deg) scale(1.02);
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-decoration: underline;
        text-decoration-style: wavy;
    }
    
    .card-content {
        font-size: 1.1rem;
        line-height: 1.4;
        font-weight: 400;
    }
    
    .linkedin-post {
        font-family: 'Kalam', cursive;
        background: #f8f9fa;
        border: 2px dashed #333;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .date-badge {
        font-family: 'Kalam', cursive;
        background: #FF6B6B;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 20px;
        transform: rotate(-2deg);
    }
</style>
""", unsafe_allow_html=True)

def configure_genai(api_key):
    """Configure Google AI Studio"""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring AI: {str(e)}")
        return False

def get_fintech_news(api_key):
    """Generate fintech and marketing news using Google AI"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
        
        prompt = f"""
        Generate exactly 5 crisp, current fintech and marketing news items specifically for India for {datetime.now().strftime('%B %d, %Y')}. 
        
        Focus on:
        - Digital payments (UPI, wallets, etc.)
        - Banking technology
        - Cryptocurrency regulations
        - Startup funding
        - Marketing trends in fintech
        - Government policies
        - Neobanks and lending platforms
        
        Format each news item as:
        TITLE: [Engaging headline in 8-12 words]
        CONTENT: [2-3 crisp sentences with key details, impact, and numbers if available]
        
        Make it current, relevant, and engaging for LinkedIn audience.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating news: {str(e)}")
        return None

def parse_news_content(content):
    """Parse the generated content into structured news items"""
    news_items = []
    
    # Split content by news items
    sections = re.split(r'\n\s*\n', content.strip())
    
    for section in sections:
        if 'TITLE:' in section and 'CONTENT:' in section:
            lines = section.strip().split('\n')
            title = ""
            content_text = ""
            
            for line in lines:
                if line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()
                elif line.startswith('CONTENT:'):
                    content_text = line.replace('CONTENT:', '').strip()
                elif content_text and not line.startswith('TITLE:'):
                    content_text += " " + line.strip()
            
            if title and content_text:
                news_items.append({
                    'title': title,
                    'content': content_text
                })
    
    return news_items[:5]  # Ensure only 5 items

def generate_linkedin_post(news_items):
    """Generate LinkedIn post content"""
    today = datetime.now().strftime('%B %d, %Y')
    
    post_content = f"""🚀 FINTECH FLASH INDIA | {today} 🇮🇳

Your daily dose of crisp fintech & marketing updates! ⚡

"""
    
    for i, item in enumerate(news_items, 1):
        post_content += f"📌 {item['title']}\n"
    
    post_content += f"""
💡 Swipe through today's flashcards for detailed insights!

What's catching your attention in today's fintech landscape? 
Drop your thoughts below! 👇

#FintechIndia #DigitalPayments #UPI #Banking #Startup #Marketing #TechNews #India #Finance #Innovation

---
Follow for daily fintech updates! 🔔
"""
    
    return post_content

# Main App
def main():
    st.markdown('<h1 class="main-header">📱 Fintech Flash India ⚡</h1>', unsafe_allow_html=True)
    
    # Date badge
    today = datetime.now().strftime('%B %d, %Y')
    st.markdown(f'<div class="date-badge">📅 {today}</div>', unsafe_allow_html=True)
    
    # API Key input
    api_key = st.text_input(
        "Enter your Google AI Studio API Key:",
        type="password",
        help="Get your API key from https://aistudio.google.com/"
    )
    
    if api_key:
        if configure_genai(api_key):
            if st.button("🎯 Generate Today's Flash Cards", type="primary"):
                with st.spinner("🔄 Fetching latest fintech news..."):
                    news_content = get_fintech_news(api_key)
                    
                    if news_content:
                        news_items = parse_news_content(news_content)
                        
                        if len(news_items) >= 3:  # Ensure we have sufficient content
                            # Display flashcards
                            st.markdown("## 📋 Today's Top 5 Fintech Flash Cards")
                            
                            # Create grid layout
                            cols = st.columns(2)
                            
                            for i, item in enumerate(news_items):
                                with cols[i % 2]:
                                    st.markdown(f"""
                                    <div class="flashcard">
                                        <div class="card-title">#{i+1} {item['title']}</div>
                                        <div class="card-content">{item['content']}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Generate LinkedIn post
                            st.markdown("## 📝 Ready-to-Post LinkedIn Content")
                            linkedin_content = generate_linkedin_post(news_items)
                            
                            st.markdown(f'<div class="linkedin-post">{linkedin_content}</div>', unsafe_allow_html=True)
                            
                            # Copy button
                            st.text_area(
                                "Copy this content for LinkedIn:",
                                linkedin_content,
                                height=200,
                                help="Select all and copy to paste on LinkedIn"
                            )
                            
                        else:
                            st.warning("⚠️ Could not generate enough news items. Please try again.")
                    else:
                        st.error("❌ Failed to generate news content. Please check your API key.")
    else:
        st.info("🔑 Please enter your Google AI Studio API key to generate flashcards.")
        
        # Instructions
        with st.expander("📖 How to get Google AI Studio API Key"):
            st.markdown("""
            1. Go to [Google AI Studio](https://aistudio.google.com/)
            2. Sign in with your Google account
            3. Click on "Get API Key" 
            4. Create a new API key
            5. Copy and paste it above
            
            **Note:** Keep your API key secure and don't share it publicly!
            """)

if __name__ == "__main__":
    main()
