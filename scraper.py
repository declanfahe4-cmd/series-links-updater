!pip install requests beautifulsoup4 pandas --quiet
!apt-get update -y
!apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
libxcomposite1 libxrandr2 libgbm1 libpangocairo-1.0-0 libasound2 \
libpango-1.0-0 libgtk-3-0
!pip install playwright nest_asyncio pandas --quiet
!playwright install chromium

import asyncio
import requests
import re
import pandas as pd
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import nest_asyncio

# تهيئة البيئة
nest_asyncio.apply()

# 1. قائمة الروابط (المقالات)
post_links = [
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e01",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e02",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e03",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e04",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e05",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e06",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e07",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e08",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e09",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e10",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e11",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e12",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e13",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e14",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e15",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e16",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e17",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e18",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e19",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e20",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e21",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e22",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e23",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e24",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e25",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e26",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e27",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e28",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e29",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e30",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e31",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e32",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e33",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e34",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e35",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e36",
"https://w.shadwo.pro/albaplayer/esref-ruya-s01e37",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e01",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e02",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e03",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e04",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e05",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e06",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e07",
"https://w.shadwo.pro/albaplayer/yeralti-2026-s01e08",
"https://w.shadwo.pro/albaplayer/sevdigim-sensin-2026-s01e01",
"https://w.shadwo.pro/albaplayer/sevdigim-sensin-2026-s01e02",
"https://w.shadwo.pro/albaplayer/sevdigim-sensin-2026-s01e03",
"https://w.shadwo.pro/albaplayer/sevdigim-sensin-2026-s01e04",
"https://w.shadwo.pro/albaplayer/sevdigim-sensin-2026-s01e05",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e01",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e02",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e03",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e04",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e05",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e06",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e07",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e08",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e09",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e10",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e11",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e12",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e13",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e14",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e15",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e16",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e17",
"https://w.shadwo.pro/albaplayer/kurulus-orhan-2025-s01e18",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e01",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e02",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e03",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e04",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e05",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e06",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e07",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e08",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e09",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e10",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e11",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e12",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e13",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e14",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e15",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e16",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e17",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e18",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e19",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e20",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e21",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e22",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e23",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e24",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e25",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e26",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e27",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e28",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e29",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e30",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e31",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e32",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e33",
"https://w.shadwo.pro/albaplayer/uzak-sehir-s01e34",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e01",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e02",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e03",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e04",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e05",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e06",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e07",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e08",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e09",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e10",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e11",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e12",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e13",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e14",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e15",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e16",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e17",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e18",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e19",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e20",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e21",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e22",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e23",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e24",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e25",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e26",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e27",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e28",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e29",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e30",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e31",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e32",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e33",
"https://w.shadwo.pro/albaplayer/doktor-baska-hayatta-2026-s01e34",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e01",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e02",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e03",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e04",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e05",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e06",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e07",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e08",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e09",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e10",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e11",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e12",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e13",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e14",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e15",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e16",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e17",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e18",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e19",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e20",
"https://w.shadwo.pro/albaplayer/guller-ve-gunahlar-2025-s01e21",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e01",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e02",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e03",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e04",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e05",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e06",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e07",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e08",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e09",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e10",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e11",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e12",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e13",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e14",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e15",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e16",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e17",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e18",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e19",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e20",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e21",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e22",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e23",
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e24",
               ]

async def get_direct_video_url(browser, embed_url):
    """استخراج رابط m3u8 من رابط الـ embed"""
    page = await browser.new_page()
    video_url = None

    async def handle_response(response):
        nonlocal video_url
        if ".m3u8" in response.url:
            video_url = response.url

    page.on("response", handle_response)
    try:
        await page.goto(embed_url, wait_until="networkidle", timeout=20000)
        await asyncio.sleep(6)
    except Exception:
        pass

    await page.close()
    return video_url

async def main():
    final_results_list = [] # لملف CSV
    json_data = {}          # لملف JSON

    print("--- بدء عملية الاستخراج والتحويل ---")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])

        for post_url in post_links:
            try:
                # استخراج اسم الحلقة من الرابط (المعرف)
                # سيأخذ آخر جزء من الرابط: guller-ve-gunahlar-2025-s01e01
                episode_id = post_url.split('/')[-1]

                print(f"\n[*] جاري معالجة: {episode_id}")

                response = requests.get(post_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")

                # 1. استخراج العنوان العربي
                title_tag = soup.find("title")
                arabic_title = title_tag.text.strip() if title_tag else "بدون عنوان"

                # 2. البحث عن روابط cdnplus
                cdnplus_links = re.findall(r"https://cdnplus\.cyou/embed-[\w\d]+\.html", response.text)

                if not cdnplus_links:
                    print(f"   [-] لم يتم العثور على مشغل.")
                    continue

                # نأخذ أول رابط متاح فقط أو نكرر للكل (هنا سنأخذ الأول لضمان هيكلة JSON)
                embed_link = list(set(cdnplus_links))[0]

                print(f"   [>] استخراج الرابط المباشر...")
                direct_video = await get_direct_video_url(browser, embed_link)

                if direct_video:
                    # إضافة للـ JSON (المفتاح هو معرف الحلقة)
                    json_data[episode_id] = {
                        "title": arabic_title,
                        "url": direct_video
                    }

                    # إضافة للقائمة (ملف CSV)
                    final_results_list.append({
                        "ID": episode_id,
                        "Title": arabic_title,
                        "Direct URL": direct_video,
                        "Original Post": post_url
                    })
                    print(f"   [+] تم بنجاح.")
                else:
                    print(f"   [x] لم يتم العثور على رابط m3u8.")

            except Exception as e:
                print(f"   [!] خطأ في {post_url}: {e}")

        await browser.close()

    # --- حفظ النتائج ---

    # 1. حفظ CSV
    if final_results_list:
        df = pd.DataFrame(final_results_list)
        df.to_csv("final_video_results.csv", index=False, encoding='utf-16')
        print(f"\n[تم] حفظ ملف CSV.")

    # 2. حفظ JSON (بشكل مرتب للعربيه)
    if json_data:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(f"[تم] حفظ ملف JSON باسم data.json.")

if __name__ == "__main__":
    asyncio.run(main())
