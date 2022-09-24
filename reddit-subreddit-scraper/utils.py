import json
import requests
import time
from heapq import heappush, heappushpop

def format_subreddit(subreddit):
	if subreddit[:2] == "r/":
		return subreddit[2:]
	return subreddit

def format_post(post_tuple):
	post, comments = list(map(lambda x: x["data"], fetch_post_info(post_tuple[1])))
	post = post["children"][0]["data"]
	comments = comments["children"]

	heap = []
	N_TOP_COMMENTS = 10
	for comment in comments:
		comment = comment["data"]
		try:
			score = comment["score"]
		except:
			continue
		author = comment["author"]
		body = comment["body"]
		if len(heap) < N_TOP_COMMENTS:
			heappush(heap, (score, author, body))
		else:
			heappushpop(heap, (score, author, body))

	post["top_replies"] = heap
	return post

def time_ago(seconds=0, minutes=0, hours=0, days=0, months=0, years=0):
	return time.time() - (seconds + minutes * 60 + hours * 3600 + days * 86400 + months * 2592000 + years * 31536000)

def fetch_post_info(name):
	# formats name correctly
	try:
		idx = name.index("_") + 1
	except:
		idx = 0
	name = name[idx:]

	r = requests.get(f"https://api.reddit.com/comments/{name}.json", headers={"User-Agent": "Subreddit Scraper v0.1"})
	match r.status_code:
		case 200: # success
			return r.json()
		case 429: # rate-limited
			time.sleep(2)
			print("Sleeping 2s")
			return fetch_posts(name)
		case _: # unknown error
			raise Exception(f"Unexpected status code {r.status_code}")

def fetch_posts(sub, after=None, limit=100):
	r = requests.get(f"https://api.reddit.com/r/{sub}/new.json?limit={limit}&sort=new&after={after}", headers={"User-Agent": "Subreddit Scraper v0.1"})
	match r.status_code:
		case 200: # success
			res = r.json()["data"]
			res["children"] = list(map(lambda x: x["data"], res["children"]))
			return res
		case 429: # rate-limited
			time.sleep(2)
			print("Sleeping 2s")
			return fetch_posts(sub, after, limit)
		case _: # unknown error
			raise Exception(f"Unexpected status code {r.status_code}")

def fetch_posts_since(sub, since):
	res = fetch_posts(sub)
	posts = res["children"]
	after = res["after"]
	delta = posts[-1]["created_utc"] - since
	while delta > 0:
		print(f"Fetched {len(posts)} post(s) -- Sifting through {delta // 86400} more day(s) worth of posts..")
		res = fetch_posts(sub, after)
		posts += res["children"]
		after = res["after"]
		if after is None:
			break
		delta = posts[-1]["created_utc"] - since
	return posts