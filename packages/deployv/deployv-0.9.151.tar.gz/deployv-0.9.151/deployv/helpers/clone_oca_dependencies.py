#!/usr/bin/python
import os
import os.path as osp
import logging
import spur
import sys
from deployv.helpers.utils import parse_repo_url

_logger = logging.getLogger()


def parse_depfile(depfile, version, owner='vauxoo'):
    """ This method, parse plain text file oca_dependencies.txt,
    if you have valid repository name, url and version
    :param depfile: object type open file
    :return: Returns list of tuples [(repo, url, version)]
    """
    deps = []
    for line in depfile:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        parts_count = len(parts)
        repo = parts[0]
        url = parts_count > 1 and parts[1]
        branch = parts_count > 2 and parts[2]
        commit = parts_count > 3 and parts[3]
        if not branch:
            branch = version
        if not url:
            url = 'https://github.com/%s/%s.git' % (owner, repo)
        if commit == '#':
            # It's not a commit, it's an inline comment
            commit = False
        deps.append((repo, url, branch, commit))
    return deps


def git_checkout(deps_checkout_dir, reponame, url, branch, commit=False):
    """ This method downloads the repositories found in the oca_dependencies
    files and clones them in the specified dir. If he specified directory
    where the dependencies will be cloned already exists
    and is not empty it won't clone the repos
    :param deps_checkout_dir: he directory in which the dependency
    repositories will be cloned
    :param reponame: name for repository
    :param url: url address repository
    :param branch: branch or version repository
    :param commit: Optional commit to clone
    :return: Returns list (full path)
    """
    checkout_dir = osp.join(deps_checkout_dir, reponame)
    if osp.isdir(checkout_dir):
        return (True, checkout_dir)
    command = ['git', 'clone', '-q', url, '-b', branch, checkout_dir]
    if not commit:
        command.insert(-1, '--depth=1')
    _logger.info('Calling %s', ' '.join(command))
    shell = spur.LocalShell()
    try:
        shell.run(command)
        if commit:
            command = ['bash', '-c', 'cd %s && git reset --hard %s' % (checkout_dir, commit)]
            _logger.info('Calling %s', ' '.join(command))
            shell.run(command)
    except spur.RunProcessError as error:
        message_str = ("Could not clone repo {repo} "
                       "branch {branch}, error: {error} ").format(repo=url,
                                                                  branch=branch,
                                                                  error=error.stderr_output)
        return (False, message_str)
    return (True, checkout_dir)


def get_dep_filename(deps_checkout_dir, build_dir, file_name, version):
    """ This method, makes a recursive search directories to get all the
    files listed in the parameters file_name (oca_dependencies.txt)
    :param deps_checkout_dir: he directory in which the dependency
    repositories will be cloned
    :param build_dir: the directory in which the tested
     repositories have been cloned
    :param file_name: filename to be searched
    :return: Returns list with absolute paths
    """
    dependencies = []
    processed = set()
    depfilename = osp.join(build_dir, file_name)
    dependencies.append((depfilename, 'vauxoo'))
    for repo in os.listdir(deps_checkout_dir):
        _logger.info('examining %s', repo)
        processed.add(repo)
        depfilename = osp.join(deps_checkout_dir, repo, file_name)
        dependencies.append((depfilename, 'vauxoo'))
    for dependency in dependencies:
        try:
            with open(dependency[0]) as depfile:
                deps = parse_depfile(depfile, version, owner=dependency[1])
        except IOError:
            deps = []
        for depname, url, branch, commit in deps:
            _logger.info('* processing %s', depname)
            if depname in processed:
                continue
            processed.add(depname)
            checkout_dir = git_checkout(deps_checkout_dir, depname,
                                        url, branch, commit)
            if not checkout_dir[0]:
                return checkout_dir
            new_dep = (osp.join(checkout_dir[1], file_name),
                       get_owner_from_url(url))
            if new_dep not in dependencies:
                dependencies.append(new_dep)
    # Return the list of dependencies without the organization so we don't
    # have to modify the methods that receive this result
    res = [dep[0] for dep in dependencies]
    return (True, res)


def get_owner_from_url(url):
    """Parses the specified url in order to get the organization from it.
    This organization will be used to clone all the dependencies of this repo
    that does not have a specific url in the oca_dependencies.txt file. If the
    specified url is not in a correct format, this will return `vauxoo` by
    default.

    :param url: URL of the repo, can be http or ssh
    :type url: str
    :return: The organization of the specified repo (default: vauxoo)
    """
    url_parts = parse_repo_url(url)
    return url_parts.get('namespace') or 'vauxoo'


def run(deps_checkout_dir, build_dir, version):
    """ This method executes above methods
    :param deps_checkout_dir: he directory in which the dependency
    repositories will be cloned
    :param build_dir: the directory in which the tested
    repositories have been cloned
    """
    depens = get_dep_filename(deps_checkout_dir, build_dir, 'oca_dependencies.txt',
                              version)
    return depens


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3])
