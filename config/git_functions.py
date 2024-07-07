from github import Github
from github.GithubException import *
from config.localsettings import ghtoken


def addctxfile(path, message, file, repo="scidata", token=ghtoken):
    """
    Push file update to GitHub repo

    :param path: path to the file in the repo
    :param message: commit message
    :param file: the file contents
    :param repo: the repo name
    :param token: GitHub user token

    return None
    :raises Exception: if file with the specified name cannot be found in the repo
    """

    # get repo
    g = Github(token)
    repoh = g.get_user().get_repo(repo)
    try:
        exists = repoh.get_contents(path)
        result = repoh.update_file(path, message, file, exists.sha)
    except UnknownObjectException:
        try:
            result = repoh.create_file(path, message, file)
        except GithubException as e:
            result = str(e.data)
    if isinstance(result, str):
        status = result
    else:
        status = 'success'
    return status
