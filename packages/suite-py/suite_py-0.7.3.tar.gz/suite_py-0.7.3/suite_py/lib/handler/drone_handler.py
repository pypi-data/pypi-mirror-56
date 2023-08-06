from ..tokens import Tokens
import requests

tokens = Tokens()
baseurl = "https://drone-1.prima.it"


def get_last_build_url(repo):
    try:
        resp = requests.get("{}/api/repos/primait/{}/builds/latest".format(baseurl, repo),
                            headers={'Authorization': 'Bearer {}'.format(tokens.drone)}).json()
        return '{}/primait/{}/{}'.format(baseurl, repo, resp['number'])
    except (Exception) as e:
        return ""


def get_pr_build_url(repo, commit_sha):
    try:
        resp = requests.get("{}/api/repos/primait/{}/builds".format(baseurl, repo),
                            headers={'Authorization': 'Bearer {}'.format(tokens.drone)}).json()
        build_number = list(filter(lambda build: build.commit == commit_sha, resp))[
            0]['number']
        return '{}/primait/{}/{}'.format(baseurl, repo, build_number)
    except (Exception) as e:
        return ""
