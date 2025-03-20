import time
import random
import os
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

mobile_devices = ['Blackberry PlayBook', 'BlackBerry Z30', 'Galaxy Note 3', 'Galaxy Note II', 'Galaxy S III', 'Galaxy S5', 
                  'Galaxy S8', 'Galaxy S9+', 'Galaxy Tab S4', 'iPad (gen 5)', 'iPad (gen 6)', 'iPad (gen 7)', 'iPad Mini', 
                  'iPad Pro 11', 'iPhone 6', 'iPhone 6 Plus', 'iPhone 7', 'iPhone 7 Plus', 'iPhone 8', 'iPhone 8 Plus', 
                  'iPhone SE', 'iPhone X', 'iPhone XR', 'iPhone 11', 'iPhone 11 Pro', 'iPhone 11 Pro Max', 'iPhone 12', 
                  'iPhone 12 Pro', 'iPhone 12 Pro Max', 'iPhone 12 Mini', 'iPhone 13', 'iPhone 13 Pro', 'iPhone 13 Pro Max', 
                  'iPhone 13 Mini', 'iPhone 14', 'iPhone 14 Plus', 'iPhone 14 Pro', 'iPhone 14 Pro Max', 'iPhone 15', 
                  'iPhone 15 Plus', 'iPhone 15 Pro', 'iPhone 15 Pro Max', 'Kindle Fire HDX', 'LG Optimus L70', 
                  'Microsoft Lumia 550', 'Microsoft Lumia 950', 'Nexus 10', 'Nexus 4', 'Nexus 5', 'Nexus 5X', 'Nexus 6', 
                  'Nexus 6P', 'Nexus 7', 'Nokia Lumia 520', 'Nokia N9', 'Pixel 2', 'Pixel 2 XL', 'Pixel 3', 'Pixel 4', 
                  'Pixel 4a (5G)', 'Pixel 5', 'Pixel 7', 'Moto G4']

# 📂 Çerezleri saklayacağımız dosya
storage_path = "cookies.json"

# 🛠 Eğer çerez dosyası bozuksa veya yoksa, yüklemeyi atla
if os.path.exists(storage_path):
    try:
        with open(storage_path, "r") as f:
            json.load(f)  # JSON'un bozuk olup olmadığını kontrol et
    except json.JSONDecodeError:
        os.remove(storage_path)  # Bozuksa dosyayı sil

def setup_browser():
    """Playwright ile Stealth modda iPhone 15 emülasyonu ile tarayıcı başlatır."""
    p = sync_playwright().start()

    # 📱 iPhone 15'e en yakın profil (iPhone 14 Pro)
    iphone_15 = p.devices["iPhone 14 Pro"]

    # Çerez dosyası varsa kullan, yoksa temiz başlat
    storage_state = storage_path if os.path.exists(storage_path) else None

    browser = p.webkit.launch(headless=False)  # WebKit tarayıcıyı kullan (Safari'yi taklit etmek için)
    context = browser.new_context(**iphone_15, storage_state=storage_state)
    page = context.new_page()

    # 🚀 Stealth Mode etkinleştir (Bot tespiti önleme)
    stealth_sync(page)

    # 🤖 Bot tespiti önleme (Ekstra önlemler)
    page.evaluate("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return p, browser, context, page

def search_google(page, keyword):
    """Google'da arama yaparak ilk reklamın HTML elementini bulur."""
    page.goto("https://www.google.com/")
    time.sleep(random.uniform(5, 8))  # Sayfanın tam yüklenmesi için bekleme

    # 🍪 Çerezleri Kabul Et
    try:
        accept_button = page.locator("text=Kabul Et")
        if accept_button.is_visible():
            accept_button.tap()  # Mobilde tıklamak yerine tap() kullan
            time.sleep(random.uniform(3, 5))
    except:
        pass  # Eğer çerez butonu yoksa devam et

    # 📝 Mobil Klavye Taklidi: Arama kutusuna tıklayarak focus yap
    search_box = page.locator("textarea[name='q']")
    search_box.tap()
    time.sleep(random.uniform(2, 5))  # Mobil klavye açılma süresi simülasyonu

    # 📌 BOŞ KARAKTER YAZ VE KLAVYEYİ AÇMAYA ZORLA
    page.evaluate("document.querySelector('textarea[name=q]').focus();")
    time.sleep(2)  
    page.keyboard.type(" ", delay=random.uniform(50, 100))  # Boşluk karakteri ekle
    page.keyboard.press("Backspace")  # Boşluğu sil
    time.sleep(1)

    # 📌 GERÇEK KELİMEYİ HARF HARF YAZ (Mobil Klavyeyi Simüle Et)
    for char in keyword:
        page.keyboard.press(char)
        time.sleep(random.uniform(0.1, 0.3))

    time.sleep(random.uniform(2, 4))  
    page.keyboard.press("Enter")

    # Sayfanın tamamen yüklenmesini bekle
    page.wait_for_load_state("load")
    time.sleep(random.uniform(5, 10))  

    # 🚨 CAPTCHA Kontrolü
    if "captcha" in page.content().lower():
        input("🚨 CAPTCHA algılandı! Lütfen manuel olarak çöz ve Enter'a bas...")

    return page

def save_html(page):
    html_source = page.content()
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(html_source)

def main():
    keyword = input("🔎 Aramak istediğiniz kelimeyi girin: ")
    p, browser, context, page = setup_browser()

    try:
        page = search_google(page, keyword)

    finally:
        # Çerezleri kaydet
        context.storage_state(path=storage_path)
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()
