import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("🤖 बुलेटप्रूफ मल्टी-पेज स्क्रैपर एक्टिवेट हो रहा है...")

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') 
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

products_data = []
search_query = "laptops"
max_pages = 3  # जितने पेज का डेटा चाहिए यहाँ बदल सकते हो

try:
    for page in range(1, max_pages + 1):
        print(f"\n📄 पेज {page} का डेटा निकाला जा रहा है...")
        url = f"https://www.flipkart.com/search?q={search_query}&page={page}"
        driver.get(url)
        time.sleep(5)  # फ्लिपकार्ट को लोड होने का पूरा समय दें

        # 🔥 हैक 1: क्लास नेम छोड़ो, सीधे 'data-id' वाले सभी प्रोडक्ट बॉक्स पकड़ो!
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
        
        if not products:
            print(f"⚠️ पेज {page} पर कोई प्रोडक्ट नहीं मिला।")
            break

        for index, product in enumerate(products, start=1):
            
            # 🔥 हैक 2: नाम और फोटो के लिए सीधे इमेज टैग (img) को टारगेट करो
            # क्योंकि फ्लिपकार्ट की इमेज के 'alt' टेक्स्ट में हमेशा प्रोडक्ट का पूरा नाम होता है!
            try:
                img_element = product.find_element(By.TAG_NAME, "img")
                name = img_element.get_attribute("alt")
                photo_url = img_element.get_attribute("src")
            except:
                name = "N/A"
                photo_url = "N/A"
                
            # 🔥 हैक 3: कीमत के लिए वो एलिमेंट ढूंढो जिसमें '₹' का सिंबल हो
            try:
                price_element = product.find_element(By.XPATH, ".//*[contains(text(), '₹')]")
                price = price_element.text
            except:
                price = "N/A"
                
            # 🔥 हैक 4: स्पेसिफिकेशन्स (Details) के लिए 'ul' लिस्ट को पकड़ो
            try:
                details_element = product.find_element(By.TAG_NAME, "ul")
                details = details_element.text.replace("\n", " | ")
            except:
                details = "N/A"
                
            # सिर्फ असली प्रोडक्ट्स को लिस्ट में डालने के लिए (ताकि रैंडम विज्ञापन न आएं)
            if name != "N/A" and price != "N/A":
                print(f"📦 [पेज {page} - No.{index}] {name[:40]}... | Price: {price}")
                products_data.append({
                    "Page": page,
                    "Product Name": name,
                    "Price": price,
                    "Photo URL": photo_url,
                    "Details/Specs": details
                })

    # 💾 डेटा को Excel/CSV में सेव करना
    if products_data:
        df = pd.DataFrame(products_data)
        df.to_csv("flipkart_all_laptops.csv", index=False, encoding="utf-8-sig")
        print(f"\n🎉 गजब भाई! कुल {len(products_data)} लैपटॉप्स का पूरा डेटा 'flipkart_all_laptops.csv' में सेव हो गया है।")
    else:
        print("\n❌ इस बार भी कोई डेटा सेव नहीं हो सका।")

except Exception as e:
    print(f"⚠️ एरर आया: {e}")

finally:
    print("🔒 काम पूरा! ब्राउज़र बंद किया जा रहा है...")
    driver.quit()