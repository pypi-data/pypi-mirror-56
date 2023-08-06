from __future__ import print_function, unicode_literals
from ..lib.handler.youtrack_handler import YoutrackHandler
from ..lib.handler.github_handler import GithubHandler
from ..lib.handler.captainhook_handler import CaptainHook
from ..lib.config import Config
from ..lib.logger import Logger
from ..lib.handler import prompt_utils
from ..lib.qainit import qainit_stop
from ..lib.handler import git_handler as git
from ..lib.handler import drone_handler as drone
import os
import sys
import re

youtrack = YoutrackHandler()
github = GithubHandler()
logger = Logger()
lock = CaptainHook()
config = Config().load()

def entrypoint(args):
    project = os.path.basename(os.getcwd())
    if not prompt_utils.ask_confirm("Vuoi continuare sul progetto {}?".format(project)):
        sys.exit(-1)

    lock_status = is_master_locked(project)
    if lock_status:
        logger.error("Il progetto è lockato su master. Impossibile continuare.")
        sys.exit(-1)

    pr = select_pr(project)
    branch_name = pr.head.ref

    if not pr.mergeable or pr.mergeable_state != "clean":
        logger.error("Impossibile fare il merge. Controlla che le review siano positive o che la build non sia fallita. {}".format(pr.html_url))
        sys.exit(-1)

    logger.info("Eseguo il merge...")

    merge_status = pr.merge(
        commit_title="{} (#{})".format(pr.title, pr.number), commit_message='', merge_method='squash')

    if not merge_status.merged:
        logger.error("Si è verificato un errore durante il merge.")
        sys.exit(-1)

    drone_build = get_drone_build(project, merge_status.sha)

    if drone_build:
        logger.info(
            "Pull request mergiata su master! Puoi seguire lo stato della build su {}".format(drone_build))
    else:
        logger.info("Pull request mergiata su master!")

    logger.info("Cancello il branch da github...")

    if git.delete_remote_branch(project, branch_name):
        logger.info("Branch remoto eliminato.")
    else:
        logger.error("Si è verificato un errore durante la cancellazione del branch remoto.")
        logger.error("Elimina il branch manualmente da {}".format(pr.html_url))

    if prompt_utils.ask_confirm("Vuoi bloccare staging? (Necessario se bisogna testare su staging)".format(project), default=False):
        lock.lock_project(project)

    logger.info("Aggiorno lo stato della card su youtrack...")
    update_card(branch_name)

    # logger.info("Spengo il qa, se esiste")
    # qainit_branch = "{}_feature/{}".format(
    #     git.get_git_username(), branch_name)
    # qainit_stop(qainit_branch)

    logger.info("Tutto fatto!")
    logger.info("Se esiste un qa per questo branch, per favore, spegnilo.")

    sys.exit()

def select_pr(project):
    prs = github.get_list_pr(project)

    choices = [{"name": "{} {}".format(i.number, i.title), "value": i} for i in prs]
    return prompt_utils.ask_choices('Seleziona PR: ', choices)

def is_master_locked(project):
    request = lock.status(project)
    if request.status_code != 200:
        logger.error("Impossibile determinare lo stato del lock su master.")
        return True
    return request.json()["locked"]

def get_drone_build(project, sha):
    drone_build = drone.get_pr_build_url(
        project, sha)
    if drone_build != "":
        return drone_build
    return None

def update_card(branch_name):
    regex = '[A-Z]+-[0-9]+'
    if re.search(regex, branch_name):
        id_card = re.findall(regex, branch_name)[0]
        if not youtrack.validate_issue(id_card):
            logger.error("La card {} non esiste".format(id_card))
            return False
        youtrack.update_state(id_card, config["youtrack"]["merged_state"])
        return True
