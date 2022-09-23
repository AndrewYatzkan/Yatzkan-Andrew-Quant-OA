import click
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
	print(subreddit)

if __name__ == "__main__":
	main()
