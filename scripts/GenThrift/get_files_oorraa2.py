# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
#         Скачать файлы Thrift для конвертации из GIT репозитория.
#         Info: http://gitpython.readthedocs.org/en/stable/tutorial.html
# ----------------------------------------------------------------------------------------

__author__ = 's.trubachev'

import os
from git import Repo, GitCommandNotFound


if __name__ == '__main__':
    join = os.path.join

    # rorepo is a a Repo instance pointing to the git-python repository.
    # For all you know, the first argument to Repo is a path to the repository
    # you want to work with

    working_tree_dir = """./git-python"""
    git_path = "ssh://git@git.home.oorraa.net:2795/internal-api/oorraa-thrift.git"
    git_url = "https://git.home.oorraa.net/internal-api/oorraa-thrift.git"
    ddd = "https://github.com/gitpython-developers/GitPython.git"
    ttt = "git@bitbucket.org:CoolJuice/py-test.git"


    #repo = Repo(path=working_tree_dir)
    #assert not repo.bare

    # инициализируем
    #bare_repo = None
    #try:
    #    bare_repo = Repo.init(path=git_path)
    #except GitCommandNotFound, tx:
    #    print ("Not found git in console")
    #    raise GitCommandNotFound(str(tx))
    ##assert bare_repo.bare
#
    ## get a config reader for read-only access
    #bare_repo.config_reader()

    #bare_repo = Repo()
    #bare_repo = Repo.init(path=working_tree_dir)
    # Клонируем
    #cloned_repo = None
    #try:
    #    cloned_repo = bare_repo.clone_from(url=git_path, to_path=working_tree_dir, branch='master')
        #cloned_repo = bare_repo.clone(path=git_path)
    #except Exception, tx:
    #    print tx
    #    raise AssertionError(str(tx))
    #assert cloned_repo.__class__ is Repo     # clone an existing repository
    #assert Repo.init(git_path).__class__ is Repo

    # -------------------------------------------------------
    bare_repo = Repo()

    #cloned_repo = bare_repo.clone_from(url=git_url, to_path=working_tree_dir, branch='master')
    path_id_rsa = "c:/Users/s.trubachev/.ssh/id_rsa"
    f = open(path_id_rsa)
    t = f.read()
    ssh_cmd = 'ssh -i "%s"' % t
    with bare_repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
        #bare_repo.remotes.origin.fetch()
        try:
            cloned_repo = bare_repo.clone_from(url=git_path, to_path=working_tree_dir, branch='master')
        except Exception, tx:
            print tx

    # TODO: у нас не работает https, а библиотека git запускает ssh из обычной консоли, которая не подтягивает ключи