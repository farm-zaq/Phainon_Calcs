import os

import base_data
import generate_teams
import csv
 
def score_team(team, lc="Fall", atk_boots=False):
  team_buffs = team + ["Phainon", "relics", "generic_st"] + [lc]

  if atk_boots:
    team_buffs += ["atk_boots"]
 
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
 
  if team[0] not in base_data.st_buffers and team[1] == "Bronya" and team[2] == "RMC":
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

  if team == ["Sunday", "Bronya"]:
    print("ATK:\t\t", atk_mult)
    print("Extra Percent:\t", team_stats["p"])
    print("CD:\t\t", 100 * (crit_mult - 1))
 
  score = atk_mult * crit_mult * p_mult * res_mult * def_mult * vuln_mult * td_mult
  return score

def get_coreflame(team, atk_boots):
  lost_turns = 0
  full_advances = 0
  half_advances = 0
  sp = 4
  good_sp = 4
  extra_users = 0
  stacks = 1
  has_robin = "Robin" in team
  for name in team:
    if base_data.rotation_data[name]["aa"] == "always":
      full_advances += 1
      if has_robin:
        full_advances += 1
    elif base_data.rotation_data[name]["aa"] == "once":
      full_advances += 1
    elif base_data.rotation_data[name]["aa"] == "atk_boots":
      half_advances += 1
      if has_robin:
        half_advances += 1
    elif base_data.rotation_data[name]["aa"] == "team":
      full_advances += 1

    sp += base_data.rotation_data[name]["sp"]
    good_sp += base_data.rotation_data[name]["good_sp"]
    stacks += base_data.rotation_data[name]["stacks"]
    if has_robin:
      sp += base_data.rotation_data[name]["robin_sp"]
      good_sp += base_data.rotation_data[name]["good_robin_sp"]
      stacks += base_data.rotation_data[name]["robin_stacks"]

    if base_data.rotation_data[name]["can_use_extra"] == "Always":
      extra_users += 1
      if has_robin:
        extra_users += 1
    if base_data.rotation_data[name]["can_use_extra"] == "Once" and has_robin:
      extra_users += 1
  
  if full_advances > 0 and half_advances == 0 and atk_boots:
    lost_turns += 1
    if has_robin:
      lost_turns = 2
  
  good_stacks = stacks
  
  phainon_turns = 1 + full_advances - lost_turns
  sp += phainon_turns
  good_sp += phainon_turns

  all_skills = phainon_turns >= sp//2
  skills = min(phainon_turns, sp//2)
  all_good_skills = phainon_turns >= good_sp//2
  good_skills = min(phainon_turns, good_sp//2)

  sp -= skills * 2
  good_sp -= good_skills * 2
  stacks += skills * 2
  good_stacks += good_skills * 2
  
  if has_robin and sp >= 1 and not all_skills and ("Bronya" in team or "Sunday" in team):
    sp -= 1
    stacks += 1
  if has_robin and good_sp >= 1 and not all_good_skills and ("Bronya" in team):
    good_sp -=1
    good_stacks += 1

  stacks += min(extra_users, sp//2)
  good_stacks += min(extra_users, good_sp//2)

  return [stacks, good_stacks]
 
def output_teams(teams, file_name, limit=None):
  filtered_teams = []
  for team in teams:
    team_name = generate_teams.get_team_name(team)
    image_url = f'=IMAGE("{base_data.image_urls[team_name]}")'
    score = score_team(team)
    percent = int(score/baseline_score * 100)
    spd_stacks = get_coreflame(team, False)
    atk_stacks = get_coreflame(team, True)
    atk_boot_score = score_team(team, atk_boots=True)
    atk_boot_percent = int(atk_boot_score/baseline_score * 100)
    team_row = [team_name, image_url, percent] + spd_stacks + [atk_boot_percent] + atk_stacks
    filtered_teams.append(team_row)
  filtered_teams = sorted(filtered_teams, key=lambda x: x[2], reverse=True)
  for i in range(len(filtered_teams)):
    filtered_teams[i][2] = f"{filtered_teams[i][2]}%"
    filtered_teams[i][5] = f"{filtered_teams[i][5]}%"
  for i in range(len(filtered_teams)):
    filtered_teams[i] = filtered_teams[i][0:2] + [""] + filtered_teams[i][2:5] + [""] + filtered_teams[i][5:]
  filtered_teams = [["", "Team", "", "Damage\n(Spd Boots)", "Coreflame\n(Spd Boots)", "Max Coreflame\n(Spd Boots)", "", "Damage\n(Atk Boots)", "Coreflame\n(Atk Boots)", "Max Coreflame\n(Atk Boots)"]] + filtered_teams
  filtered_teams = [row[1:] for row in filtered_teams]
  if limit:
    filtered_teams = filtered_teams[:limit+1]
  
  folder_path = "output/csvs"
  os.makedirs(folder_path, exist_ok=True)
  
  with open(f"{folder_path}/{file_name}.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerows(filtered_teams)

if __name__ == "__main__":
  baseline_score = score_team(["Bronya", "RMC", "Tingyun"])

  grouped_teams = generate_teams.generate_grouped_teams()
  for group in grouped_teams:
    output_teams(group[1], group[0])

  ungrouped_teams = generate_teams.generate_ungrouped_teams()
  output_teams(ungrouped_teams, "top_ten", limit=10)

  score_team(["Sunday", "Bronya"])