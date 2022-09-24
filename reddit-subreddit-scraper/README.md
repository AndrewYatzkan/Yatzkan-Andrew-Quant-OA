# Reddit Subreddit Scraper

## Usage

Run the executable with the following arguments:

`-s, --subreddit` - Specify the subreddit to scrape (use the format `r/subreddit_name`)
`-f, --file` - Specify the file to parse and display the results of

You may specify either the `subreddit` or the `file` argument, but not both.

## Description

Scrapes the specified subreddit for posts made in the past 3 months. The script will then filter for for the top 5 posts made in each week, and download the top 10 comments for each of these posts. Results are written to a JSON file.

To view the results, rerun the script with the `--file` argument and the name of the output file.

## Future Improvements

- Use unofficial API like Pushshift.io that has data cached to fetch relevant info in fewer requests
- Increase customizability by letting the user pass in more arguments
- Send multiple requests at once to speed up process
- Print the data in a cleaner way, potentially involving some sort of data visualization