import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pdf2image import convert_from_path
from PIL import Image, ImageChops, ImageOps
import pprint

def export_sheet(gid, title):
  export_url = (
    f"https://docs.google.com/spreadsheets/d/{file_id}/export?"
    f"format=pdf"
    f"&gid={gid}"
    f"&portrait=false"
    f"&size=tabloid"
    f"&fitw=true"
    f"&sheetnames=false"
    f"&printtitle=false"
    f"&pagenumbers=false"
    f"&gridlines=false"
    f"&fzr=true"
    f"&horizontal_alignment=CENTER"
    f"&top_margin=0.50&bottom_margin=0.50&left_margin=0.50&right_margin=0.50"
    f"&scale=3"
  )

  headers = {'Authorization': f'Bearer {creds.token}'}
  response = requests.get(export_url, headers=headers)

  while response.status_code != 200 and attempts < 10:
    print(f"Failed: {response.status_code} - {response.text}")
    response = requests.get(export_url, headers=headers)
    attempts += 1
  if response.status_code == 200:
      print("200")
      with open(f'output/pdfs/{title}.pdf', 'wb') as f:
          f.write(response.content)
      print(f"PDF for {title} downloaded successfully.")
  else:
      print(f"Failed: {response.status_code} - {response.text}")

def convert_sheet(title):
  pages = convert_from_path(f'output/pdfs/{title}.pdf', dpi=400)  # increase dpi for better quality
  img = pages[0]

  img_rgb = img.convert("RGB")

  bg = Image.new(img_rgb.mode, img_rgb.size, (255, 255, 255))
  diff = ImageChops.difference(img_rgb, bg)
  bbox = diff.getbbox()

  if bbox:
      cropped_img = img_rgb.crop(bbox)
  else:
      cropped_img = img_rgb
  
  width, _ = cropped_img.size
  top_padding = int(width * 0.03333333333)
  padded_img = ImageOps.expand(cropped_img, border=(0, top_padding, 0, 0), fill="white")

  padded_img.save(f'output/pngs/{title}.png')

SCOPES = ['https://www.googleapis.com/auth/drive.readonly', "https://www.googleapis.com/auth/spreadsheets.readonly"]

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

file_id = '1n-nixpUFCcMkaTtZACKLvRN-b9RdAl8h8QjD5auy_sE'

service = build("sheets", "v4", credentials=creds)
sheet_metadata = service.spreadsheets().get(spreadsheetId=file_id).execute()
sheets = sheet_metadata.get("sheets", [])
for sheet in sheets:
  gid = sheet["properties"]["sheetId"]
  title = sheet["properties"]["title"]
  export_sheet(gid, title)
  convert_sheet(title)
