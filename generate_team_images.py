import os
from PIL import Image

import generate_teams

def generate_team_image(team):
  input_folder = "../../Chibis"
  output_folder = "../../chibi_teams"
  name = generate_teams.get_team_name(team)
  path = os.path.join(output_folder, f"{name}.png")

  if os.path.exists(path):
    print(f"An image for {name} already exists")
    return
  
  images = [Image.open(f"{input_folder}/Phainon.png").convert('RGBA')]
  for char in team:
    images.append(Image.open(f"{input_folder}/{char}.png").convert('RGBA'))

  width = 256
  height = 256
  image_size = (width, height)

  combo_width = image_size[0] * 2
  combo_height = image_size[1] * 2

  new_img = Image.new('RGBA', (combo_width, combo_height), (255, 255, 255, 0))

  new_img.paste(images[0], (0, 0))
  new_img.paste(images[1], (image_size[0], 0))
  new_img.paste(images[2], (0, image_size[1]))
  new_img.paste(images[3], (image_size[0], image_size[1]))

  output_path = os.path.join(output_folder, f"{name}.png")
  new_img.save(output_path)

  print(f"Team image created at {output_path}")

def make_all_team_images():
  ungrouped_teams = generate_teams.generate_ungrouped_teams()
  for team in ungrouped_teams:
    generate_team_image(team)

if __name__ == "__main__":
  make_all_team_images()