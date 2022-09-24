from dataclasses import dataclass, field
# from pprint import pprint

@dataclass(frozen=True, order=True, unsafe_hash=True)
class Post:
	name: str
	title: str
	author: str
	upvotes: int
	downvotes: int