import asyncio
import requests
import re
import pandas as pd
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import nest_asyncio

nest_asyncio.apply()

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
"https://w.shadwo.pro/albaplayer/halef-koklerin-cagrisi-2025-s01e24",    # ... باقي الروابط
]

async def get_direct_video_url(browser, embed_url):
    page = await browser.new_page()
    video_url = None

    async def handle_response(response):
        nonlocal video_url
        if ".m3u8" in response.url and "master" in response.url:  # اختياري: فلتر أفضل
            video_url = response.url

    page.on("response", handle_response)

    try:
        await page.goto(embed_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(8)  # زد الانتظار شوية
    except Exception as e:
        print(f"خطأ أثناء الذهاب للصفحة: {e}")
    finally:
        await page.close()

    return video_url

async def main():
    json_data = {}
    final_results_list = []

    print("--- بدء عملية الاستخراج ---")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )

        for post_url in post_links:
            try:
                episode_id = post_url.split('/')[-1]
                print(f"\n[*] معالجة: {episode_id}")

                resp = requests.get(post_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                title = soup.find("title").text.strip() if soup.find("title") else episode_id

                cdn_links = re.findall(r"https://cdnplus\.cyou/embed-[\w\d]+\.html", resp.text)
                if not cdn_links:
                    print("   [-] لا يوجد مشغل")
                    continue

                embed = cdn_links[0]  # أول واحد
                print(f"   [>] جاري استخراج من: {embed}")

                m3u8 = await get_direct_video_url(browser, embed)

                if m3u8:
                    json_data[episode_id] = {"title": title, "url": m3u8}
                    final_results_list.append({
                        "ID": episode_id,
                        "Title": title,
                        "URL": m3u8,
                        "Post": post_url
                    })
                    print("   [+] نجح")
                else:
                    print("   [x] ما لقيناش m3u8")

            except Exception as e:
                print(f"   [!] خطأ: {e}")

        await browser.close()

    # حفظ
    if json_data:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print("[تم] data.json")

    if final_results_list:
        pd.DataFrame(final_results_list).to_csv("results.csv", index=False, encoding="utf-8-sig")
        print("[تم] results.csv")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"خطأ عام في التشغيل: {e}")
        raise
