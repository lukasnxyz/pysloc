#!/usr/bin/python3
from pygit2 import Repository, Signature
from pygit2.enums import SortMode
from datetime import datetime, timezone, timedelta
from argparse import ArgumentParser

class Commit:
    def __init__(self, msg: str, author: Signature, commit_hash: str):
        tzinfo = timezone(timedelta(minutes=author.offset))
        dt = datetime.fromtimestamp(float(author.time), tzinfo)

        self.msg = msg
        self.author = author.name
        self.commit_hash = commit_hash
        self.time = dt.strftime("%c %z")

        self.sloc_added = 0
        self.sloc_removed = 0
        self.sloc_diff = abs(self.sloc_added - self.sloc_removed)

    def __repr__(self):
        return f"commit {self.commit_hash}\nAuthor:\t{self.author}\nTime:\t{self.time}\n\t{self.msg}"

class Repo:
    def __init__(self, name: str, path: str, commits: []=[]):
        self.name = name
        self.commits = commits
        self.path = path

    def append_commit(self, commit: Commit):
        self.commits.append(commit)

    def log(self):
        for c in self.commits:
            print(c)

    def __repr__(self):
        return f"Name: {self.name}\nPath: '{self.path}'\nCommits: {len(self.commits)}"

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-d", "--directory", help="Specify directory containing git project")
    args = arg_parser.parse_args()

    pygit_repo = Repository(args.directory)
    repo = Repo("pysloc", args.directory)

    # handle this in Repo constructor?
    for commit in pygit_repo.walk(pygit_repo.head.target, SortMode.TOPOLOGICAL | SortMode.REVERSE):
        repo.append_commit(Commit(
            commit.message, 
            commit.author, 
            commit.hex
        ))

    repo.log()
    print(repo)

if __name__ == "__main__":
    main()
