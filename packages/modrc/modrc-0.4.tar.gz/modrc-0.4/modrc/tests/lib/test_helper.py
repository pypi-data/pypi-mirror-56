import pathlib
import tempfile
import unittest

from parameterized import parameterized

from modrc import exceptions
from modrc.lib import helper, setup


class TestVerifyModRCDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_modrc_dir_does_not_exist(self):
        """Tests that a folder does not exist at the given path."""
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.verify_modrc_dir()

    def test_modrc_file_does_not_exist(self):
        """Tests that the .modrc file exists at the given path."""
        modrc_dir = pathlib.Path('~/.modrc').expanduser()
        modrc_dir.mkdir()
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.verify_modrc_dir()

    def test_success(self):
        """Tests that the ModRC directory is valid at a given path."""
        setup.initial_setup()
        self.assertTrue(helper.verify_modrc_dir())


class TestGetModRCDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_does_not_exist(self):
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.get_modrc_dir()

    def test_symlinked(self):
        modrc_dir = setup.initial_setup(self.temp_dir)
        self.assertEqual(modrc_dir, helper.get_modrc_dir())


class TestGetModRCFile(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_does_not_exist(self):
        modrc_dir = pathlib.Path('~/.modrc').expanduser()
        modrc_dir.mkdir()
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.get_modrc_file()

    def test_exists(self):
        modrc_dir = setup.initial_setup(self.temp_dir)
        modrc_file = helper.get_modrc_file()
        self.assertEqual(modrc_file, modrc_dir.joinpath('modrc.yml'))


class TestGetPackagesDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_invalid_modrc_dir(self):
        """Tests that a exceptions.ModRCIntegrityError is raised for an invalid ModRC directory."""
        # create a path for a non-existant ModRC directory
        modrc_dir = self.temp_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        # test that an exception is raised
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.get_packages_dir()

    def test_packages_dir_does_not_exist(self):
        """Tests that a exceptions.ModRCIntegrityError is raised if the packages directory does not exist."""
        # setup the ModRC directory without a packages directory
        modrc_dir = self.temp_dir.joinpath('.modrc')
        modrc_file = modrc_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        modrc_file.touch()
        # test that an exception is raised
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.get_packages_dir()

    def test_success(self):
        """Tests that the path for the packages directory is retrieved successfully."""
        modrc_dir = setup.initial_setup(self.temp_dir)
        packages_dir = modrc_dir.joinpath('packages')
        self.assertEqual(packages_dir, helper.get_packages_dir())


class TestGetLiveDir(unittest.TestCase):
    def setUp(self):
        # setup a temporary mock home directory
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = pathlib.Path(self.temp.name)

    def tearDown(self):
        # destroy the ModRC symlink
        setup.teardown(ignore_errors=True)
        # destroy the temp directory
        self.temp.cleanup()

    def test_invalid_modrc_dir(self):
        """Tests that a exceptions.ModRCIntegrityError is raised for an invalid ModRC directory."""
        # create a path for a non-existant ModRC directory
        modrc_dir = self.temp_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        # test that an exception is raised
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.get_live_dir()

    def test_live_dir_does_not_exist(self):
        """Tests that a exceptions.ModRCIntegrityError is raised if the live directory does not exist."""
        # setup the ModRC directory without a live directory
        modrc_dir = self.temp_dir.joinpath('.modrc')
        modrc_file = modrc_dir.joinpath('.modrc')
        modrc_dir.mkdir()
        modrc_file.touch()
        # test that an exception is raised
        with self.assertRaises(exceptions.ModRCIntegrityError):
            helper.get_live_dir()

    def test_success(self):
        """Tests that the path for the live directory is retrieved successfully."""
        modrc_dir = setup.initial_setup(self.temp_dir)
        live_dir = modrc_dir.joinpath('live')
        self.assertEqual(live_dir, helper.get_live_dir())


class TestValidFilterName(unittest.TestCase):
    @parameterized.expand([
        ('global')
    ])
    def test_valid(self, filter_name):
        """Test generally valid filter names."""
        self.assertTrue(helper.valid_filter_name(filter_name))

    @parameterized.expand([
        (''),
        ('random'),
        ('.global'),
        ('global.'),
        ('.global.')
    ])
    def test_invalid(self, filter_name):
        """Test generally invalid filter names."""
        self.assertFalse(helper.valid_filter_name(filter_name))

    @parameterized.expand([
        ('macos'),
        ('macos.10'),
        ('macos.10.10'),
        ('macos.10.20'),
        ('macos.10.20.0'),
        ('macos.10.20.5')
    ])
    def test_macos_valid(self, filter_name):
        """Test macOS valid filter names."""
        self.assertTrue(helper.valid_filter_name(filter_name))

    @parameterized.expand([
        ('macos.9'),
        ('macos.11'),
        ('macos.9.0'),
        ('macos.11.0'),
        ('macos.9.0.0'),
        ('macos.11.0.0'),
        ('macos.10.0.0.0'),
        ('macos.10.a'),
        ('macos.10.1.b'),
        ('macos.10.1.2.c')
    ])
    def test_macos_invalid(self, filter_name):
        """Test macOS invalid filter names."""
        self.assertFalse(helper.valid_filter_name(filter_name))

    @parameterized.expand([
        ('linux'),
        ('linux.distro'),
        ('linux.distro.10'),
        ('linux.distro.8.17'),
        ('linux.distro.3.72.31')
    ])
    def test_linux_valid(self, filter_name):
        """Test linux valid filter names."""
        self.assertTrue(helper.valid_filter_name(filter_name))

    @parameterized.expand([
        ('linux.4'),
        ('linux.32.7'),
        ('linux.2.99.67')
    ])
    def test_linux_invalid(self, filter_name):
        """Test linux invalid filter names."""
        self.assertFalse(helper.valid_filter_name(filter_name))

    @parameterized.expand([
        ('d70751763e70'),
        ('fd8c03658fa4'),
        ('22f93c7e100d')
    ])
    def test_mac_address_valid(self, mac_address):
        """Test valid MAC addresses."""
        self.assertTrue(helper.valid_filter_name(mac_address))

    @parameterized.expand([
        ('AAAAAAAAAAAA'),
        ('aa:aa:aa:aa:aa'),
        ('aa-aa-aa-aa-aa-aa'),
        ('00000000000'),
        ('0000000000000'),
        ('g0000000000z')
    ])
    def test_mac_address_invalid(self, mac_address):
        """Test invalid MAC addresses."""
        self.assertFalse(helper.valid_filter_name(mac_address))
