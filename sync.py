import hashlib
import os
import shutil
from pathlib import Path


"""
BLOCKSIZE = 65536

def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(root):
    root_hashes = {}

    for folder, _, files in os.walk(root):
        for fn in files:
            root_hashes[hash_file(Path(folder) / fn)] = fn

    return root_hashes


def determine_actions(src_hash, dst_hash, src, dst):
    k1 = set(src_hash)
    k2 = set(dst_hash)
    kv1 = set(src_hash.items())
    kv2 = set(dst_hash.items())

    # mv: same hash, different fn
    # rm: hash1 is not in hash2
    for diff in kv2 - kv1:
        if diff[0] in k1 & k2:
            yield 'move', Path(dst) / diff[1], Path(dst) / src_hash[diff[0]]
        else:
            yield 'delete', Path(dst) / diff[1]

    # cp: in hash1 but not in hash2
    for diff in kv1 - kv2:
        if diff[0] not in k1 & k2:
            yield 'copy', Path(src) / diff[1], Path(dst) / diff[1]
"""


def synchronise_dirs(reader, filesystem, src_root, dst_root):
    src_hashes = reader(src_root)
    dst_hashes = reader(dst_root)

    k1 = set(src_hashes)
    k2 = set(dst_hashes)
    kv1 = set(src_hashes.items())
    kv2 = set(dst_hashes.items())

    # mv: same hash, different fn
    # rm: hash1 is not in hash2
    for diff in kv2 - kv1:
        if diff[0] in k1 & k2:
            filesystem.move(dst_root + '/' + diff[1], dst_root + '/' + src_hashes[diff[0]])
        else:
            filesystem.delete(dst_root + '/' + diff[1])

    # cp: in hash1 but not in hash2
    for diff in kv1 - kv2:
        if diff[0] not in k1 & k2:
            filesystem.copy(src_root + '/' + diff[1], dst_root + '/' + diff[1])


"""
def sync(src, dst):
    # input: imperative shell
    src_hashes = read_paths_and_hashes(src)
    dst_hashes = read_paths_and_hashes(dst)

    # logic: function core
    actions = determine_actions(src_hashes, dst_hashes, src, dst)

    # output: imperative shell
    for action, *path in actions:
        print(action, *path)

"""
"""
def sync(src, dst):
    # hash all the files in src and save them in dict
    path_to_hash = {}
    hash_to_path = {}
    for folder, _, files in os.walk(src):
        for fn in files:
            hash_src_file = hash_file(Path(folder) / fn)
            path_to_hash[fn] = hash_src_file
            hash_to_path[hash_src_file] = fn

    # hash file in dst and check if it's in dict
    for folder, _, files in os.walk(dst):
        for fn in files:
            path = Path(folder) / fn
            dst_file_hash = hash_file(path)
            if dst_file_hash in hash_to_path:
                if hash_to_path[dst_file_hash] != fn:
                    print(f'move /dst/{fn} to /dst/{hash_to_path[dst_file_hash]}')
                    shutil.move(path, Path(dst, hash_to_path[dst_file_hash]))
                del path_to_hash[hash_to_path[dst_file_hash]]
            else:
                print(f'delete /dst/{fn}')
                path.unlink()

    # copy files
    for fn in path_to_hash.keys():
        src_path = os.path.join(src, fn)
        dst_path = os.path.join(dst, fn)
        print(f'copy /src/{fn} to /dst/{fn}')
        shutil.copy(src_path, dst_path)
"""
