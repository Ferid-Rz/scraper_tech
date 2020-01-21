instagram_url = 'https://www.instagram.com'
# profile_url = 'nanna___000'

def get_followers_count(profile_url: str, session):
	response = session.get(f"{instagram_url}/{profile_url}")
	# print(response.status_code)
	if response.ok:
		html = response.text
		bs_html = BeautifulSoup(html,features="html.parser")
		scripts = bs_html.select('script[type="application/ld+json"]')
		scripts_content = json.loads(scripts[0].text.strip())
		main_entity_of_page = scripts_content['mainEntityofPage']
		interaction_statistic = main_entity_of_page['interactionStatistic']
		followers_count = interaction_statistic['userInteractionCount']
		# print(followers_count)
		return followers_count

async def get_followers_async(profiles: list) -> list:
	res = []
	with ThreadPoolExecutor(max_workers=10) as executor:
		with requests.Session() as session:
			loop = asyncio.get_event_loop()
			tasks = [
				loop.run_in_executor(executor,get_followers_count, *(profile,session)) for profile in profiles
			]
			for response in await asyncio.gather(*tasks):
				res.append(response)
	return res

profiles = ['anar.py','thenotoriousmma','arianagrande']

start = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_followers_async(profiles))
res = loop.run_until_complete(future)
end = time.time()
elapsed = end-start
print(res)
# print(f'ASYNC took {elapsed} seconds')
