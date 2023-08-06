from __future__ import print_function, unicode_literals
from ..lib.handler.youtrack_handler import YoutrackHandler
from ..lib.handler.github_handler import GithubHandler, GithubException
from ..lib.logger import Logger
from ..lib.config import Config
from ..lib.handler import git_handler as git
from ..lib.handler import prompt_utils
from termcolor import colored
import sys
import os
import re

youtrack = YoutrackHandler()
github = GithubHandler()
config = Config().load()
logger = Logger()


def entrypoint(args):
    repo = os.path.basename(os.getcwd())
    branch_name = git.current_branch_name()

    git.is_dirty(repo)

    if not git.branch_exists(repo, branch_name):
        logger.error("Branch remoto {} non trovato".format(branch_name))
        sys.exit(-1)

    regex = '[A-Z]+-[0-9]+'
    if re.search(regex, branch_name):
        id_card = re.findall(regex, branch_name)[0]
        if not youtrack.validate_issue(id_card):
            logger.error("La card {} non esiste".format(id_card))
            sys.exit(-1)

        pulls = github.get_pr_from_branch(repo, branch_name)
        if pulls.totalCount:
            pr = pulls[0]
            print("PR numero", colored(pr.number, attrs=[
                'bold']), "trovata sul branch", colored(branch_name, attrs=['bold']))

            if prompt_utils.ask_confirm("Vuoi modificare la description della PR?"):
                edit_pr(pr)
                sys.exit(0)

        else:
            logger.info("Card nel branch trovata - Creo pr con link card")
            create_pr(repo, branch_name, id_card)
    else:
        if not prompt_utils.ask_confirm("Card non trovata nel nome del branch, vuoi collegare la CARD con la PR?"):
            logger.warning("Creo PR senza collegarla")
            id_card = None
        else:
            id_card = ask_for_id_card()
        create_pr(repo, branch_name, id_card)


def edit_pr(pr):
    pr_body = ask_for_description(pr.body)
    pr.edit(body=pr_body)
    logger.info("PR modificata")


def create_pr(repo, branch_name, id_card=None):
    if id_card:
        print("\nStai creando una PR sul repo", colored(repo, attrs=['bold']), "sul branch",
              colored(branch_name, attrs=['bold']), "collegato con la card", colored(id_card, attrs=['bold']), "\n")
        link = youtrack.get_link(id_card)
        title = "[{}]: {}".format(
            id_card, youtrack.get_issue(id_card)["summary"])
    else:
        logger.warning("Stai creando una PR sul repo {} sul branch {} NON collegata a una card".format(
            repo, branch_name))
        link = ""
        title = ask_for_title()

    pr_body = ask_for_description()

    body = "{} \n\n {}".format(link, pr_body)

    try:
        pr = github.create_pr(repo, branch_name, title, body)
        logger.info("PR numero {} creata!".format(pr.number))
    except GithubException as e:
        logger.error('Errore durante la richiesta a GitHub: ')
        logger.error(e.data["errors"][0])
        sys.exit(-1)

    if id_card:
        link = github.get_link_from_pr(repo, pr.number)
        update_card(id_card, repo, link)
        logger.info("Inserito link della PR nella Card {}".format(id_card))


def ask_for_description(pr_body=""):
    input("Inserisci la description della PR. Premi Invio per continuare")
    description = prompt_utils.ask_questions_editor(
        'Inserisci la description della PR: ', pr_body)

    if description == "":
        logger.warning("La descrizione della PR non può essere vuota")
        ask_for_description(pr_body)
    else:
        return description


def ask_for_id_card():
    id_card = prompt_utils.ask_questions_input('Inserisci ID della card: ')
    if youtrack.validate_issue(id_card):
        return id_card
    else:
        logger.error("ID non esistente su YouTrack")
        ask_for_id_card()


def update_card(id_card, repo, link):
    youtrack.comment(id_card, "PR {} -> {}".format(repo, link))


def ask_for_title():
    return prompt_utils.ask_questions_input('Inserisci il titolo della PR: ')
