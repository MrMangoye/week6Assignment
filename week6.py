import os
import requests
from urllib.parse import urlparse
from uuid import uuid4

def get_image_filename(url):
    """Extract filename from URL or generate one if missing."""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename or '.' not in filename:
        filename = f"image_{uuid4().hex}.jpg"
    return filename

def download_image(url, save_dir="Fetched_Images"):
    """Download image from URL and save it to the specified directory."""
    os.makedirs(save_dir, exist_ok=True)  # ✅ Requirement 3

    try:
        response = requests.get(url, timeout=10)  # ✅ Requirement 1
        response.raise_for_status()              # ✅ Requirement 2

        filename = get_image_filename(url)       # ✅ Requirement 4
        filepath = os.path.join(save_dir, filename)

        with open(filepath, "wb") as f:          # ✅ Requirement 5
            f.write(response.content)

        print(f"✅ Image saved as '{filename}' in '{save_dir}'.")

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Please check your internet or the URL.")
    except requests.exceptions.Timeout:
        print("⏳ Request timed out. Try again later.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

if __name__ == "__main__":
    print("🌍 Welcome to the Ubuntu Image Fetcher!")
    image_url = input("🔗 Enter the image URL: ").strip()
    download_image(image_url)