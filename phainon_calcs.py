import os

import base_data
import generate_teams
 
def score_team(team, lc="Fall"):
  team_buffs = team + ["Phainon", "relics", "generic_st"] + [lc]
 
  team_stats = {
    "base_atk": 0.0,
    "atk_p": 0.0,
    "atk": 0.0,
    "p": 0.0,
    "cr": 0.0,
    "cd": 0.0,
    "res": 0.0,
    "res_pen": 0.0,
    "def_shred": 0.0,
    "vuln": 0.0,
    "true_dmg": 0.0
  }
 
  for buff_name in team_buffs:
    buff = base_data.buffs[buff_name]
    for stat_name in team_stats:
      if stat_name in buff:
        team_stats[stat_name] += buff[stat_name]
 
  atk_mult = team_stats["base_atk"] * (1 + team_stats["atk_p"]/100) + team_stats["atk"]
 
  if team[0] not in base_data.st_buffers and team[1] == "Bronya" and team[2] == "RMC" and "Robin" not in team:
    team_stats["cd"] -= 18
  if team_stats["cr"] > 100:
    team_stats["cd"] +=  (team_stats["cr"] - 100) * 2
    team_stats["cr"] = 100
  crit_mult = 1 + (team_stats["cr"]/100 * team_stats["cd"]/100)
 
  p_mult = team_stats["p"]/100 + 1
  res_mult = 1.0 - team_stats["res"]/100 + team_stats["res_pen"]/100
  def_mult = 100/(115 * (1 - team_stats["def_shred"]/100) + 100)
  vuln_mult = 1.0 + team_stats["vuln"]/100
  td_mult = 1.0 + team_stats["true_dmg"]/100
 
  score = atk_mult * crit_mult * p_mult * res_mult * def_mult * vuln_mult * td_mult
  return score
 
def output_teams(teams, file_name, limit=None):
  filtered_teams = []
  for team in teams:
    team_name = generate_teams.get_team_name(team)
    image_url = f'=IMAGE("{base_data.image_urls[team_name]}")'
    score = score_team(team)
    percent = int(score/baseline_score * 100)
    if team_name in base_data.stacks:
      stack_rows = base_data.stacks[team_name]
    else:
      stack_rows = ["?", "?"]
    filtered_teams.append([team_name, image_url, percent] + stack_rows)
  filtered_teams = sorted(filtered_teams, key=lambda x: x[2], reverse=True)
  for i in range(len(filtered_teams)):
    filtered_teams[i][2] = f"{filtered_teams[i][2]}%"
  filtered_teams = [["", "Team", "Damage", "Coreflame", "Max Coreflame"]] + filtered_teams
  filtered_teams = [row[1:] for row in filtered_teams]
  if limit:
    filtered_teams = filtered_teams[:limit+1]
  
  folder_path = "output/csvs"
  os.makedirs(folder_path, exist_ok=True)

  with open(f"{folder_path}/{file_name}.csv", "w", newline="") as file:
    for row in filtered_teams:
        line = ",".join(str(cell) for cell in row)
        file.write(line + "\n")

if __name__ == "__main__":
  baseline_score = score_team(["Bronya", "RMC", "Tingyun"])

  grouped_teams = generate_teams.generate_grouped_teams()
  for group in grouped_teams:
    output_teams(group[1], group[0])

  ungrouped_teams = generate_teams.generate_ungrouped_teams()
  output_teams(ungrouped_teams, "top_ten", limit=10)