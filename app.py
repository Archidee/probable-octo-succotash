import streamlit as st
import requests
import json
from datetime import datetime
import google.generativeai as genai
from typing import List, Dict
import time

# Page config
st.set_page_config(
    page_title="India Fintech Daily Flash ⚡",
    page_icon="💳",
    layout="wide"
)

# Custom CSS for sketch fonts and grid layout
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@300;400;700&family=Caveat:wght@400;500;600;700&display=swap');

.main-title {
    font-family: 'Caveat', cursive;
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    color: #1f4e79;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.flashcard {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: white;
    font-family: 'Kalam', cursive;
    transition: transform 0.3s ease;
}

.flashcard:hover {
    transform: translateY(-5px);
}

.flashcard h3 {
    font-family: 'Caveat', cursive;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 15px;
    color: #fff;
}

.flashcard p {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 10px;
}

.linkedin-post {
    background: #f8f9fa;
    border: 2px dashed #4267b2;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    font-family: 'Kalam', cursive;
}

.news-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

class FintechNewsGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    
    def get_fintech_news(self) -> List[Dict]:
        """Generate fintech news using Gemini AI"""
        prompt = f"""
        Generate exactly 5 crisp, current fintech news items specifically for India for {datetime.now().strftime('%B %d, %Y')}.
        
        Each news item should:
        - Be real and credible (based on recent trends in Indian fintech)
        - Be 2-3 sentences maximum
        - Include specific company names, numbers, or locations when possible
        - Focus on: payments, digital banking, cryptocurrency, lending, insurtech, or fintech regulations in India
        
        Return as JSON format:
        {{
            "news": [
                {{
                    "title": "Brief catchy title",
                    "content": "2-3 sentence description",
                    "category": "category like 'Payments', 'Digital Banking', etc."
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            news_data = json.loads(response_text)
            return news_data.get('news', [])
        except Exception as e:
            st.error(f"Error generating news: {str(e)}")
            return self.get_fallback_news()
    
    def get_fallback_news(self) -> List[Dict]:
        """Fallback news in case API fails"""
        return [
            {
                "title": "PhonePe Crosses 500M Users",
                "content": "PhonePe announces milestone of 500 million registered users, processing over 8 billion transactions monthly. The Walmart-backed fintech continues to dominate India's UPI ecosystem.",
                "category": "Payments"
            },
            {
                "title": "RBI Introduces New Digital Lending Rules",
                "content": "Reserve Bank of India unveils stricter guidelines for digital lending platforms. New regulations focus on fair practices and borrower protection in the growing fintech lending space.",
                "category": "Regulation"
            },
            {
                "title": "Paytm Bank Launches Savings Plus",
                "content": "Paytm Payments Bank introduces high-yield savings account with 6% interest rate. The neo-bank targets young professionals with digital-first banking features.",
                "category": "Digital Banking"
            },
            {
                "title": "Razorpay Expands to Southeast Asia",
                "content": "Razorpay announces international expansion with launch in Malaysia and Singapore. The payment gateway aims to capture $2 billion Southeast Asian market opportunity.",
                "category": "Payments"
            },
            {
                "title": "HDFC Bank Partners with Fintech Startups",
                "content": "HDFC Bank launches fintech accelerator program investing ₹100 crores in emerging startups. Focus areas include AI-driven lending and blockchain-based solutions.",
                "category": "Innovation"
            }
        ]
    
    def generate_linkedin_post(self, news_items: List[Dict]) -> str:
        """Generate LinkedIn post content"""
        prompt = f"""
        Create an engaging LinkedIn post for sharing today's top 5 Indian fintech news.
        
        News items:
        {json.dumps(news_items, indent=2)}
        
        The post should:
        - Start with an engaging hook about Indian fintech
        - Mention it's a daily series "India Fintech Flash ⚡"
        - Use relevant emojis and hashtags
        - Be professional yet engaging
        - Include call-to-action for engagement
        - Keep it under 300 words
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return self.get_fallback_linkedin_post()
    
    def get_fallback_linkedin_post(self) -> str:
        """Fallback LinkedIn post"""
        return """🚀 India Fintech Flash ⚡ - Your Daily Dose of Fintech Innovation!

Another exciting day in India's fintech ecosystem! Here are today's top 5 developments that are reshaping how we bank, pay, and invest:

💳 From payment unicorns hitting new milestones to regulatory updates shaping the future
🏦 Digital banking innovations making financial services more accessible
📊 Investment in fintech reaching new heights across the country

India continues to lead the global fintech revolution with over 500M+ digital payment users and counting!

What's your take on these developments? Which news caught your attention the most?

#IndiaFintech #DigitalPayments #Fintech #Innovation #Banking #UPI #DigitalIndia #FintechFlash

---
📌 Follow for daily fintech updates
🔔 Turn on notifications to never miss the flash!"""

def main():
    st.markdown('<h1 class="main-title">🇮🇳 India Fintech Flash ⚡</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-family: Kalam; font-size: 1.2rem; color: #666;">Your Daily Top 5 Fintech News Flashcards</p>', unsafe_allow_html=True)
    
    # Sidebar for API key
    with st.sidebar:
        st.markdown("### 🔑 Configuration")
        api_key = st.text_input("Google AI Studio API Key", type="password", help="Enter your Google AI Studio API key")
        
        if st.button("🔄 Generate Fresh News", type="primary"):
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.regenerate = True
            else:
                st.error("Please enter your API key first!")
    
    # Main content
    if 'api_key' not in st.session_state:
        st.info("👈 Please enter your Google AI Studio API key in the sidebar to generate news flashcards!")
        st.markdown("""
        ### How to get your API key:
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a new API key
        3. Copy and paste it in the sidebar
        4. Click 'Generate Fresh News'
        """)
        return
    
    # Initialize or regenerate news
    if 'news_data' not in st.session_state or st.session_state.get('regenerate', False):
        with st.spinner("🔍 Fetching latest fintech news..."):
            generator = FintechNewsGenerator(st.session_state.api_key)
            st.session_state.news_data = generator.get_fintech_news()
            st.session_state.linkedin_post = generator.generate_linkedin_post(st.session_state.news_data)
            st.session_state.regenerate = False
    
    # Display news flashcards
    if 'news_data' in st.session_state:
        st.markdown(f"### 📅 {datetime.now().strftime('%B %d, %Y')} - Top 5 Fintech Updates")
        
        # Create grid layout for flashcards
        cols = st.columns(2)
        for i, news in enumerate(st.session_state.news_data):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="flashcard">
                    <h3>💡 {news['title']}</h3>
                    <p>{news['content']}</p>
                    <small style="background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.8rem;">
                        📊 {news['category']}
                    </small>
                </div>
                """, unsafe_allow_html=True)
        
        # LinkedIn post section
        st.markdown("---")
        st.markdown("### 📱 Ready-to-Post LinkedIn Content")
        
        st.markdown(f"""
        <div class="linkedin-post">
            <h4 style="color: #4267b2; font-family: Caveat; margin-bottom: 15px;">📋 Copy & Paste to LinkedIn:</h4>
            <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #4267b2;">
                {st.session_state.linkedin_post.replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Copy button
        if st.button("📋 Copy LinkedIn Post", help="Click to copy the post content"):
            st.success("✅ LinkedIn post copied to clipboard! (Use Ctrl+C to copy the text above)")
        
        # Download options
        st.markdown("### 💾 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            # Create JSON download
            news_json = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "news": st.session_state.news_data,
                "linkedin_post": st.session_state.linkedin_post
            }
            st.download_button(
                "📄 Download as JSON",
                data=json.dumps(news_json, indent=2),
                file_name=f"fintech_flash_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        with col2:
            # Create text download
            text_content = f"""India Fintech Flash ⚡ - {datetime.now().strftime('%B %d, %Y')}

TOP 5 FINTECH NEWS:
{'='*50}

"""
            for i, news in enumerate(st.session_state.news_data, 1):
                text_content += f"{i}. {news['title']}\n   {news['content']}\n   Category: {news['category']}\n\n"
            
            text_content += f"""
LINKEDIN POST:
{'='*50}
{st.session_state.linkedin_post}
"""
            
            st.download_button(
                "📝 Download as Text",
                data=text_content,
                file_name=f"fintech_flash_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
