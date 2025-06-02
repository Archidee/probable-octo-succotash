import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
import zipfile
import os
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="Marketing News Flash Cards",
    page_icon="📱",
    layout="wide"
)

# Custom CSS for sketch font styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Caveat:wght@400;600;700&display=swap');

.main-header {
    font-family: 'Kalam', cursive;
    font-size: 3rem;
    color: #0077B5;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.sub-header {
    font-family: 'Caveat', cursive;
    font-size: 1.5rem;
    color: #666;
    text-align: center;
    margin-bottom: 3rem;
}

.flash-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    color: white;
    font-family: 'Kalam', cursive;
}

.linkedin-post {
    background: #f8f9fa;
    border-left: 4px solid #0077B5;
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

def create_flash_card_image(title, content, index, total=5):
    """Create a flash card image with sketch font styling"""
    # Card dimensions
    width, height = 800, 600
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(height):
        r = int(102 + (118 - 102) * y / height)
        g = int(126 + (75 - 126) * y / height)
        b = int(234 + (162 - 234) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Try to load custom fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        content_font = ImageFont.truetype("arial.ttf", 20)
        number_font = ImageFont.truetype("arial.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        number_font = ImageFont.load_default()
    
    # Draw card number
    draw.text((50, 50), f"{index}", fill='white', font=number_font)
    
    # Draw title with text wrapping
    title_wrapped = textwrap.fill(title, width=35)
    draw.text((50, 120), title_wrapped, fill='white', font=title_font)
    
    # Draw content with text wrapping
    content_wrapped = textwrap.fill(content, width=50)
    draw.text((50, 250), content_wrapped, fill='white', font=content_font)
    
    # Add decorative elements
    draw.rectangle([30, height-80, width-30, height-30], outline='white', width=3)
    draw.text((50, height-65), f"India Marketing News • {datetime.now().strftime('%B %d, %Y')}", 
             fill='white', font=content_font)
    
    return img

def generate_marketing_news_with_ai(api_key):
    """Generate marketing news using Google AI Studio API"""
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Generate exactly 5 crisp marketing news items specifically for India market for {datetime.now().strftime('%B %d, %Y')}. 
        
        Format each news item as:
        TITLE: [Engaging title under 60 characters]
        CONTENT: [Brief description under 120 characters with key insights]
        
        Focus on:
        - Digital marketing trends in India
        - Brand campaigns and launches
        - Consumer behavior insights
        - Marketing technology updates
        - Social media marketing trends
        - E-commerce marketing strategies
        
        Make them current, relevant, and actionable for Indian marketers.
        
        Return in this exact format:
        1. TITLE: [title]
        CONTENT: [content]
        
        2. TITLE: [title]
        CONTENT: [content]
        
        And so on...
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        st.error(f"Error generating content with AI: {str(e)}")
        return None

def parse_ai_response(response_text):
    """Parse AI response into structured news items"""
    news_items = []
    lines = response_text.strip().split('\n')
    
    current_item = {}
    for line in lines:
        line = line.strip()
        if line.startswith('TITLE:'):
            if current_item:
                news_items.append(current_item)
            current_item = {'title': line.replace('TITLE:', '').strip()}
        elif line.startswith('CONTENT:'):
            current_item['content'] = line.replace('CONTENT:', '').strip()
    
    if current_item:
        news_items.append(current_item)
    
    return news_items[:5]  # Ensure we only get 5 items

def create_linkedin_post(news_items):
    """Generate LinkedIn post content"""
    today = datetime.now().strftime('%B %d, %Y')
    
    post_content = f"""🚀 Daily Marketing Flash ⚡ | {today}

Top 5 Marketing Insights for India Today:

"""
    
    for i, item in enumerate(news_items, 1):
        post_content += f"{i}. {item['title']}\n   {item['content']}\n\n"
    
    post_content += """💡 Which trend excites you the most?

#MarketingIndia #DigitalMarketing #MarketingTrends #IndiaMarketing #MarketingInsights #MarketingStrategy #BrandMarketing

---
Generated with AI • Follow for daily marketing insights"""
    
    return post_content

def create_download_zip(images, linkedin_content):
    """Create a ZIP file with all images and LinkedIn content"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add images
        for i, img in enumerate(images, 1):
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            zip_file.writestr(f'flash_card_{i}.png', img_buffer.getvalue())
        
        # Add LinkedIn content
        zip_file.writestr('linkedin_post.txt', linkedin_content)
    
    zip_buffer.seek(0)
    return zip_buffer

# Main App
def main():
    st.markdown('<h1 class="main-header">📱 Marketing News Flash Cards</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Daily Top 5 Marketing Insights for India</p>', unsafe_allow_html=True)
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input("Google AI Studio API Key", type="password", 
                               help="Enter your Google AI Studio API key to generate fresh content")
        
        if st.button("🔄 Generate Fresh Content", type="primary"):
            if api_key:
                st.session_state['generate_fresh'] = True
                st.session_state['api_key'] = api_key
            else:
                st.error("Please enter your API key first!")
    
    # Default sample data
    default_news = [
        {"title": "AI-Powered Personalization Boosts E-commerce by 40%", 
         "content": "Indian brands using AI for personalized recommendations see significant conversion increases"},
        {"title": "Regional Language Content Drives 60% More Engagement", 
         "content": "Brands adopting vernacular content strategies outperform English-only campaigns"},
        {"title": "Social Commerce Reaches ₹3.5 Lakh Crore in India", 
         "content": "Instagram and WhatsApp shopping features drive massive growth in social selling"},
        {"title": "Video Marketing Budgets Increase by 50% This Quarter", 
         "content": "Short-form video content on reels and shorts becomes top priority for marketers"},
        {"title": "Voice Search Optimization Becomes Critical for Local Brands", 
         "content": "45% of Indian consumers use voice search for local business discovery"}
    ]
    
    # Generate content
    if st.session_state.get('generate_fresh', False) and st.session_state.get('api_key'):
        with st.spinner("🤖 Generating fresh marketing insights..."):
            ai_response = generate_marketing_news_with_ai(st.session_state['api_key'])
            if ai_response:
                news_items = parse_ai_response(ai_response)
                if len(news_items) == 5:
                    st.session_state['news_items'] = news_items
                    st.session_state['generate_fresh'] = False
                    st.success("✅ Fresh content generated!")
                else:
                    st.warning("Using default content due to parsing issues")
                    st.session_state['news_items'] = default_news
            else:
                st.session_state['news_items'] = default_news
    
    # Use stored news items or default
    news_items = st.session_state.get('news_items', default_news)
    
    # Display flash cards in grid
    st.subheader("📋 Today's Marketing Flash Cards")
    
    cols = st.columns(2)
    images = []
    
    for i, item in enumerate(news_items):
        col_idx = i % 2
        with cols[col_idx]:
            # Create and display flash card image
            img = create_flash_card_image(item['title'], item['content'], i+1, len(news_items))
            images.append(img)
            
            # Convert to displayable format
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            st.image(img_buffer, use_column_width=True)
            
            # Download button for individual card
            st.download_button(
                label=f"📥 Download Card {i+1}",
                data=img_buffer.getvalue(),
                file_name=f"marketing_flash_card_{i+1}.png",
                mime="image/png",
                key=f"download_{i}"
            )
    
    # LinkedIn Post Section
    st.subheader("📱 Ready-to-Post LinkedIn Content")
    linkedin_content = create_linkedin_post(news_items)
    
    st.markdown(f'<div class="linkedin-post">{linkedin_content}</div>', unsafe_allow_html=True)
    
    # Copy button for LinkedIn content
    st.text_area("Copy this content:", linkedin_content, height=200)
    
    # Download all as ZIP
    st.subheader("📦 Download Everything")
    zip_file = create_download_zip(images, linkedin_content)
    
    st.download_button(
        label="📦 Download All Cards + LinkedIn Post (ZIP)",
        data=zip_file.getvalue(),
        file_name=f"marketing_flash_cards_{datetime.now().strftime('%Y%m%d')}.zip",
        mime="application/zip"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Pro Tip:** Use your Google AI Studio API key for fresh, daily content!")
    st.markdown("🔄 Content updates daily • Perfect for consistent LinkedIn posting")

if __name__ == "__main__":
    main()
