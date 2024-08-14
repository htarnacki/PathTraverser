import unittest
import os
import re
from pathlib import Path
from PathTraverser import Traverser
from PathTraverser.Traverser import Iterator
from PathTraverser.filters import files, dirs, symlinks, ext, name, path, \
    depth, hidden, executable, writeable, readonly, owner, size, call
from PathTraverser.utils.Path import first, last, part_count, starts_with


HERE: Path = Path(__file__).parent
TEST_DATA_ROOT: Path = HERE / 'testData'

os.chdir(HERE)

ALL_TEST_PATHS: list[str] = [
    "testData/0",
    "testData/0/.hidden_dir",
    "testData/0/.hidden_file",
    "testData/0/executable.exe",
    "testData/0/readonly.jpg",
    "testData/0/writeable.png",
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1",
    "testData/sub1/sub1.1/d.mp4",
    "testData/sub1/sub1.1/d.mp4.link",
    "testData/sub2",
    "testData/sub2/1.txt",
    "testData/sub2/sub2.1",
    "testData/sub2/sub2.1/cat_dog_fish.txt",
    "testData/sub2/sub2.1/sub2.1.1",
    "testData/sub2/sub2.1/sub2.1.1/2.txt",
    "testData/sub3",
    "testData/sub3/sub3.1",
    "testData/sub3/sub3.1/sub3.1.1",
    "testData/sub3/sub3.1/sub3.1.1/z.zip",
    "testData/x",
    "testData/x/y",
    "testData/x/y/z",
    "testData/x/y/z/x"
]

ALL_TEST_FILES: list[str] = [
    "testData/0/.hidden_file",
    "testData/0/executable.exe",
    "testData/0/readonly.jpg",
    "testData/0/writeable.png",
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1/d.mp4",
    "testData/sub1/sub1.1/d.mp4.link",
    "testData/sub2/1.txt",
    "testData/sub2/sub2.1/cat_dog_fish.txt",
    "testData/sub2/sub2.1/sub2.1.1/2.txt",
    "testData/sub3/sub3.1/sub3.1.1/z.zip"
]

ALL_TEST_DIRS: list[str] = [
    "testData/0",
    "testData/0/.hidden_dir",
    "testData/sub1",
    "testData/sub1/sub1.1",
    "testData/sub2",
    "testData/sub2/sub2.1",
    "testData/sub2/sub2.1/sub2.1.1",
    "testData/sub3",
    "testData/sub3/sub3.1",
    "testData/sub3/sub3.1/sub3.1.1",
    "testData/x",
    "testData/x/y",
    "testData/x/y/z",
    "testData/x/y/z/x"
]

ALL_TEST_SYMLINKS: list[str] = [
    "testData/sub1/sub1.1/d.mp4.link"
]

ZIP_TXT_MP4_TEST_FILES: list[str] = [
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1/d.mp4",
    "testData/sub2/1.txt",
    "testData/sub2/sub2.1/cat_dog_fish.txt",
    "testData/sub2/sub2.1/sub2.1.1/2.txt",
    "testData/sub3/sub3.1/sub3.1.1/z.zip"
]

READONLY_TEST_FILES: list[str] = [
    "testData/0/readonly.jpg"
]

HIDDEN_TEST_FILES: list[str] = [
    "testData/0/.hidden_file"
]

HIDDEN_TEST_DIRS: list[str] = [
    "testData/0/.hidden_dir"
]

EXECUTABLE_TEST_FILES: list[str] = [
    "testData/0/executable.exe"
]

WRITEABLE_TEST_PATHS: list[str] = [
    "testData/0",
    "testData/0/.hidden_dir",
    "testData/0/.hidden_file",
    "testData/0/executable.exe",
    "testData/0/writeable.png",
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1",
    "testData/sub1/sub1.1/d.mp4",
    "testData/sub1/sub1.1/d.mp4.link",
    "testData/sub2",
    "testData/sub2/1.txt",
    "testData/sub2/sub2.1",
    "testData/sub2/sub2.1/cat_dog_fish.txt",
    "testData/sub2/sub2.1/sub2.1.1",
    "testData/sub2/sub2.1/sub2.1.1/2.txt",
    "testData/sub3",
    "testData/sub3/sub3.1",
    "testData/sub3/sub3.1/sub3.1.1",
    "testData/sub3/sub3.1/sub3.1.1/z.zip",
    "testData/x",
    "testData/x/y",
    "testData/x/y/z",
    "testData/x/y/z/x"
]

D_MP4_TEST_FILE: list[str] = [
    "testData/sub1/sub1.1/d.mp4"
]

D_PLUS_C_MP4_TEST_FILE: list[str] = [
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1/d.mp4"
]

MP4_TEST_FILES: list[str] = [
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1/d.mp4"
]

MP4_PLUS_ZIP_TEST_FILES: list[str] = [
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1/d.mp4",
    'testData/sub3/sub3.1/sub3.1.1/z.zip'
]

TXT_TEST_FILES: list[str] = [
    "testData/sub2/1.txt",
    "testData/sub2/sub2.1/cat_dog_fish.txt",
    "testData/sub2/sub2.1/sub2.1.1/2.txt"
]

DEPTH_2_TEST_PATHS: list[str] = [
    "testData/sub1/sub1.1/d.mp4",
    "testData/sub1/sub1.1/d.mp4.link",
    "testData/sub2/sub2.1/cat_dog_fish.txt",
    "testData/sub2/sub2.1/sub2.1.1",
    "testData/sub3/sub3.1/sub3.1.1",
    "testData/x/y/z"
]

MP4_LESS_THAN_2MB: list[str] = [
    "testData/a.mp4",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1/d.mp4"
]

MP4_MORE_THAN_1MB: list[str] = [
    "testData/a.mp4",
    "testData/b.mp4"
]

A_MP4_DEPTH_LESS_THAN_1_TEST_FILE: list[str] = [
    "testData/a.mp4"
]

SKIPSUBTREE_SUB2_TEST_PATHS: list[str] = [
    "testData/0",
    "testData/0/.hidden_dir",
    "testData/0/.hidden_file",
    "testData/0/executable.exe",
    "testData/0/readonly.jpg",
    "testData/0/writeable.png",
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1",
    "testData/sub1/c.mp4",
    "testData/sub1/sub1.1",
    "testData/sub1/sub1.1/d.mp4",
    "testData/sub1/sub1.1/d.mp4.link",
    "testData/sub2",
    "testData/sub3",
    "testData/sub3/sub3.1",
    "testData/sub3/sub3.1/sub3.1.1",
    "testData/sub3/sub3.1/sub3.1.1/z.zip",
    "testData/x",
    "testData/x/y",
    "testData/x/y/z",
    "testData/x/y/z/x"
]

DIR_0_TEST_PATHS: list[str] = [
    "testData/0",
    "testData/0/.hidden_dir",
    "testData/0/.hidden_file",
    "testData/0/executable.exe",
    "testData/0/readonly.jpg",
    "testData/0/writeable.png"
]

A_MP4_TEST_PATHS: list[str] = [
    "testData/a.mp4"
]

PART_COUNT_1_TEST_PATHS: list[str] = [
    "testData/0",
    "testData/a.mp4",
    "testData/b.mp4",
    "testData/sub1",
    "testData/sub2",
    "testData/sub3",
    "testData/x"
]

TEST_TRAVERSER_PY_TEST_FILE: list[str] = [
    "testTraverser.py"
]

LEVEL_0_TEST_PATHS: list[str] = [
    'testData/0',
    'testData/a.mp4',
    'testData/b.mp4',
    'testData/sub1',
    'testData/sub2',
    'testData/sub3',
    'testData/x'
]

for table in [
    ALL_TEST_PATHS, ALL_TEST_DIRS, ALL_TEST_FILES, ALL_TEST_SYMLINKS, ZIP_TXT_MP4_TEST_FILES, READONLY_TEST_FILES,
    HIDDEN_TEST_FILES, EXECUTABLE_TEST_FILES, WRITEABLE_TEST_PATHS, D_MP4_TEST_FILE, MP4_TEST_FILES, TXT_TEST_FILES,
    MP4_LESS_THAN_2MB, MP4_MORE_THAN_1MB, A_MP4_DEPTH_LESS_THAN_1_TEST_FILE, DEPTH_2_TEST_PATHS,
    SKIPSUBTREE_SUB2_TEST_PATHS, DIR_0_TEST_PATHS, A_MP4_TEST_PATHS, PART_COUNT_1_TEST_PATHS, D_PLUS_C_MP4_TEST_FILE,
    MP4_PLUS_ZIP_TEST_FILES, TEST_TRAVERSER_PY_TEST_FILE, HIDDEN_TEST_DIRS, LEVEL_0_TEST_PATHS
]:
    for idx, item in enumerate(table):
        table[idx] = str(HERE / item)


class TraverserTestCase(unittest.TestCase):

    def test_001(self) -> None:
        self.assertListEqual(sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT))), ALL_TEST_PATHS)

    def test_002(self) -> None:
        self.assertListEqual(sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).files)), ALL_TEST_FILES)

    def test_003(self) -> None:
        self.assertListEqual(sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).dirs)), ALL_TEST_DIRS)

    def test_004(self) -> None:
        self.assertListEqual(sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).symlinks)), ALL_TEST_SYMLINKS)

    def test_005(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, files + dirs))),
            sorted(list(set(ALL_TEST_FILES + ALL_TEST_DIRS))))

    def test_006(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, files + dirs + symlinks))),
            sorted(list(set(ALL_TEST_FILES + ALL_TEST_DIRS + ALL_TEST_SYMLINKS))))

    def test_007(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, -dirs))),
            sorted(list(set(ALL_TEST_FILES + ALL_TEST_SYMLINKS))))

    def test_008(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, -(files + symlinks)))), ALL_TEST_DIRS)

    def test_009(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).files(ext.zip + ext.txt + ext.mp4))),
            ZIP_TXT_MP4_TEST_FILES)

    def test_010(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).files(ext('zip', 'txt', 'mp4')))),
            ZIP_TXT_MP4_TEST_FILES)

    def test_011(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).files(readonly))),
            READONLY_TEST_FILES)
        
    def test_012(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).files(hidden))),
            HIDDEN_TEST_FILES)
        
    def test_013(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT).files(executable))),
            EXECUTABLE_TEST_FILES)

    def test_014(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, writeable))),
            WRITEABLE_TEST_PATHS)

    def test_015(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, readonly + hidden))),
            sorted(list(set(READONLY_TEST_FILES + HIDDEN_TEST_FILES + HIDDEN_TEST_DIRS))))

    def test_016(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name('d.mp4')))),
            D_MP4_TEST_FILE)

    def test_017(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name.glob('*.mp4')))),
            MP4_TEST_FILES)

    def test_018(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name.regex(r'.*\.mp4$')))),
            MP4_TEST_FILES)

    def test_019(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name(re.compile(r'.*\.mp4$'))))),
            MP4_TEST_FILES)

    def test_020(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, path.regex(r'.*\.mp4$', r'.*\.txt$')))),
            MP4_TEST_FILES + TXT_TEST_FILES)

    def test_021(self) -> None:
        current_user: str = os. getlogin()
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, owner(current_user)))),
            ALL_TEST_PATHS)

    def test_022(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, 1 < depth() < 3))),
            DEPTH_2_TEST_PATHS)

    def test_023(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, depth() == 2))),
            DEPTH_2_TEST_PATHS)

    def test_024(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, ext.mp4, size() < '2MB'))),
            MP4_LESS_THAN_2MB)

    def test_025(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, ext.mp4, size() > '1MB'))),
            MP4_MORE_THAN_1MB)

    def test_026(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(
                TEST_DATA_ROOT,
                call(lambda _, depth: True if _.name == 'a.mp4' and depth < 1 else False)))),
            A_MP4_DEPTH_LESS_THAN_1_TEST_FILE)

    def test_027(self) -> None:
        result: list[Path] = []
        for _ in (paths := Traverser(TEST_DATA_ROOT).iter()):
            if _.name == 'sub2' and _.is_dir():
                paths.skipsubtree(_)
            result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), SKIPSUBTREE_SUB2_TEST_PATHS)

    def test_028(self) -> None:
        self.assertListEqual(sorted(str(_) for _ in Traverser(TEST_DATA_ROOT).get()), ALL_TEST_PATHS)

    def test_029(self) -> None:
        counter = 0
        def inc(_) -> None:
            nonlocal counter
            counter += 1
        self.assertListEqual(
            sorted(str(_) for _ in Traverser(TEST_DATA_ROOT).iter().on_each(inc).get()), ALL_TEST_PATHS)
        assert counter == 27

    def test_030(self) -> None:
        counter = 0
        def inc(_) -> None:
            nonlocal counter
            counter += 1
        self.assertListEqual(sorted(str(_) for _ in Traverser(TEST_DATA_ROOT).on_each(inc).get()), ALL_TEST_PATHS)
        assert counter == 27

    def test_031(self) -> None:
        counter = 0
        def inc(_) -> None:
            nonlocal counter
            counter += 1
        self.assertListEqual(sorted(str(_) for _ in Traverser(TEST_DATA_ROOT).on_file(inc).get()), ALL_TEST_PATHS)
        assert counter == 13

    def test_032(self) -> None:
        counter = 0
        def inc(_) -> None:
            nonlocal counter
            counter += 1
        self.assertListEqual(sorted(str(_) for _ in Traverser(TEST_DATA_ROOT).on_dir(inc).get()), ALL_TEST_PATHS)
        assert counter == 14

    def test_033(self) -> None:
        counter = 0
        def inc(_) -> None:
            nonlocal counter
            counter += 1
        self.assertListEqual(sorted(str(_) for _ in Traverser(TEST_DATA_ROOT).on_symlink(inc).get()), ALL_TEST_PATHS)
        assert counter == 1

    def test_034(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, call(lambda _, rel: starts_with(rel, Path('0')))))),
            DIR_0_TEST_PATHS)

    def test_035(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, call(lambda _, rel: first(rel) == Path('0'))))),
            DIR_0_TEST_PATHS)

    def test_036(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, call(lambda _, rel: last(rel) == Path('a.mp4'))))),
            A_MP4_TEST_PATHS)

    def test_037(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, call(lambda _, rel: part_count(rel) == 1)))),
            PART_COUNT_1_TEST_PATHS)
        
    def test_038(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name('d.mp4', 'c.mp4')))),
            D_PLUS_C_MP4_TEST_FILE)

    def test_039(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name == ['d.mp4', 'c.mp4']))),
            D_PLUS_C_MP4_TEST_FILE)

    def test_040(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name.regex(r'.*\.mp4$', r'.*\.zip$')))),
            MP4_PLUS_ZIP_TEST_FILES)

    def test_041(self) -> None:
            self.assertListEqual(
                [str(_) for _ in Traverser(name == 'testTraverser.py').get()], TEST_TRAVERSER_PY_TEST_FILE)

    def test_042(self) -> None:
            self.assertListEqual(
                sorted(list(Traverser())),
                sorted(Traverser().get()))

    def test_043(self) -> None:
            self.assertListEqual(
                sorted(list(Traverser(files))),
                sorted(Traverser().files.get()))

    def test_044(self) -> None:
            self.assertListEqual(
                sorted(list(Traverser(dirs))),
                sorted(Traverser().dirs.get()))

    def test_045(self) -> None:
            self.assertListEqual(
                sorted(list(Traverser(symlinks))),
                sorted(Traverser().symlinks.get()))

    def test_046(self) -> None:
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, name.regex(re.compile(r'.*\.mp4$'))))),
            MP4_TEST_FILES)

    def test_047(self) -> None:
        current_user: str = os. getlogin()
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, owner == current_user))),
            ALL_TEST_PATHS)
        
    def test_048(self) -> None:
        current_user: str = os. getlogin()
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, owner('root', current_user)))),
            ALL_TEST_PATHS)

    def test_049(self) -> None:
        current_user: str = os. getlogin()
        self.assertListEqual(
            sorted(list(str(_) for _ in Traverser(TEST_DATA_ROOT, owner == ['root', current_user]))),
            ALL_TEST_PATHS)

    def test_050(self) -> None:
        result: list[Path] = []
        with Traverser(TEST_DATA_ROOT).iter() as paths:
            for _ in paths:
                if _.name == 'sub2' and _.is_dir():
                    paths.skipsubtree(_)
                result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), SKIPSUBTREE_SUB2_TEST_PATHS)

    def test_051(self) -> None:
        result: list[Path] = []
        paths: Iterator = Traverser(TEST_DATA_ROOT).iter()
        for _ in paths:
            if _.name == 'sub2' and _.is_dir():
                paths.skipsubtree(_)
            result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), SKIPSUBTREE_SUB2_TEST_PATHS)

    def test_052(self) -> None:
        result: list[Path] = []
        paths: Iterator = iter(Traverser(TEST_DATA_ROOT))
        for _ in paths:
            if _.name == 'sub2' and _.is_dir():
                paths.skipsubtree(_)
            result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), SKIPSUBTREE_SUB2_TEST_PATHS)

    def test_053(self) -> None:
        result: list[Path] = []
        for _ in (paths := iter(Traverser(TEST_DATA_ROOT))):
            if _.name == 'sub2' and _.is_dir():
                paths.skipsubtree(_)
            result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), SKIPSUBTREE_SUB2_TEST_PATHS)

    def test_054(self) -> None:
        result: list[Path] = []
        with Traverser(TEST_DATA_ROOT, hidden) as paths:
            for _ in paths.files:
                result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), HIDDEN_TEST_FILES)

    def test_055(self) -> None:
        result: list[Path] = []
        with Traverser(TEST_DATA_ROOT, hidden) as paths:
            for _ in paths.files:
                result.append(_)
            for _ in paths.dirs:
                result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), sorted(HIDDEN_TEST_FILES + HIDDEN_TEST_DIRS))

    def test_056(self) -> None:
        result: list[Path] = []
        with Traverser(TEST_DATA_ROOT, hidden) as paths:
            for _ in paths.filter(files):
                result.append(_)
            for _ in paths.filter(dirs):
                result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), sorted(HIDDEN_TEST_FILES + HIDDEN_TEST_DIRS))

    def test_057(self) -> None:
        result: list[Path] = []
        for _ in (paths := iter(Traverser(TEST_DATA_ROOT))):
            if paths.depth == 0 and _.is_dir():
                paths.skipsubtree(_)
            result.append(_)
        self.assertListEqual(sorted(list(str(_) for _ in result)), LEVEL_0_TEST_PATHS)

if __name__ == '__main__':
    unittest.main()
