import time
import random
import os
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup

def setup_browser():
    """Playwright ile Stealth modda tarayıcı başlatır."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)  # Tarayıcıyı açık çalıştır
    context = browser.new_context()
    page = context.new_page()

    # 🚀 Stealth Mode etkinleştir (Bot tespiti önleme)
    stealth_sync(page)

    return p, browser, context, page

def simulate_human_mouse_move(page, target_x, target_y):
    """Fareyi doğal bir şekilde hedef noktaya hareket ettirir."""
    start_x, start_y = random.randint(50, 300), random.randint(50, 300)  # Rastgele başlangıç noktası
    steps = random.randint(10, 30)  # Hareketi bölmek için rastgele adım sayısı

    for step in range(steps):
        new_x = start_x + (target_x - start_x) * (step / steps)
        new_y = start_y + (target_y - start_y) * (step / steps)

        page.mouse.move(new_x, new_y)
        time.sleep(random.uniform(0.01, 0.03))  # Küçük gecikmelerle daha doğal hale getir

    # Son konuma git ve tıklama yap
    page.mouse.move(target_x, target_y)
    time.sleep(random.uniform(0.2, 0.5))  # Gerçekçi tıklama gecikmesi ekle
    page.mouse.click(target_x, target_y)

def search_google(page, keyword):
    """Google'da arama yaparak ilk reklamın HTML elementini bulur."""
    page.goto("https://www.google.com/")
    time.sleep(random.uniform(3, 5))

    # 🍪 Çerezleri Kabul Et
    try:
        accept_button = page.locator("text=Kabul Et")
        if accept_button.is_visible():
            bbox = accept_button.bounding_box()
            if bbox:
                simulate_human_mouse_move(page, bbox["x"] + 10, bbox["y"] + 10)
                accept_button.click()
    except:
        pass  # Eğer çerez butonu yoksa devam et

    # 📝 Arama Kutusuna Yaz ve Enter'a Bas (Harf harf yaz)
    search_box = page.locator("textarea[name='q']")
    bbox = search_box.bounding_box()
    if bbox:
        simulate_human_mouse_move(page, bbox["x"] + 10, bbox["y"] + 10)

    search_box.type(keyword, delay=random.uniform(50, 150))  # İnsan gibi yazma efekti
    time.sleep(random.uniform(1, 2))
    page.keyboard.press("Enter")

    # Sayfanın tamamen yüklenmesini bekle
    page.wait_for_load_state("load")
    time.sleep(random.uniform(4, 7))

    return page

def extract_and_visit_first_ad(page):
    """Google arama sonuçlarındaki ilk reklama tıklayarak açar."""
    print("⏳ Reklam öğesi bekleniyor...")
    ad_element = page.locator("div[data-text-ad] a").first  # 🎯 Sadece ilk reklamı al!

    # Reklamın gerçekten göründüğünü kontrol et
    try:
        page.wait_for_selector("div[data-text-ad] a", timeout=5000)
    except:
        print("❌ Reklam bulunamadı!")
        return

    # İlk reklamın X-Y koordinatlarını al
    bbox = ad_element.bounding_box()
    if bbox:
        ad_x, ad_y = bbox["x"] + (bbox["width"] / 2), bbox["y"] + (bbox["height"] / 2)  # Ortasına tıklamak için
        print(f"✅ İlk reklama gidiliyor... (X: {ad_x}, Y: {ad_y})")

        # 🎯 Reklamın görünür olup olmadığını kontrol et
        viewport_height = page.viewport_size["height"]
        if ad_y > viewport_height:
            scroll_amount = ad_y - (viewport_height / 2)
            print(f"🔽 Sayfa kaydırılıyor: {scroll_amount}px")
            page.mouse.wheel(0, scroll_amount)
            time.sleep(random.uniform(2, 4))

        # 🎯 Fareyi reklamın üzerine getir, hover yap, ardından tıkla
        print("🎯 Fare reklamın üzerine getiriliyor ve hover yapılıyor...")
        ad_element.hover()
        time.sleep(random.uniform(0.5, 1.5))

        # Tıklamayı force=True ile zorla
        print("🖱️ Reklama tıklanıyor...")
        ad_element.click(force=True)
        time.sleep(5)  # Sayfanın açılmasını bekle
        print("✅ Reklama başarıyla tıklandı!")

        # ✅ Sayfaya girdikten sonra ekranı kaydırma ekleyelim
        print("🔽 Sayfa aşağı kaydırılıyor...")
        page.mouse.wheel(0, random.randint(500, 1000))  # 500-1000px arası kaydır
        time.sleep(random.uniform(3, 5))  # Kaydırma sonrası bekleme süresi

        # ✅ Geri tuşuna basarak reklamların olduğu sayfaya dön
        print("🔙 Geri tuşuna basılıyor, tekrar Google arama sonuçlarına dönülüyor...")
        page.go_back()
        time.sleep(5)  # Geri geldikten sonra sayfanın yüklenmesini bekle

        print("✅ Başarıyla geri dönüldü, işlem tamamlandı!")

    else:
        print("❌ Reklamın konumu belirlenemedi!")
    """Google arama sonuçlarındaki ilk reklama tıklayarak açar."""

    

def google_search_and_click(term):
    p, browser, context, page = setup_browser()

    try:
        page = search_google(page, term)
        extract_and_visit_first_ad(page)

    finally:
        browser.close()
        p.stop()


os.environ["GOOGLE_API_KEY"] = "AIzaSyCL2JkomUsFf6GbCf-kUcoluBSZmHqMe6Q"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

tool = Tool(
    name="Google Search Clicker",
    func=google_search_and_click,
    description="Google'da arama yapıp reklamları tıklayan bir araç."
)

agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

search_terms = ["en iyi laptop terimini ara", "ucuz uçak bileti terimini ara", "online kurs terimini ara"]

for term in search_terms:
    print(f"Aranan terim: {term}")
    agent.run(term)

