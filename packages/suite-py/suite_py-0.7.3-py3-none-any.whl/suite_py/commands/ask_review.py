from __future__ import print_function, unicode_literals
from ..lib.handler.youtrack_handler import YoutrackHandler
from ..lib.handler.github_handler import GithubHandler
from ..lib.logger import Logger
from ..lib.handler import git_handler as git
from ..lib.handler import prompt_utils
from ..lib.handler.captainhook_handler import CaptainHook
import os
import sys
import readline
import re

youtrack = YoutrackHandler()
github = GithubHandler()
logger = Logger()

try:
    captainhook = CaptainHook()
    users = captainhook.get_users_list().json()
except:
    logger.error(
        "Non riesco ad ottenere la lista degli utenti da captainhook. Agiungere i reviewer dal sito GitHub")
    sys.exit(-1)


def entrypoint(args):

    repo = os.path.basename(os.getcwd())
    branch_name = git.current_branch_name()
    github_reviewers = []

    pull = github.get_pr_from_branch(repo, branch_name)

    if pull.totalCount:
        pr = pull[0]
        logger.info('Trovata PR numero {} sul branch {} sul repo {}'.format(
            pr.number, branch_name, repo))
    else:
        logger.error(
            'Nessuna PR aperta trovata con il branch {}'.format(branch_name))
        sys.exit(-1)

    youtrack_reviewers = ask_reviewer()

    for rev in youtrack_reviewers:
        for user in users:
            if user["youtrack"] == rev:
                github_reviewers.append(user["github"])

    pr.create_review_request(github_reviewers)

    regex = '[A-Z]+-[0-9]+'
    if re.search(regex, pr.title):
        id_card = re.findall(regex, pr.title)[0]
        if not youtrack.validate_issue(id_card):
            logger.error("La card {} non esiste".format(id_card))
            sys.exit(-1)
        else:
            logger.info(
                'Sposto la card {} in review su youtrack e aggiungo i tag degli utenti'.format(id_card))
            youtrack.update_state(id_card, 'Review')
            for rev in youtrack_reviewers:
                try:
                    youtrack.add_tag(id_card, "review:{}".format(rev))
                except BaseException as e:
                    logger.warning(
                        "Non sono riuscito ad aggiungere i tag di review: {}".format(e))
                    sys.exit(-1)
    else:
        logger.warning('Reviewers inseriti su GitHub. Nessuna card collegata.')


def ask_reviewer():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    youtrack_reviewers = []

    youtrack_reviewers = list(
        input("Scegli i reviewers (separati da spazio) > ").split())

    if len(youtrack_reviewers) < 1:
        logger.warning("Devi inserire almeno un reviewer")
        ask_reviewer()
    else:
        return youtrack_reviewers


def completer(text, state):
    options = [x["youtrack"]
               for x in users if text.lower() in x["youtrack"].lower()]
    try:
        return options[state]
    except IndexError:
        return None
