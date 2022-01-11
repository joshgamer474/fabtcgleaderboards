import json

class LeaderboardData:
  def __init__(self, rank, country, name, xp, date):
    self.rank = rank
    self.country = country
    self.name = name
    self.xp = xp
    self.date = date
  
  def to_json(self):
    data = {}
    data['rank'] = self.rank
    data['country'] = self.country
    data['name'] = self.name
    data['xp'] = self.xp
    data['date'] = self.date
    return json.dumps(data, default=str).encode('utf-8')

  def __repr__(self):
    return f"rank: {self.rank}, country: {self.country}, name: {self.name}, xp: {self.xp}, date: {self.date}"
  def __str__(self):
    return f"rank: {self.rank}, country: {self.country}, name: {self.name}, xp: {self.xp}, date: {self.date}"