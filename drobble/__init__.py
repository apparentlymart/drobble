
import os
import os.path
from stat import S_ISDIR

from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit


def tree_from_dir(repo, dirname):
    abspath = os.path.abspath(dirname)
    tree = Tree()
    for name in os.listdir(dirname):
        path = os.path.join(abspath, name)
        s = os.lstat(path)
        mode = s.st_mode
        if S_ISDIR(mode):
            obj = tree_from_dir(repo, path)
        else:
            obj = Blob.from_string(file(path).read())
        repo.object_store.add_object(obj)
        tree.add(name, mode, obj.id)

    repo.object_store.add_object(tree)
    return tree
