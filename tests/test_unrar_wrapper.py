import argparse
import os
import unittest
import unrar_wrapper as uw


class TestTransformSyntax(unittest.TestCase):

    def test_listing_commands(self):
        args = argparse.Namespace(archive='sample.rar', command='l',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-l']), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='lb',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', []), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='lt',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-L']), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='lta',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-L']), uw.transform_syntax(args))

    def test_verbose_listing_commands(self):
        args = argparse.Namespace(archive='sample.rar', command='v',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-l']), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='vb',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', []), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='vt',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-L']), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='vta',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-L']), uw.transform_syntax(args))

    def test_extract_command(self):
        args = argparse.Namespace(archive='sample.rar', command='x',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('unar', []), uw.transform_syntax(args))

    def test_test_command(self):
        args = argparse.Namespace(archive='sample.rar', command='t',
                                  overwrite=None, password=None, rest=[])
        self.assertEqual(('lsar', ['-t']), uw.transform_syntax(args))

    def test_unar_overwrite_options(self):
        args = argparse.Namespace(archive='sample.rar', command='x',
                                  overwrite='+', password=None, rest=[])
        self.assertEqual(('unar', ['-f']), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='x',
                                  overwrite='-', password=None, rest=[])
        self.assertEqual(('unar', ['-s']), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='x',
                                  overwrite='r', password=None, rest=[])
        self.assertEqual(('unar', ['-r']), uw.transform_syntax(args))

    def test_unar_lsar_password_option(self):
        args = argparse.Namespace(archive='sample.rar', command='x',
                                  overwrite=None, password='mypass', rest=[])
        self.assertEqual(('unar', ['-p', "mypass"]), uw.transform_syntax(args))

        args = argparse.Namespace(archive='sample.rar', command='lb',
                                  overwrite=None, password='mypass', rest=[])
        self.assertEqual(('lsar', ['-p', "mypass"]), uw.transform_syntax(args))


class TestTransformListFiles(unittest.TestCase):

    def setUp(self):
        self.this_dir = os.path.dirname(os.path.abspath(__file__))

    def test_listfiles1(self):
        lf1 = os.path.join(self.this_dir, 'testdata/unit/listfiles1')
        self.assertEqual(['rar/a.png', 'rar/b.png', 'file1'],
                         uw.transform_list_files([lf1]))

    def test_two_listfiles(self):
        lf1 = os.path.join(self.this_dir, 'testdata/unit/listfiles1')
        lf2 = os.path.join(self.this_dir, 'testdata/unit/listfiles2')
        self.assertEqual(['rar/a.png', 'rar/b.png', 'file1', 'test1.pdf',
                          'myrar/test2.pdf', 'myrar/file3.txt', 'rar/x.png'],
                         uw.transform_list_files([lf1, lf2]))

    def test_emptylistfiles(self):
        lf1 = os.path.join(self.this_dir, 'testdata/unit/emptylistfiles')
        self.assertEqual([], uw.transform_list_files([lf1]))


class TestProcessRest(unittest.TestCase):

    def test_process_rest(self):

        test_list = ['a.png']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual(['a.png'], files)
        self.assertEqual([], listfiles)
        self.assertEqual(None, path)

        test_list = ['a.png', 'b.png', 'c.png']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual(['a.png', 'b.png', 'c.png'], files)
        self.assertEqual([], listfiles)
        self.assertEqual(None, path)

        test_list = ['a.png', '@./lists/mylist1', '@./lists/mylist1']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual(['a.png'], files)
        self.assertEqual(['./lists/mylist1', './lists/mylist1'], listfiles)
        self.assertEqual(None, path)

        test_list = ['a.png', './lists/mylist1', './lists/mylist1']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual(['a.png', './lists/mylist1', './lists/mylist1'], files)
        self.assertEqual([], listfiles)
        self.assertEqual(None, path)

        test_list = ['path_to_extract/']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual([], files)
        self.assertEqual([], listfiles)
        self.assertEqual('path_to_extract/', path)

        test_list = ['path_to_extract']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual(['path_to_extract'], files)
        self.assertEqual([], listfiles)
        self.assertEqual(None, path)

        test_list = ['path_to_extract/', 'a.png', '@list/mylist1']
        (files, listfiles, path) = uw.process_rest(test_list)
        self.assertEqual(['a.png'], files)
        self.assertEqual(['list/mylist1'], listfiles)
        self.assertEqual('path_to_extract/', path)
