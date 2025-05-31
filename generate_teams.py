import base_data

def generate_grouped_teams():
  base_data.st_buffers = ["Sunday", "Sparkle", "Bronya", "RMC", "Tingyun"]
  nt_buffers = ["Cipher", "Tribbie", "Jiaoqiu", "RuanMei", "Yukong"]
  nt_buffers_w_robin = ["Robin"] + nt_buffers
  sustains = ["Aventurine", "FuXuan", "Huohuo", "Gallagher"]

  grouped_teams = []

  st_teams = []
  for i in range(len(base_data.st_buffers)):
    for j in range(i+1, len(base_data.st_buffers)):
      for k in range(j+1, len(base_data.st_buffers)):
        team = [base_data.st_buffers[i], base_data.st_buffers[j], base_data.st_buffers[k]]
        st_teams.append([base_data.st_buffers[i], base_data.st_buffers[j], base_data.st_buffers[k]])
  grouped_teams.append(["st", st_teams])

  for i in range(len(nt_buffers)):
    nt_buffers_teams = []
    for j in range(len(base_data.st_buffers)):
      for k in range(j+1, len(base_data.st_buffers)):
        team = [nt_buffers[i], base_data.st_buffers[j], base_data.st_buffers[k]]
        nt_buffers_teams.append(team)
    grouped_teams.append([nt_buffers[i], nt_buffers_teams])

  robin_teams = []
  for i in range(len(nt_buffers)):
    for j in range(len(base_data.st_buffers)):
      team = ["Robin", nt_buffers[i], base_data.st_buffers[j]]
      robin_teams.append(team)
  grouped_teams.append(["Robin", robin_teams])

  for i in range(len(sustains)):
    sustains_teams = []
    for j in range(len(base_data.st_buffers)):
      for k in range(len(nt_buffers_w_robin)):
        team = [nt_buffers_w_robin[k], base_data.st_buffers[j], sustains[i]]
        sustains_teams.append(team)
    grouped_teams.append([sustains[i], sustains_teams])

  return grouped_teams

def generate_ungrouped_teams():
  grouped_teams = generate_grouped_teams()
  ungrouped_teams = [item for row in grouped_teams for item in row[1]]
  return ungrouped_teams

def get_team_name(team):
  return "-".join(team)