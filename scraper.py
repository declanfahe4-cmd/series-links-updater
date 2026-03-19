import asyncio
import requests
import re
import pandas as pd
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import nest_asyncio

nest_asyncio.apply()

try:
    with open("links.txt", "r", encoding="utf-8") as f:
        post_links = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
except FileNotFoundError:
    print("خطأ: الملف links.txt غير موجود في نفس المجلد!")
    post_links = []  # أو يمكنك إنهاء البرنامج: import sys; sys.exit(1)
except Exception as e:
    print(f"خطأ أثناء قراءة links.txt: {e}")
    post_links = []

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
