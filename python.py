import time
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

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
    time.sleep(random.uniform(1, 2))

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
    ad_element = page.locator("div[data-text-ad] a").first  # 🎯 **Sadece ilk reklamı al!**

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

        # **Tıklamayı force=True ile zorla**
        print("🖱️ Reklama tıklanıyor...")
        ad_element.click(force=True)
        time.sleep(5)  # Sayfanın açılmasını bekle
        print("✅ Reklama başarıyla tıklandı!")

        # ✅ **Sayfaya girdikten sonra ekranı kaydırma ekleyelim**
        print("🔽 Sayfa aşağı kaydırılıyor...")
        page.mouse.wheel(0, random.randint(500, 1000))  # 500-1000px arası kaydır
        time.sleep(random.uniform(3, 5))  # Kaydırma sonrası bekleme süresi

        # ✅ **Geri tuşuna basarak reklamların olduğu sayfaya dön**
        print("🔙 Geri tuşuna basılıyor, tekrar Google arama sonuçlarına dönülüyor...")
        page.go_back()
        time.sleep(5)  # Geri geldikten sonra sayfanın yüklenmesini bekle

        print("✅ Başarıyla geri dönüldü, işlem tamamlandı!")

    else:
        print("❌ Reklamın konumu belirlenemedi!")

def main(term):
    keyword = term
    p, browser, context, page = setup_browser()

    try:
        page = search_google(page, keyword)
        extract_and_visit_first_ad(page)

    finally:
        browser.close()
        p.stop()

terms = ["Python", "JavaScript", "Node.js", "React.js", "Vue.js", "Angular.js", "TypeScript", "Django", "Flask", "FastAPI","çilingir","anahtarcı",
            "anahtar", "anahtarcı", "çilingir servisi", "çilingir hizmetleri", "çilingir fiyatları", "anahtarcı servisi", "anahtarcı hizmetleri", "anahtarcı fiyatları", 
            "anahtar kopyalama", "anahtar çoğaltma", "kapı açma", "kapı kilidi değiştirme", "kapı kilidi tamiri", "çelik kapı açma", 
            "çelik kapı tamiri", "çelik kapı kilidi değiştirme", "çelik kapı kilidi tamiri","çelik kapı kilidi değiştirme", 
            "çelik kapı kilidi tamiri", "oto çilingir", "oto anahtarcı", "oto çilingir servisi", "oto çilingir hizmetleri", 
            "oto çilingir fiyatları", "oto anahtarcı servisi", "oto anahtarcı hizmetleri", "oto anahtarcı fiyatları", 
            "oto anahtar kopyalama", "oto anahtar çoğaltma", "oto kapı açma", "oto kapı kilidi değiştirme", "oto kapı kilidi tamiri",
            "oto çelik kapı açma", "oto çelik kapı tamiri", "oto çelik kapı kilidi değiştirme", "oto çelik kapı kilidi tamiri", 
            "oto çelik kapı kilidi değiştirme", "oto çelik kapı kilidi tamiri", "çilingir yakınımda", "anahtarcı yakınımda", 
            "çilingir telefonu", "anahtarcı telefonu", "çilingir adresi", "anahtarcı adresi", "çilingir nerede", "anahtarcı nerede",
            "çilingir nasıl bulunur", "anahtarcı nasıl bulunur", "çilingir nasıl çağrılır", "anahtarcı nasıl çağrılır", 
            "çilingir nasıl ulaşılır", "anahtarcı nasıl ulaşılır"]

if __name__ == "__main__":
    #for term in terms:
        #main(term)
    print(len(terms))
