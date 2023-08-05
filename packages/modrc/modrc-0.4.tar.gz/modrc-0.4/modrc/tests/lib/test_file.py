import pathlib
import tempfile
import unittest

from parameterized import parameterized

from modrc import exceptions
from modrc.lib import file, helper, package, setup


class TestCreateFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Test that an exception is raised when the package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            file.create_file('test-file', 'test-package')

    def test_file_already_exists(self):
        """Test that an exception is raised when the file already exists."""
        package_dir = package.create_package('test-package')
        package_dir.joinpath('files', 'test-file').mkdir(parents=True)
        with self.assertRaises(exceptions.ModRCFileExistsError):
            file.create_file('test-file', 'test-package')

    def test_create_file_success(self):
        """Tests that the new file is created successfully."""
        package_dir = package.create_package('test-package')
        file_dir = file.create_file('test-file', 'test-package')
        self.assertEqual(package_dir.joinpath('files', 'test-file'), file_dir)
        self.assertTrue(file_dir.is_dir())


class TestGetFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Tests that an exception is raised if the package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            file.get_file('test-file', 'test-package')

    def test_file_does_not_exist(self):
        """Tests that an exception is raised if the file does not exist."""
        package.create_package('test-package')
        with self.assertRaises(exceptions.ModRCFileDoesNotExistError):
            file.get_file('test-file', 'test-package')

    def test_file_exists(self):
        """Tests that a file is retrieved."""
        package.create_package('test-package')
        file_dir = file.create_file('test-file', 'test-package')
        self.assertEqual(file_dir, file.get_file('test-file', 'test-package'))


class TestCreateFileFilter(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_package_does_not_exist(self):
        """Test that an exception is thrown if the package does not exist."""
        with self.assertRaises(exceptions.ModRCPackageDoesNotExistError):
            file.create_file_filter('global', 'test-file', 'test-package')

    def test_file_does_not_exist(self):
        """Test that an exception is thrown if the file does not exist."""
        package.create_package('test-package')
        with self.assertRaises(exceptions.ModRCFileDoesNotExistError):
            file.create_file_filter('global', 'test-file', 'test-package')

    def test_create_file_filter_success(self):
        """Test that a file filter is created."""
        package.create_package('test-package')
        file_dir = file.create_file('test-file', 'test-package')
        file_filter = file.create_file_filter('global', 'test-file', 'test-package')
        self.assertEqual(file_filter, file_dir.joinpath('global'))
        self.assertTrue(file_filter.exists())

    def test_validate_filter_name(self):
        """Tests that an exception is thrown if the filter name is invalid"""
        package.create_package('test-package')
        file.create_file('test-file', 'test-package')
        with self.assertRaises(exceptions.ModRCFilterNameError):
            file.create_file_filter('bad', 'test-file', 'test-package')


class TestCompileFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        self.modrc_dir = setup.initial_setup(self.temp_dir)
        self.packages_dir = helper.get_packages_dir()
        package.create_package('test-package')

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_file_does_not_exist(self):
        """Tests that an error is thrown if the file does not exist."""
        with self.assertRaises(exceptions.ModRCFileDoesNotExistError):
            file.compile_file('test-file', 'test-package', 'macos')

    @parameterized.expand([
        ('macos.10.15.1'),
        ('linux.ubuntu.18.04.3')
    ])
    def test_global_file_compile(self, system):
        """Test that the global filter is compiled for macOS and Linux."""
        file.create_file('test-file', 'test-package')
        # create the file filter with content and compile it
        file_filter = file.create_file_filter('global', 'test-file', 'test-package')
        with open(str(file_filter), 'w') as ff:
            ff.write('GLOBAL CONTENT')
        compiled_file = file.compile_file('test-file', 'test-package', system)
        # check the file
        self.assertTrue(compiled_file.is_file())
        self.assertEqual(compiled_file, helper.get_live_dir().joinpath('test-file'))
        with open(str(file_filter)) as ff, open(str(compiled_file), 'r') as cf:
            self.assertEqual(ff.readlines(), cf.readlines())

    @parameterized.expand([
        ('macos.10.15.1'),
        ('linux.ubuntu.18.04.3')
    ])
    def test_exclusive_file_compilation(self, system):
        """Test that the only the right OS filter is compiled."""
        file.create_file('test-file', 'test-package')
        # create the file filters swith content and compile them
        file_filter_macos = file.create_file_filter('macos', 'test-file', 'test-package')
        with open(str(file_filter_macos), 'w') as ff:
            ff.write('MACOS CONTENT')
        file_filter_linux = file.create_file_filter('linux', 'test-file', 'test-package')
        with open(str(file_filter_linux), 'w') as ff:
            ff.write('LINUX CONTENT')
        compiled_file = file.compile_file('test-file', 'test-package', system)
        # check the file
        self.assertTrue(compiled_file.is_file())
        self.assertEqual(compiled_file, helper.get_live_dir().joinpath('test-file'))
        if system[0:5] == 'macos':
            system_file_filter = file_filter_macos
        else:
            system_file_filter = file_filter_linux
        with open(str(system_file_filter)) as sff, open(str(compiled_file), 'r') as cf:
            self.assertEqual(sff.readlines(), cf.readlines())

    @parameterized.expand([
        ('macos.10.15.1'),
        ('linux.ubuntu.18.04.3')
    ])
    def test_override_compiled_file(self, system):
        """Test that a previously compiled file is overriden when being compiled again."""
        # create the file and compile it
        file.create_file('test-file', 'test-package')
        file_filter = file.create_file_filter('global', 'test-file', 'test-package')
        for i in range(2):
            with open(str(file_filter), 'w') as ff:
                ff.write('GLOBAL {}'.format(i))
            compiled_file = file.compile_file('test-file', 'test-package', system)
        # check the file
        self.assertTrue(compiled_file.is_file())
        self.assertEqual(compiled_file, helper.get_live_dir().joinpath('test-file'))
        with open(str(file_filter)) as ff, open(str(compiled_file), 'r') as cf:
            self.assertEqual(ff.readlines(), cf.readlines())

    @parameterized.expand([
        ('macos.10.15.1'),
        ('linux.ubuntu.18.04.3')
    ])
    def test_filters_do_not_exist(self, system):
        """Tests that an exception is raised if no filters exist when a file is compiled."""
        file.create_file('test-file', 'test-package')
        # create the file filter with content and compile it
        with self.assertRaises(exceptions.ModRCFilterDoesNotExistError):
            file.compile_file('test-file', 'test-package', system)
        self.assertFalse(helper.get_live_dir().joinpath('test-file').exists())

    # TODO: test filter scoping precedence


class TestGetLiveFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)
        setup.initial_setup(self.temp_dir)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_live_file_does_not_exist(self):
        """Tests that an exception is thrown if a live file does not exist."""
        with self.assertRaises(exceptions.ModRCLiveFileDoesNotExistError):
            file.get_live_file('test-file')

    def test_live_file_exists(self):
        """Tests that a live file is retrieved if it exists."""
        live_file = helper.get_live_dir().joinpath('test-file')
        live_file.touch()
        self.assertEqual(file.get_live_file('test-file'), live_file)
