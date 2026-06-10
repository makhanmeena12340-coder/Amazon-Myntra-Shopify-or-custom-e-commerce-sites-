import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. Page Configuration & Custom CSS for High-End Styling
st.set_page_config(page_title="Flipkart Live Scraper Dashboard", page_icon="⚡", layout="wide")

# Injecting premium UI/UX styles
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }
    .product-card {
        border: 1px solid #1e293b;
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 340px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
        box-shadow: 0 10px 15px -3px rgb(59 130 246 / 0.3);
    }
    .product-title {
        font-size: 14px;
        font-weight: 600;
        color: #f8fafc;
        margin-top: 10px;
        height: 45px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .product-price {
        color: #10b981;
        font-size: 22px;
        font-weight: 700;
        margin-top: 5px;
    }
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<h1 style='text-align: center; color: #3b82f6; margin-bottom: 0;'>⚡ UNIVERSAL FLIPKART LIVE SCRAPER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-top: 5px;'>Instantly extract real-time product data, pricing, and images directly from Flipkart</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 3. Selenium Live Scraper Core Logic
def live_flipkart_scraper(search_query):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Background execution
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    products_data = []
    
    try:
        url = f"https://www.flipkart.com/search?q={search_query}&page=1"
        driver.get(url)
        time.sleep(4)
        
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
        
        for product in products:
            try:
                img_element = product.find_element(By.TAG_NAME, "img")
                name = img_element.get_attribute("alt")
                photo_url = img_element.get_attribute("src")
            except:
                name = "N/A"
                photo_url = "N/A"
                
            try:
                price_element = product.find_element(By.XPATH, ".//*[contains(text(), '₹')]")
                price = price_element.text
            except:
                price = "N/A"
                
            if name != "N/A" and price != "N/A" and len(name) > 5:
                products_data.append({
                    "Product Name": name,
                    "Price": price,
                    "Photo URL": photo_url
                })
                
    except Exception as e:
        st.error(f"Scraping Error: {e}")
    finally:
        driver.quit()
        
    return products_data

# 4. Search and Input UI Panel
st.markdown("<h4 style='color: #cbd5e1;'>Search Engine</h4>", unsafe_allow_html=True)
search_word = st.text_input("Enter product name to scrape (e.g., jeans, chair, smart watch, iphone):", placeholder="Type keywords here...").strip()

if search_word:
    with st.spinner(f"✨ Navigating Flipkart for '{search_word}'... Extracting live data points..."):
        scraped_result = live_flipkart_scraper(search_word)
        
    if scraped_result:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric(label="Total Live Products Fetched", value=f"{len(scraped_result)} Items")
        st.markdown("<h3 style='color: #f8fafc; border-bottom: 2px solid #3b82f6; padding-bottom: 8px;'>📦 Live Showcase</h3>", unsafe_allow_html=True)
        
        # 4-Column Grid Layout for premium look
        cols = st.columns(4)
        for index, row in enumerate(scraped_result):
            with cols[index % 4]:
                # 🚀 प्योर HTML इमेज टैग ताकि कंपोनेंट अंदर ही लॉक रहे
                img_html = f"<img src='{row['Photo URL']}' style='height: 120px; object-fit: contain; margin-bottom: 10px; border-radius: 6px;'>" if row['Photo URL'] and row['Photo URL'] != "N/A" else "<div style='height:120px; color:#64748b; display:flex; align-items:center; justify-content:center;'>📷 No Image</div>"
                
                short_title = row['Product Name'][:45] + "..." if len(row['Product Name']) > 45 else row['Product Name']
                
                # पूरा कार्ड एक ही ब्लॉक में इंजेक्ट कर रहे हैं
                card_html = f"""
                <div class='product-card'>
                    {img_html}
                    <div class='product-title'>{short_title}</div>
                    <div class='product-price'>{row['Price']}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
        # 💾 Data Export Segment
        st.markdown("<br>", unsafe_allow_html=True)
        df = pd.DataFrame(scraped_result)
        csv_data = df.to_csv(index=False, encoding="utf-8-sig")
        
        st.download_button(
            label="📥 Download Dataset as CSV",
            data=csv_data,
            file_name=f"flipkart_{search_word}_live.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No products found. Please refine your search query.")