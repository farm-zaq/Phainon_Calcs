import re
import requests
import os
from dotenv import load_dotenv

def get_file_name_from_public_url(url, api_key):
    match = re.search(r'(?:/d/|id=)([a-zA-Z0-9_-]{25,})', url)
    if not match:
        print("Invalid URL format")
        return None

    file_id = match.group(1)

    endpoint = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name&key={api_key}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        file_name = response.json().get("name")
        return file_name
    else:
        print(f"Error: {response.status_code} - {response.text}")
        a = 0/0
        return None

load_dotenv()
api_key = os.getenv("api_key")

urls = [
  "https://drive.google.com/file/d/11pQ0QnTl9yjmbxMmJsfetnOnCsejQ0aP/view?usp=sharing",
  "https://drive.google.com/file/d/15Rbxij31XZUGkRAAfOgwbyQD3HzJrCz8/view?usp=sharing",
  "https://drive.google.com/file/d/15wAZu3sz0mCO4Fxf9VwEkculRIa3yjL7/view?usp=sharing",
  "https://drive.google.com/file/d/18WYAVldI_yinKOLEMtnP9mLgvlBWbShK/view?usp=sharing",
  "https://drive.google.com/file/d/18l6xjvi3rV90HSNX5r9NT78QRDexg74J/view?usp=sharing",
  "https://drive.google.com/file/d/19L6xaGQ3Je7QzkDecmHdR4kMHh-ZCLKU/view?usp=sharing",
  "https://drive.google.com/file/d/19iTGUBhNDlgGeTc6O2DW8B7qPFyrm00R/view?usp=sharing",
  "https://drive.google.com/file/d/1A8likDCNT9BL5fEllgOcoWyejuI_NhrK/view?usp=sharing",
  "https://drive.google.com/file/d/1BR0ZMwLGAHMmnMpHUIU4YQAJb6NRcoxc/view?usp=sharing",
  "https://drive.google.com/file/d/1BRIOqajL9pGdaot5u0vCtrJqQdFQaatO/view?usp=sharing",
  "https://drive.google.com/file/d/1DZG--cIH7YA_rO2_iw3VI8PHs2x_c1mP/view?usp=sharing",
  "https://drive.google.com/file/d/1HNVEdFrQ3yQTLhqFGtlwiNJz-4o38fbF/view?usp=sharing",
  "https://drive.google.com/file/d/1HqqX-ZluSA0nr7CSuUfQYTn6S6h2awil/view?usp=sharing",
  "https://drive.google.com/file/d/1IFnc7AtB3vMZR1gCD1gvBsvbdkVpREDS/view?usp=sharing",
  "https://drive.google.com/file/d/1NsgMcDi-lwNaYbrD1E9v1Cjk588RmJrD/view?usp=sharing",
  "https://drive.google.com/file/d/1OYMb1gwRdQLMnTGeZQYyLWCfyHq6ep5t/view?usp=sharing",
  "https://drive.google.com/file/d/1ULMCGjmzySajLv3CM9SJSw52wEA7dDPY/view?usp=sharing",
  "https://drive.google.com/file/d/1WNcqP0vJaqRpzToZN6qL2hNpU_dOEyKF/view?usp=sharing",
  "https://drive.google.com/file/d/1WPk8RMw7PTWZEQ1zUjDFOdDbujWYwNoR/view?usp=sharing",
  "https://drive.google.com/file/d/1cTdOrH0IYMfjmVMROmNnE52ybX73eVAK/view?usp=sharing",
  "https://drive.google.com/file/d/1e4BAXIagMp-8ePFPcOj1vXFqq1TaUlxj/view?usp=sharing",
  "https://drive.google.com/file/d/1f3RGVTIIWSU3ojaIb0sXsNy_Ul4jUjXz/view?usp=sharing",
  "https://drive.google.com/file/d/1ief6Y7Sqv2SIwluFNiNq2eZI_8n_zPpg/view?usp=sharing",
  "https://drive.google.com/file/d/1mHyQjUGvqPZTY5dyq7ty7KtVPBpGL1fz/view?usp=sharing",
  "https://drive.google.com/file/d/1qO-yQPT8W5Vd9l3SCubQi1NMPe1negm4/view?usp=sharing",
  "https://drive.google.com/file/d/1qP4lij2M4L8xrozFq51o6bFC-HX96fk3/view?usp=sharing",
  "https://drive.google.com/file/d/1qh0ursxl8VADFvGZucyIIrjR9mLoZ723/view?usp=sharing",
  "https://drive.google.com/file/d/1rVO0azIKQzulpiyiC_vm5QDJmmYtd2ce/view?usp=sharing",
  "https://drive.google.com/file/d/1u787SPEgp3Fi9raf-ZCk99U9_jAit1a2/view?usp=sharing",
  "https://drive.google.com/file/d/1wmLn86Vk_9Pw9Kol_CnCGAk6yHuwA4Yd/view?usp=sharing",
  "https://drive.google.com/file/d/1wqUeIRRHlqXkibmImcF0IM2xbVVv3G5d/view?usp=sharing",
  "https://drive.google.com/file/d/1xZ-SNAbFdGlTZS3nTtVYZuKmxYkceupc/view?usp=sharing",
  "https://drive.google.com/file/d/1y0OadfitZSFMkQN8KyLpmlV9aSE6Iqyy/view?usp=sharing",
  "https://drive.google.com/file/d/1yV5iJffU1905qQCBnotOwy_AIxgWRqiI/view?usp=sharing",
  "https://drive.google.com/file/d/1yk7qrIMIq7OmM-_sff9VBjKKX8jnLnXD/view?usp=sharing"
]

if __name__ == "__main__":
  for url in urls:
    file_name = get_file_name_from_public_url(url, api_key)
    print(f'"{file_name}": "{url}",')
