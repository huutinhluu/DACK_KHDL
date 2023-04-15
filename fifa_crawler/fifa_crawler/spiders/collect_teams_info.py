import scrapy
import json
import re
import datetime

class collect_team_info(scrapy.Spider):
  name='teams_info'
  
  def __init__(self):
    try:
      with open('dataset/teams_urls.json') as f:
        self.teams = json.load(f)
      self.team_count = 1
    except IOError:
      print("File not found")

  def start_requests(self):
    # YOUR CODE HERE
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    for team in self.teams:
      url = 'https://sofifa.com' + team['team_url'] + '?units=mks'
      yield scrapy.Request(url=url, headers=headers, callback=self.parse)
  
  def parse(self, response):
      # YOUR CODE HERE
      team_info = {}

      team_info["Name"] = response.css('div.info h1::text').get();

      team_info["League"] = response.css('div.meta.ellipsis a::text').get()

      ratings = response.css('section.card .bp3-tag.p::text').getall()

      team_info["Overall"] = ratings[0]

      team_info["Attack"] = ratings[1]
      
      team_info["Midfield"] = ratings[2]
      
      team_info["Defence"] = ratings[3]

      team_info["Home stadium"] = response.css('ul.pl li.ellipsis:contains("Home stadium")::text').get()
      
      team_info["Rival team"] = response.css('ul.pl li:contains("Rival team") a::text').get()

      team_info["International prestige"] = response.css('ul.pl li:contains("International prestige") span::text').get()

      team_info["Domestic prestige"] = response.css('ul.pl li:contains("Domestic prestige") span::text').get()

      team_info["Club worth"] = response.css('ul.pl li:contains("Club worth")::text').get()

      team_info["Starting XI average age"] = response.css('ul.pl li:contains("Starting XI average age")::text').get()

      team_info["Whole team average age"] = response.css('ul.pl li:contains("Whole team average age")::text').get()

      team_info["Captain"] = response.css('ul.pl li:contains("Captain") a::text').get()

      team_info["Short free kick"] = response.css('ul.pl li:contains("Short free kick") a::text').get()

      team_info["Long free kick"] = response.css('ul.pl li:contains("Long free kick") a::text').get()

      team_info["Left short free kick"] = response.css('ul.pl li:contains("Left short free kick") a::text').get()
      
      team_info["Right short free kick"] = response.css('ul.pl li:contains("Right short free kick") a::text').get()
      
      team_info["Penalties"] = response.css('ul.pl li:contains("Penalties") a::text').get()
      
      team_info["Left corner"] = response.css('ul.pl li:contains("Left corner") a::text').get()
      
      team_info["Right corner"] = response.css('ul.pl li:contains("Right corner") a::text').get()

      yield team_info