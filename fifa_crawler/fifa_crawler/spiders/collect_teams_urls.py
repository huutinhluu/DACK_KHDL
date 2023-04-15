import scrapy

class collect_team_url(scrapy.Spider):
  name='teams_urls' 
  
  def start_requests(self):
    urls = ['https://sofifa.com/teams?col=oa&sort=desc&offset=0']
    
    # YOUR CODE HERE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    for i in range(1,13):
        url = f'https://sofifa.com/teams?col=oa&sort=desc&offset={i*60}' 
        urls.append(url)

    for url in urls:
      yield scrapy.Request(url=url, headers=headers, callback=self.parse)

  def parse(self, response):
    team_urls = response.css('td.col-name-wide a::attr(href)').extract()
    team_ids = []
    for url in team_urls:
      if url.split('/')[1] == "team":
        team_id = url.split('/')[2]
        team_url = f"/team/{team_id}"
        team_item = {"team_url": team_url}
        yield team_item