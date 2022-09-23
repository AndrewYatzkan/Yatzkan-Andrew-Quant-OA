def format_subreddit(subreddit):
	prefix = "r/"
	if subreddit[:2] == prefix:
		return subreddit
	return prefix + subreddit