# coding: utf-8

"""This module substitutes some functions from Gitlab or Github API"""
from os import makedirs, path
from .utils import get_error_message, parse_repo_url, clean_files
from ..base.clonev import deploy_key
from tempfile import mkdtemp
import re
import spur
import shlex
import sys
import logging

_logger = logging.getLogger(__name__)


def get_config(repo, working_folder):
    """Given a working folder returns the .git folder of the repository.

    :param repo: The repository where get the config.
    :type: dict
    :param working_folder: The folder where store the repostiroy.
    :type: str

    :return: return the config needs to get the commit history.
    :rtype: dict
    """
    res = parse_repo_url(repo['repo_url']['origin'])
    folder = path.join(working_folder, res['domain'],
                       res['namespace'], res['repo_name'])
    clone_path = path.join(folder, repo['branch'])
    res.update({'folder': folder, 'checkout_dir': clone_path})
    return res


def prepare(config):
    """Creates repo folder if it does not exists

    :param config: The config with the `folder` key where store the repository.
    :type: dict
    """
    if not path.isdir(config['folder']):
        makedirs(config['folder'])


def clone_repo(repo, config, key_file=False):
    """ If repository exist pulls last changes if it does not clones the repository

    :param repo: The repository that will clone in the working folder.
    :type: dict
    :param config: The config used to know to get the path where clone the repository.
    :type: dict
    """
    shell = spur.LocalShell()
    env = {}
    if path.isdir(config['checkout_dir']):
        cmd = 'git --git-dir={} pull '.format(path.join(config['checkout_dir'], '.git'))
        _logger.debug("Pulling %s", repo['repo_url']['origin'])
    else:
        cmd = 'git clone -q {repo} -b {branch} {folder}'.format(
            repo=repo['repo_url']['origin'], branch=repo['branch'], folder=config['checkout_dir'])
        _logger.debug("Cloning %s", repo['repo_url']['origin'])
    if key_file:
        ssh_command = ('ssh -i %s -o UserKnownHostsFile=/dev/null -o '
                       'StrictHostKeyChecking=no' % (key_file))
        env.update({'GIT_SSH_COMMAND': ssh_command})
    shell.run(shlex.split(cmd), update_env=env)


def get_history(checkout_dir, repo, old_commit):
    """ Gets the commits between old commit and new commit.
    """
    res = []
    shell = spur.LocalShell()
    encodig = sys.stdout.encoding
    new_commit = repo.get('commit')
    values = {'codir': path.join(checkout_dir, '.git'),
              'old': old_commit, 'new': new_commit}
    cmd = ('git --git-dir={codir} log --pretty=format:"%H|%ad|%an|%ae|%s"'
           ' --date=iso {old}..{new}'.format(**values))
    output = shell.run(shlex.split(cmd))
    lines = str(output.output, encodig).split('\n') or []
    repo_url = repo.get('repo_url').get('origin')
    try:
        for line in lines:
            if not line:
                continue
            fields = line.split('|')
            res.append({'commit': fields[0][:7], 'date': fields[1], 'author': fields[2],
                        'commit_url': parse_commit_url(repo_url, fields[0]),
                        'email': fields[3], 'message': fields[4]})
    except Exception as error:
        _logger.error("Could not create commit history between %s and %s", old_commit, new_commit)
        _logger.error(get_error_message(error))
    return res


def parse_commits_data(commits, repo, ref, error):
    repo_url = repo.get('repo_url').get('origin')
    commit_from = ref.get('commit')[:7]
    commit_to = repo.get('commit')[:7]
    commits = sorted(commits, key=lambda commit: commit['date'])
    return {
        'from': commit_from, 'from_url': parse_commit_url(repo_url, commit_from),
        'to': commit_to, 'to_url': parse_commit_url(repo_url, commit_to),
        'path': repo.get('path'), 'branch': repo.get('branch'), 'name': repo.get('name'),
        'repo_url': repo_url, 'commits': commits or [], 'error': error or False,
    }


def parse_commit_url(repo_url, commit):
    """ Given the repo url in ssh or https format, forms the commit url
    """
    exp = (r'((git@)|(?P<proto>http[s]?:\/\/))(?P<domain>[\.\w\d-]*)'
           r'([:\/]{1})(?P<repo>.*)([\.]git)')
    res = re.match(exp, repo_url or '')
    if res:
        values = res.groupdict()
        values.update({
            'proto': values.get('proto') or 'http://', 'commit': commit,
        })
        return "%(proto)s%(domain)s/%(repo)s/commit/%(commit)s" % values
    return ''


def get_commit_history(repo, ref, working_folder, key_file=False):
    """ Gets the commit history between the repository in ref repository.
    """
    _logger.debug("Repository: %s", repo)
    _logger.debug("Ref repository: %s", ref)
    config = get_config(repo, working_folder)
    prepare(config)
    commits = []
    error_message = ''
    key_path = mkdtemp(prefix='key_', dir=working_folder)
    try:
        full_path = deploy_key(key_file, key_path)
        clone_repo(repo, config, full_path)
        commits = get_history(config['checkout_dir'], repo, ref.get('commit', ''))
    except spur.results.RunProcessError as error:
        error_message = get_error_message(error)
    history = parse_commits_data(commits, repo, ref, error_message)
    clean_files(key_path)
    _logger.debug(history)
    return history
