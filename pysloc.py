#!/usr/bin/python3
from pygit2 import Repository, Signature, Patch
from pygit2.enums import SortMode
from datetime import datetime, timezone, timedelta
from argparse import ArgumentParser

from colorama import Fore

class Commit:
    def __init__(self, msg: str, author: Signature, commit_hash: str, sloc_added, sloc_removed):
        tzinfo = timezone(timedelta(minutes=author.offset))
        dt = datetime.fromtimestamp(float(author.time), tzinfo)

        self.msg = msg
        self.author = author.name
        self.email = author.email
        self.commit_hash = commit_hash
        self.time = dt.strftime("%c %z")

        self.sloc_added = sloc_added
        self.sloc_removed = sloc_removed
        self.sloc_diff = abs(self.sloc_added - self.sloc_removed)

    def __repr__(self):
        return (f"commit {self.commit_hash}\n" +
                f"Author:\t{self.author} <{self.email}>\n" +
                f"Time:\t{self.time}\n" +
                f"Diff:\t+{self.sloc_added} -{self.sloc_removed}\n" +
                f"\t{self.msg}")

class Repo:
    def __init__(self, name: str, path: str, commits: []=[]):
        self.name = name
        self.commits = commits
        self.path = path
        self.sloc_total = 0

    def append_commit(self, commit: Commit):
        self.commits.append(commit)

    def log(self):
        for c in self.commits:
            print(c)

    def __repr__(self):
        return (f"Repository: {self.name}\n" + 
                f"Path: '{self.path}'\n" + 
                f"Commits: {len(self.commits)}\n" + 
                f"Total sloc: {self.sloc_total}\n")

# def line_diffs

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-d", "--directory", help="Specify directory containing git project")
    args = arg_parser.parse_args()

    pygit_repo = Repository(args.directory)
    pygit_repo_commits = []

    repo = Repo("pysloc", args.directory)

    for commit in pygit_repo.walk(pygit_repo.head.target, SortMode.TOPOLOGICAL | SortMode.REVERSE):
        pygit_repo_commits.append(commit)

    # prepend a commit with diff 0 t0 pygit_repo_commits

    for commit, next_commit in zip(pygit_repo_commits, pygit_repo_commits[1:]):
        diff = pygit_repo.diff(commit, next_commit, context_lines=0, interhunk_lines=0) 

        sloc_added = 0
        sloc_removed = 0

        for obj in diff:
            if type(obj) == Patch:
                for hunk in obj.hunks:
                    for line in hunk.lines:
                        if line.new_lineno == -1: 
                            sloc_removed += 1
                        if line.old_lineno == -1: 
                            sloc_added +=1

        repo.append_commit(Commit(
            commit.message, 
            commit.author, 
            commit.hex,
            sloc_added,
            sloc_removed
            ))

    repo.log()
    print(repo)

if __name__ == "__main__":
    main()