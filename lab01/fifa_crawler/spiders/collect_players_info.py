import scrapy
import json
import re
import datetime

class collect_player_info(scrapy.Spider):
  name='players_info'
  
  def __init__(self):
    try:
      with open('dataset/players_urls.json') as f:
        self.players = json.load(f)
      self.player_count = 1
    except IOError:
      print("File not found")

  def start_requests(self):
    urls = ['https://sofifa.com/player/231747?units=mks']
    # YOUR CODE HERE
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    for player in self.players:
      url = 'https://sofifa.com' + player['player_url'] + '?units=mks'
      yield scrapy.Request(url=url, headers=headers, callback=self.parse)
  
  def parse(self, response):
      # YOUR CODE HERE
      id = response.css('li:contains("ID")::text').get().strip()
      name = response.css('div.info h1::text').get()
      primary_position = response.css('ul.pl li:nth-child(1) span.pos::text').get()
      positions = []
      for pos in response.css('ul.ellipsis.pl li span.pos::text').getall():
        positions.append(pos)
      # extract age, date of birth, height, and weight
      meta_info = response.css('div.info div.meta.ellipsis::text').getall()
      # Assuming that meta_info is already defined
      age = re.search(r'(\d{2})y\.o\.', meta_info[1]).group(1)
      birth_date = datetime.datetime.strptime(re.search(r'\((.*?)\)', meta_info[1]).group(1), '%b %d, %Y').strftime('%Y/%b/%d')
      height = int(re.search(r'(\d{3})cm', meta_info[1]).group(1))
      weight = int(re.search(r'(\d{2,3})lbs', meta_info[1]).group(1))
      overall_rating = int(response.css('section.card.spacing div.block-quarter:nth-child(1) span.p::text').get())
      potential = response.css('section.card.spacing div.block-quarter:nth-child(2) span.p::text').get()
      value = response.css('div.block-quarter:nth-child(3) div::text').get().strip()
      wage = response.css('div.block-quarter:nth-child(4) div::text').get().strip()
      preferred_foot = response.css('li.ellipsis:contains("Preferred Foot")::text').get().strip().replace("Preferred Foot", "")
      weak_foot = int(response.css('li.ellipsis:contains("Weak Foot")::text').get().strip()[0])
      skill_moves = int(response.css('li.ellipsis:contains("Skill Moves")::text').get().strip()[0])
      international_reputation = int(response.css('li.ellipsis:contains("International Reputation")::text').get().strip()[0])
      work_rate = response.css('li:contains("Work Rate") span::text').get()
      body_type = response.css('ul.pl li:contains("Body Type") span::text').get()
      real_face = response.css('ul.pl li:contains("Real Face") span::text').get()
      release_clause = response.css('ul.pl li:contains("Release Clause") span::text').get()
      teams = dict(zip(response.css('div.card h5 a::text').getall(), response.css('ul.ellipsis.pl li span.bp3-tag.p::text').getall()))
      stats_names =  response.css('div.grid div.block-quarter div.card h5::text').getall()
      stats_values = response.css('div.card ul.pl li span.bp3-tag::text').getall()
      stats_keys = response.css('div.card ul.pl li span[role="tooltip"]::text').getall()
      attacking = dict(zip(stats_keys[0:4],list(map(int, stats_values[0:4]))))
      skill = dict(zip(stats_keys[5:9],list(map(int, stats_values[5:9]))))
      movement = dict(zip(stats_keys[10:14],list(map(int, stats_values[10:14]))))
      power = dict(zip(stats_keys[15:19],list(map(int, stats_values[15:19]))))
      mentality = dict(zip(stats_keys[20:25],list(map(int, stats_values[20:25]))))
      defending = dict(zip(stats_keys[26:28],list(map(int, stats_values[26:28]))))
      goalkeeping = dict(zip(stats_keys[29:33],list(map(int, stats_values[29:33]))))
      player_traits = stats_keys[34:38]
      player_specialities = response.css('div.card ul.pl li a::text').getall()
        
      player_info = {
        "id": id,
        "name": name.encode('unicode_escape').decode(),
        "primary_position": primary_position,
        "positions": positions,
        "age": age,
        "birth_date":birth_date,
        "height": height, 
        "weight": weight,
        "Overall Rating": overall_rating,
        "Potential": potential,
        "Value": value.encode('unicode_escape').decode(), 
        "Wage": wage.encode('unicode_escape').decode(),
        "Preferred Foot": preferred_foot,
        "Weak Foot": weak_foot,
        "Skill Moves":skill_moves,
        "International Reputation": international_reputation,
        "Work Rate": work_rate,
        "Body Type": body_type,
        "Real Face": real_face,
        "Release Clause": release_clause.encode('unicode_escape').decode(),
        "teams": teams,
        "attacking": attacking,
        "skill": skill,
        "power": power,
        "mentality": mentality,
        "defending": defending,
        "goalkeeping": goalkeeping,
        "player_traits": player_traits,
        "player_specialities": player_specialities
        }
      yield player_info