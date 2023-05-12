import tempfile
import shutil
from pathlib import Path

from sync import synchronise_dirs


class FakeFileSystem(list):

    def copy(self, src, dst):
        self.append(("COPY", src, dst))

    def move(self, src, dst):
        self.append(("MOVE", src, dst))

    def delete(self, dst):
        self.append(("DELETE", dst))


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    src = {"hash": "file"}
    dst = {}
    reader = {"/src": src, "/dst": dst}
    filesystem = FakeFileSystem()

    synchronise_dirs(reader.pop, filesystem, "/src", "/dst")

    assert filesystem  == [("COPY", "/src/file", "/dst/file")]


def test_when_a_file_has_been_renamed_in_the_source():
    src = {"hash": "file"}
    dst = {"hash": "file1"}
    reader = {"/src": src, "/dst": dst}
    filesystem = FakeFileSystem()

    synchronise_dirs(reader.pop, filesystem, "/src", "/dst")

    assert filesystem  == [("MOVE", "/dst/file1", "/dst/file")]


def test_same_name_with_different_content():
    src = {"hash": "file"}
    dst = {"hash1": "file"}
    reader = {"/src": src, "/dst": dst}
    filesystem = FakeFileSystem()

    synchronise_dirs(reader.pop, filesystem, "/src", "/dst")

    assert filesystem  == [("DELETE", "/dst/file"), ("COPY", "/src/file", "/dst/file")]


def test_same_file_in_both_src_and_dst():
    src = {"hash": "file"}
    dst = {"hash": "file"}
    reader = {"/src": src, "/dst": dst}
    filesystem = FakeFileSystem()

    synchronise_dirs(reader.pop, filesystem, "/src", "/dst")

    assert filesystem  == []


"""
def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)

        src_hashes = read_paths_and_hashes(src)
        dst_hashes = read_paths_and_hashes(dst)

        actions = determine_actions(src_hashes, dst_hashes, src, dst)

        assert list(actions) == [('copy', Path(src, 'file'), Path(dst, 'file'))]

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


def test_when_a_file_has_been_renamed_in_the_source():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)
        dst_file = Path(dst, 'file2')
        expect_file = Path(dst, 'file')
        dst_file.write_text(content)

        src_hashes = read_paths_and_hashes(src)
        dst_hashes = read_paths_and_hashes(dst)

        actions = determine_actions(src_hashes, dst_hashes, src, dst)

        assert list(actions) == [('move', Path(dst, 'file2'), Path(dst, 'file'))]

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


def test_same_name_with_different_content():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)
        expect_file = Path(dst, 'file')
        expect_file.write_text('some contentABC')

        src_hashes = read_paths_and_hashes(src)
        dst_hashes = read_paths_and_hashes(dst)

        actions = determine_actions(src_hashes, dst_hashes, src, dst)

        assert list(actions) == [
            ('delete', Path(dst, 'file')),
            ('copy', Path(src, 'file'), Path(dst, 'file'))
        ]

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


def test_same_file_in_both_src_and_dst():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)
        expect_file = Path(dst, 'file')
        expect_file.write_text(content)

        src_hashes = read_paths_and_hashes(src)
        dst_hashes = read_paths_and_hashes(dst)

        actions = determine_actions(src_hashes, dst_hashes, src, dst)

        assert list(actions) == []

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


"""
"""
def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)

        sync(src, dst)

        expect_path = Path(dst, 'file')

        assert expect_path.exists()
        assert expect_path.read_text() == content

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


def test_when_a_file_has_been_renamed_in_the_source():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)
        dst_file = Path(dst, 'file2')
        expect_file = Path(dst, 'file')
        dst_file.write_text(content)

        sync(src, dst)

        assert expect_file.exists()
        assert dst_file.exists() == False
        assert expect_file.read_text() == content

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


def test_same_name_with_different_content():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)
        expect_file = Path(dst, 'file')
        expect_file.write_text('some contentABC')

        sync(src, dst)

        assert expect_file.exists()
        assert expect_file.read_text() == content

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)


def test_same_file_in_both_src_and_dst():
    try:
        src = tempfile.mkdtemp()
        dst = tempfile.mkdtemp()

        content = 'some content'
        Path(src, 'file').write_text(content)
        expect_file = Path(dst, 'file')
        expect_file.write_text(content)

        sync(src, dst)

        assert expect_file.exists()
        assert expect_file.read_text() == content

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dst)
"""
