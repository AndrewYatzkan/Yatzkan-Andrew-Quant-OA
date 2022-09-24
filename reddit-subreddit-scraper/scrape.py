import click
import json
from heapq import heappush, heappushpop
from utils import *
from post import Post

@click.command()
@click.option(
	"-s",
	"--subreddit",
	help="The subreddit to scrape (ex: r/wallstreetbets)",
)
@click.option(
	"-f",
	"--file",
	help="The file to parse",
)
def main(subreddit, file):
	if not subreddit and not file:
		raise click.ClickException("Must specify subreddit to scrape or file to parse. Run again with --help for more info.")
	if subreddit:
		scrape(subreddit)
	else:
		parse(file)

def parse(file):
	try:
		f = open(file, "r")
		data = f.read()
	except:
		raise click.ClickException(f"Couldn't open file \"{file}\"")
	data = json.loads(data)
	
	for week in data["top_posts"]:
		weeks_ago = week["weeks_ago"]
		posts = week["posts"]
		for post in posts:
			score = post["score"]
			ratio = post["upvote_ratio"]
			replies = post["top_replies"]
			p = Post(post["name"], post["title"], post["author"], int(score * ratio), int(score * (1 - ratio)))
			print(f"Week {weeks_ago + 1} post:", p)
	return file

def scrape(subreddit):
	subreddit = format_subreddit(subreddit)
	print(f"Scraping sub: {subreddit}\n")

	timestamp = time_ago(months=3)
	posts = fetch_posts_since(subreddit, timestamp)
	
	ONE_WK = 60 * 60 * 24 * 7
	most_recent = posts[0]["created_utc"]

	N_WEEKS = 26
	N_TOP_POSTS = 5
	heaps = []
	unique_authors = set()
	posts_dict = {}
	for x in range(N_WEEKS):
		heaps.append([])
	for post in posts:
		post_id = post["name"]
		posts_dict[post_id] = post

		try:
			unique_authors.add(post["author_fullname"])
		except:
			pass # author is [deleted]

		score = post["score"]
		created = post["created_utc"]
		weeks_ago = int((most_recent - created) / ONE_WK)

		if weeks_ago <= N_WEEKS - 1:
			if len(heaps[weeks_ago]) < N_TOP_POSTS:
				heappush(heaps[weeks_ago], (score, post["name"]))
			else:
				heappushpop(heaps[weeks_ago], (score, post["name"]))

	print("\nThere have been", len(unique_authors), "unique authors in the past 3 months.\n")
	data = {"top_posts": []}

	for x in range(len(heaps)):
		heap = heaps[x]
		if (len(heap) == 0):
			continue
		heap.sort(key=lambda x: x[0], reverse=True)
		print(f"Fetching comments for week {x + 1} posts")
		heap = list(map(format_post, heap))
	
		week = {"weeks_ago": x, "posts": heap}
		data["top_posts"].append(week)

	OUTPUT_FILE = "out.json"
	print(f"Results written to {OUTPUT_FILE}\nRerun with `--file {OUTPUT_FILE}` to pretty print the contents")
	with open(OUTPUT_FILE, 'w') as f:
		f.write(json.dumps(data))
if __name__ == "__main__":
	main()
