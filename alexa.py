"""
File: alexa

Description:
Primary Author(s): Michael Clawar
Secondary Author(s):

Notes:

January 14, 2017
StratoDem Analytics, LLC
"""

from flask import Flask
from flask_ask import Ask, statement

from github_scraper import get_top_repositories

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('TopRepositoriesIntent')
def top_repositories(language, period):
    top_repos = get_top_repositories(language=language, period=period)

    text_response = """
    The top repositories for {language} {period} were {repos}.""".format(
        language=language,
        period=period,
        repos='. '.join([
            '{rank}. {repo_name}, which describes itself as {repo_description}'.format(
                rank=idx + 1, repo_name=repo_info['repository'],
                repo_description=repo_info['description']
            ) for idx, repo_info in enumerate(top_repos[:10])])).strip()

    return statement(text_response)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
