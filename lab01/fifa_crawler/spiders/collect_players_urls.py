import scrapy

class collect_player_url(scrapy.Spider):
  name='players_urls' 
  
  def start_requests(self):
    urls = ['https://sofifa.com/players?col=oa&sort=desc&offset=0']
    
    # YOUR CODE HERE
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    for i in range(1,13):
        url = f'https://sofifa.com/players?col=oa&sort=desc&offset={i}' 
        urls.append(url)

    for url in urls:
      yield scrapy.Request(url=url, headers=headers, callback=self.parse)

  def parse(self, response):
    player_urls = response.css('td.col-name a[role="tooltip"]::attr(href)').extract()
    player_ids = []
    for url in player_urls:
      if url.split('/')[1] == "player":
        player_id = url.split('/')[2]
        player_url = f"/player/{player_id}"
        player_item = {"player_url": player_url}
        yield player_item