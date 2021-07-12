import itertools
import datetime
import pygit2
import humanize

from .decorators import asyncexe


def format_commit(self, commit):
    short, _, _ = commit.message.partition('\n')
    short_sha2 = commit.hex[0:6]
    commit_tz = datetime.timezone(
        datetime.timedelta(minutes=commit.commit_time_offset))
    commit_time = datetime.datetime.fromtimestamp(
        commit.commit_time).astimezone(commit_tz)

    offset = humanize.naturaldelta(commit_time.astimezone(
        datetime.timezone.utc) - datetime.datetime.utcnow())
    return f'[`{short_sha2}`](https://github.com/SuperOrca/apollo/commit/{commit.hex}) {short} ({offset})'


@asyncexe()
def get_last_commits(self, count=3):
    repo = pygit2.Repository('.git')
    commits = list(itertools.islice(
        repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
    return '\n'.join(format_commit(c) for c in commits)
