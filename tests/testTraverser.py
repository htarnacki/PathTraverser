import unittest
import re
from pathlib import Path
from Traverser import Traverser, PathTypes


class TraverserTestCase(unittest.TestCase):

    def test_001(self):
        with Traverser(Path(__file__).parent / 'testData') as paths:
            for _ in paths:
                print(str(_))

    def test_002(self):
        with Traverser(Path(__file__).parent / 'testData') as paths:
            for _ in paths:
                print(str(_))
            for _ in paths:
                print(str(_))

    def test_003(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                namefilter='d.mp4'
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_004(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                namefilter=re.compile(r'.*\.mp4')
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_005(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                extfilter='txt'
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_006(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                maxdepth=0
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_007(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                mindepth=2
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_008(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                pathtype=PathTypes.FILE) as files:
            for _ in files:
                print(str(_))

    def test_009(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                pathtype=PathTypes.DIRECTORY) as dirs:
            for _ in dirs:
                print(str(_))

    def test_010(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                pathtype=PathTypes.LINK) as links:
            for _ in links:
                print(str(_))

    def test_011(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                pathfilter=lambda _: 'dog' in _.name) as paths:
            for _ in paths:
                print(str(_))

    def test_012(self):
        from Traverser.PathUtils import first
        with Traverser(
                Path(__file__).parent / 'testData',
                pathfilter=lambda _, rel: first(rel).name in {'sub2', 'sub3'}
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_013(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                pathfilter=lambda _, depth: depth < 1
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_014(self):
        from Traverser.PathUtils import starts_with
        with Traverser(
                Path(__file__).parent / 'testData',
                pathfilter=lambda _, root: starts_with(_, root / 'sub1')
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_015(self):
        from Traverser.PathUtils import first, last
        with Traverser(
                Path(__file__).parent / 'testData',
                mindepth=1,
                pathfilter=lambda _, rel: first(rel).name == last(rel).name
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_016(self):
        from Traverser.PathUtils import Path
        with Traverser(
                Path(__file__).parent / 'testData',
                mindepth=1,
                pathfilter=lambda _, rel: rel.first.name == rel.last.name
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_017(self):
        from Traverser.PathUtils import Path
        with Traverser(
                Path(__file__).parent / 'testData',
                pathfilter=lambda _, rel: rel.part_count == 1
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_018(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                exclude_namefilter='d.mp4'
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_019(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                exclude_namefilter=re.compile(r'.*\.mp4')
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_020(self):
        with Traverser(
                Path(__file__).parent / 'testData',
                exclude_extfilter='txt'
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_021(self):
        from Traverser.PathUtils import Path
        with Traverser(
                Path(__file__).parent / 'testData',
                mindepth=1,
                exclude_pathfilter=lambda _, rel: rel.first.name == 'x'
        ) as paths:
            for _ in paths:
                print(str(_))

    def test_022(self):
        with Traverser(Path(__file__).parent / 'testData') as paths:
            for _ in paths:
                if paths.depth == 0 and _.is_dir() and _.name == 'x':
                    paths.skipsubtree(_)
                    continue
                print(str(_))


if __name__ == '__main__':
    unittest.main()
