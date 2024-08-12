import argparse
import asyncio
import sys

from . import __version__
from .github import Stars


async def dump_starred_repos(username: str):
    stars = await Stars(username).fetch()
    if not stars:
        sys.exit(f"No starred repositories found for {username}")

    for repo in stars:
        print(f"- [{repo.name}]({repo.html_url}) - {repo.description} ({', '.join(repo.topics)}))")


def main():
    parser = argparse.ArgumentParser(
        description="Download all starred repositories into a markdown file.",
        argument_default=argparse.SUPPRESS,
    )
    # Global arguments
    parser.add_argument(
        "--username",
        help="Define a github username to fetch starred repositories",
    )
    parser.add_argument(
        "--version",
        help="Print version information and quite",
        action="version",
        version=__version__,
    )

    try:
        args = parser.parse_args()
        if not vars(args):
            return parser.print_help()
    except Exception as e:
        sys.exit(f"Error: {e}")

    asyncio.run(dump_starred_repos(args.username))


if __name__ == "__main__":
    main()
