import click
from heapq import heappush, heappushpop
from utils import *

@click.command()
@click.option(
	"-s",
	"--subreddit",
	help="The subreddit to scrape (ex: r/wallstreetbets)",
	required=True
)
def main(subreddit):
	subreddit = format_subreddit(subreddit)

	timestamp = time_ago(days=15)
	posts = fetch_posts_since("uiuc", timestamp)

	ONE_WK = 60 * 60 * 24 * 7
	most_recent = posts[0]["created_utc"]

	heaps = []
	for x in range(7):
		heaps.append([])
	for post in posts:
		score = post["score"]
		created = post["created_utc"]
		weeks_ago = int((most_recent - created) / ONE_WK)

		if weeks_ago <= 6:
			if len(heaps[weeks_ago]) < 5:
				heappush(heaps[weeks_ago], (score, post["title"]))
			else:
				heappushpop(heaps[weeks_ago], (score, post["title"]))

	# sorts the posts by week
	for heap in heaps:
		heap.sort(key=lambda x: x[0], reverse=True)

	for post in heaps[3]:
		print(post)

if __name__ == "__main__":
	main()