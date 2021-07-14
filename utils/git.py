def format_commit(commit):
    return f"[`{commit['sha'][:7]}``]({commit['html_url']}) {commit['commit']['message']}"


async def get_last_commits(bot, count=3):
    commits = await (await bot.session.get("https://api.github.com/repos/SuperOrca/apollo/commits")).json()
    return '\n'.join(format_commit(c) for c in commits[:count])
