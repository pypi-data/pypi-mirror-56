import pathlib
import tempfile
import unittest
import yaml

from modrc import exceptions
from modrc.lib import helper, setup


class TestInitialSetup(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_modrc_directory_already_exists(self):
        """Test that exception is raised if the ModRC directory already exists."""
        modrc_dir = pathlib.Path('~/.modrc').expanduser()
        modrc_dir.mkdir()
        with self.assertRaises(exceptions.ModRCIntegrityError):
            setup.initial_setup(self.temp_dir)

    def test_initial_setup(self):
        """Test ModRC directory creation."""
        modrc_dir = setup.initial_setup()
        self.assertEqual(modrc_dir.name, '.modrc')
        self.assertTrue(modrc_dir.exists())

    def test_initial_setup_symlink(self):
        """Test ModRC directory creation with symlink."""
        modrc_dir = setup.initial_setup(self.temp_dir)
        self.assertEqual(modrc_dir.name, '.modrc')
        self.assertTrue(modrc_dir.exists())

    def test_create_modrc_file(self):
        """Test .modrc file creation"""
        modrc_dir = setup.initial_setup(self.temp_dir)
        modrc_file = modrc_dir.joinpath('modrc.yml')
        self.assertTrue(modrc_file.exists())

    def test_create_packages_directory(self):
        """Test package directory creation."""
        modrc_dir = setup.initial_setup(self.temp_dir)
        packages_dir = modrc_dir.joinpath('packages')
        self.assertTrue(packages_dir.exists())

    def test_create_live_directory(self):
        """Test live directory creation."""
        modrc_dir = setup.initial_setup(self.temp_dir)
        live_dir = modrc_dir.joinpath('live')
        self.assertTrue(live_dir.exists())


class TestPopulateModRCFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_verify_modrc_dir(self):
        """Test that the ModRC directory is verified before changing the ModRC file."""
        # ModRC dir does not exist
        with self.assertRaises(exceptions.ModRCIntegrityError):
            setup.populate_modrc_file(None, None, None, None)
        pathlib.Path('~/.modrc').expanduser().mkdir()
        # ModRC file does not exist
        with self.assertRaises(exceptions.ModRCIntegrityError):
            setup.populate_modrc_file('test-package', 'vim', False, False)

    def test_set_default_package(self):
        """Tests that the default package is set in the ModRC file."""
        setup.initial_setup()
        setup.populate_modrc_file('test-package', None, None, None)
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as yf:
            modrc_yaml = yaml.safe_load(yf)
        self.assertIn('defaultpackage', modrc_yaml)
        self.assertEqual(modrc_yaml['defaultpackage'], 'test-package')

    def test_set_editor(self):
        """Tests that the editor is set in the ModRC file."""
        setup.initial_setup()
        setup.populate_modrc_file(None, 'vim', None, None)
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as yf:
            modrc_yaml = yaml.safe_load(yf)
        self.assertIn('editor', modrc_yaml)
        self.assertEqual(modrc_yaml['editor'], 'vim')

    def test_set_auto_compile(self):
        """Tests that auto compile is set in the ModRC file."""
        setup.initial_setup()
        setup.populate_modrc_file(None, None, True, None)
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as yf:
            modrc_yaml = yaml.safe_load(yf)
        self.assertIn('autocompile', modrc_yaml)
        self.assertEqual(modrc_yaml['autocompile'], True)

    def test_set_auto_sync(self):
        """Tests that auto sync is set in the ModRC file."""
        setup.initial_setup()
        setup.populate_modrc_file(None, None, None, True)
        modrc_file = helper.get_modrc_file()
        with open(str(modrc_file), 'r') as yf:
            modrc_yaml = yaml.safe_load(yf)
        self.assertIn('autosync', modrc_yaml)
        self.assertEqual(modrc_yaml['autosync'], True)


class TestTeardown(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_teardown(self):
        """Tests that the ModRC directory is destroyed."""
        modrc_dir = setup.initial_setup()
        teardown = setup.teardown()
        self.assertTrue(teardown)
        self.assertFalse(modrc_dir.exists())

    def test_teardown_symlink(self):
        """Tests that the ModRC symlink is destroyed."""
        modrc_dir = setup.initial_setup(self.temp_dir)
        teardown = setup.teardown()
        self.assertTrue(teardown)
        self.assertFalse(modrc_dir.exists())

    def test_modrc_not_setup(self):
        """Tests that an exception is raised if ModRC is not setup."""
        with self.assertRaises(exceptions.ModRCIntegrityError):
            setup.teardown()

    def test_modrc_not_setup_ignore_errors(self):
        """Tests that an exception is not raised if ModRC is not setup and ignore_errors is True."""
        try:
            teardown = setup.teardown(ignore_errors=True)
        except exceptions.ModRCIntegrityError:
            self.fail('teardown() raised ModRCIntegrityError')
        self.assertFalse(teardown)

