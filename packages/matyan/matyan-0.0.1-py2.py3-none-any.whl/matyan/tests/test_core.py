# -*- coding: utf-8 -*-

import copy
import logging
import os
import unittest

import six
from six.moves.urllib.parse import urlsplit

from .. import defaults
from ..conf import get_setting, reset_settings, set_setting
from ..exceptions import (
    TldBadUrl,
    TldDomainNotFound,
    TldImproperlyConfigured,
    TldIOError,
)
from ..helpers import project_dir
from ..utils import (
    get_fld,
    get_tld,
    get_tld_names,
    is_tld,
    parse_tld,
    reset_tld_names,
    update_tld_names,
    update_tld_names_cli,
)

from .base import internet_available_only, log_info

__title__ = 'tld.tests.test_core'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-or-later'
__all__ = ('TestCore',)

LOGGER = logging.getLogger(__name__)


class TestCore(unittest.TestCase):
    """Core tld functionality tests."""

    def setUp(self):
        """Set up."""
        self.good_patterns = [
            {
                'url': 'http://www.google.co.uk',
                'fld': 'google.co.uk',
                'subdomain': 'www',
                'domain': 'google',
                'suffix': 'co.uk',
                'tld': 'co.uk',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'http://www.v2.google.co.uk',
                'fld': 'google.co.uk',
                'subdomain': 'www.v2',
                'domain': 'google',
                'suffix': 'co.uk',
                'tld': 'co.uk',
                'kwargs': {'fail_silently': True},
            },
            # No longer valid
            # {
            #    'url': 'http://www.me.congresodelalengua3.ar',
            #    'tld': 'me.congresodelalengua3.ar',
            #    'subdomain': 'www',
            #    'domain': 'me',
            #    'suffix': 'congresodelalengua3.ar',
            # },
            {
                'url': u'http://хром.гугл.рф',
                'fld': u'гугл.рф',
                'subdomain': u'хром',
                'domain': u'гугл',
                'suffix': u'рф',
                'tld': u'рф',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'http://www.google.co.uk:8001/lorem-ipsum/',
                'fld': 'google.co.uk',
                'subdomain': 'www',
                'domain': 'google',
                'suffix': 'co.uk',
                'tld': 'co.uk',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'http://www.me.cloudfront.net',
                'fld': 'me.cloudfront.net',
                'subdomain': 'www',
                'domain': 'me',
                'suffix': 'cloudfront.net',
                'tld': 'cloudfront.net',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'http://www.v2.forum.tech.google.co.uk:8001/'
                       'lorem-ipsum/',
                'fld': 'google.co.uk',
                'subdomain': 'www.v2.forum.tech',
                'domain': 'google',
                'suffix': 'co.uk',
                'tld': 'co.uk',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'https://pantheon.io/',
                'fld': 'pantheon.io',
                'subdomain': '',
                'domain': 'pantheon',
                'suffix': 'io',
                'tld': 'io',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'v2.www.google.com',
                'fld': 'google.com',
                'subdomain': 'v2.www',
                'domain': 'google',
                'suffix': 'com',
                'tld': 'com',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': '//v2.www.google.com',
                'fld': 'google.com',
                'subdomain': 'v2.www',
                'domain': 'google',
                'suffix': 'com',
                'tld': 'com',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': 'http://foo@bar.com',
                'fld': 'bar.com',
                'subdomain': '',
                'domain': 'bar',
                'suffix': 'com',
                'tld': 'com',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'http://user:foo@bar.com',
                'fld': 'bar.com',
                'subdomain': '',
                'domain': 'bar',
                'suffix': 'com',
                'tld': 'com',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'https://faguoren.xn--fiqs8s',
                'fld': 'faguoren.xn--fiqs8s',
                'subdomain': '',
                'domain': 'faguoren',
                'suffix': 'xn--fiqs8s',
                'tld': 'xn--fiqs8s',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'blogs.lemonde.paris',
                'fld': 'lemonde.paris',
                'subdomain': 'blogs',
                'domain': 'lemonde',
                'suffix': 'paris',
                'tld': 'paris',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': 'axel.brighton.ac.uk',
                'fld': 'brighton.ac.uk',
                'subdomain': 'axel',
                'domain': 'brighton',
                'suffix': 'ac.uk',
                'tld': 'ac.uk',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': 'm.fr.blogspot.com.au',
                'fld': 'fr.blogspot.com.au',
                'subdomain': 'm',
                'domain': 'fr',
                'suffix': 'blogspot.com.au',
                'tld': 'blogspot.com.au',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': u'help.www.福岡.jp',
                'fld': u'www.福岡.jp',
                'subdomain': 'help',
                'domain': 'www',
                'suffix': u'福岡.jp',
                'tld': u'福岡.jp',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': u'syria.arabic.variant.سوريا',
                'fld': u'variant.سوريا',
                'subdomain': 'syria.arabic',
                'domain': 'variant',
                'suffix': u'سوريا',
                'tld': u'سوريا',
                'kwargs': {'fail_silently': True, 'fix_protocol': True},
            },
            {
                'url': u'http://www.help.kawasaki.jp',
                'fld': u'www.help.kawasaki.jp',
                'subdomain': '',
                'domain': 'www',
                'suffix': u'help.kawasaki.jp',
                'tld': u'help.kawasaki.jp',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': u'http://www.city.kawasaki.jp',
                'fld': u'city.kawasaki.jp',
                'subdomain': 'www',
                'domain': 'city',
                'suffix': u'kawasaki.jp',
                'tld': u'kawasaki.jp',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': u'http://fedoraproject.org',
                'fld': u'fedoraproject.org',
                'subdomain': '',
                'domain': 'fedoraproject',
                'suffix': u'org',
                'tld': u'org',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': u'http://www.cloud.fedoraproject.org',
                'fld': u'www.cloud.fedoraproject.org',
                'subdomain': '',
                'domain': 'www',
                'suffix': u'cloud.fedoraproject.org',
                'tld': u'cloud.fedoraproject.org',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': u'https://www.john.app.os.fedoraproject.org',
                'fld': u'john.app.os.fedoraproject.org',
                'subdomain': 'www',
                'domain': 'john',
                'suffix': u'app.os.fedoraproject.org',
                'tld': u'app.os.fedoraproject.org',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'ftp://www.xn--mxail5aa.xn--11b4c3d',
                'fld': 'xn--mxail5aa.xn--11b4c3d',
                'subdomain': 'www',
                'domain': 'xn--mxail5aa',
                'suffix': 'xn--11b4c3d',
                'tld': 'xn--11b4c3d',
                'kwargs': {'fail_silently': True},
            },
            {
                'url': 'http://cloud.fedoraproject.org',
                'fld': 'cloud.fedoraproject.org',
                'subdomain': '',
                'domain': '',
                'suffix': 'cloud.fedoraproject.org',
                'tld': 'cloud.fedoraproject.org',
                'kwargs': {'fail_silently': True}
            },
            {
                'url': 'github.io',
                'fld': 'github.io',
                'subdomain': '',
                'domain': '',
                'suffix': 'github.io',
                'tld': 'github.io',
                'kwargs': {'fail_silently': True, 'fix_protocol': True}
            },
            {
                'url': urlsplit('http://lemonde.fr/article.html'),
                'fld': 'lemonde.fr',
                'subdomain': '',
                'domain': 'lemonde',
                'suffix': 'fr',
                'tld': 'fr',
                'kwargs': {'fail_silently': True}
            },
        ]

        self.bad_patterns = {
            'v2.www.google.com': {
                'exception': TldBadUrl,
            },
            '/index.php?a=1&b=2': {
                'exception': TldBadUrl,
            },
            'http://www.tld.doesnotexist': {
                'exception': TldDomainNotFound,
            },
            'https://2001:0db8:0000:85a3:0000:0000:ac1f:8001': {
                'exception': TldDomainNotFound,
            },
            'http://192.169.1.1': {
                'exception': TldDomainNotFound,
            },
            'http://localhost:8080': {
                'exception': TldDomainNotFound,
            },
            'https://localhost': {
                'exception': TldDomainNotFound,
            },
            'https://localhost2': {
                'exception': TldImproperlyConfigured,
                'kwargs': {'search_public': False, 'search_private': False},
            },
        }

        self.invalid_tlds = {
            'v2.www.google.com',
            'tld.doesnotexist',
            '2001:0db8:0000:85a3:0000:0000:ac1f',
            '192.169.1.1',
            'localhost',
            'google.com',
        }
        reset_settings()

    def tearDown(self):
        """Tear down."""
        reset_settings()

    @property
    def good_url(self):
        return self.good_patterns[0]['url']

    @property
    def bad_url(self):
        return list(self.bad_patterns.keys())[0]

    @log_info
    def test_0_tld_names_loaded(self):
        """Test if tld names are loaded."""
        get_fld('http://www.google.co.uk')
        from ..utils import tld_names
        res = len(tld_names) > 0
        self.assertTrue(res)
        return res

    @internet_available_only
    @log_info
    def test_1_update_tld_names(self):
        """Test updating the tld names (re-fetch mozilla source)."""
        res = update_tld_names(fail_silently=True)
        self.assertTrue(res)
        return res

    @log_info
    def test_2_fld_good_patterns_pass(self):
        """Test good URL patterns."""
        res = []
        for data in self.good_patterns:
            _res = get_fld(data['url'], **data['kwargs'])
            self.assertEqual(_res, data['fld'])
            res.append(_res)
        return res

    @log_info
    def test_3_fld_bad_patterns_pass(self):
        """Test bad URL patterns."""
        res = []
        for url, params in self.bad_patterns.items():
            _res = get_fld(url, fail_silently=True)
            self.assertEqual(_res, None)
            res.append(_res)
        return res

    @log_info
    def test_4_override_settings(self):
        """Testing settings override."""
        def override_settings():
            """Override settings."""
            return get_setting('DEBUG')

        self.assertEqual(defaults.DEBUG, override_settings())

        set_setting('DEBUG', True)

        self.assertEqual(True, override_settings())

        return override_settings()

    @log_info
    def test_5_tld_good_patterns_pass_parsed_object(self):
        """Test good URL patterns."""
        res = []
        for data in self.good_patterns:
            kwargs = copy.copy(data['kwargs'])
            kwargs.update({'as_object': True})
            _res = get_tld(data['url'], **kwargs)
            self.assertEqual(_res.tld, data['tld'])
            self.assertEqual(_res.subdomain, data['subdomain'])
            self.assertEqual(_res.domain, data['domain'])
            self.assertEqual(_res.suffix, data['suffix'])
            self.assertEqual(_res.fld, data['fld'])

            if six.PY3:
                self.assertEqual(
                    str(_res).encode('utf8'),
                    data['tld'].encode('utf8')
                )
            else:
                self.assertEqual(str(_res), data['tld'].encode('utf8'))

            self.assertEqual(
                _res.__dict__,
                {
                    'tld': _res.tld,
                    'domain': _res.domain,
                    'subdomain': _res.subdomain,
                    'fld': _res.fld,
                    'parsed_url': _res.parsed_url,
                }
            )

            res.append(_res)
        return res

    @log_info
    def test_6_override_full_names_path(self):
        default = project_dir('dummy.txt')
        override_base = '/tmp/test'
        set_setting('NAMES_LOCAL_PATH_PARENT', override_base)
        modified = project_dir('dummy.txt')
        self.assertNotEqual(default, modified)
        self.assertEqual(modified, os.path.abspath('/tmp/test/dummy.txt'))

    @log_info
    def test_7_public_private(self):
        res = get_fld(
            'http://silly.cc.ua',
            fail_silently=True,
            search_private=False
        )

        self.assertEqual(res, None)

        res = get_fld(
            'http://silly.cc.ua',
            fail_silently=True,
            search_private=True
        )

        self.assertEqual(res, 'silly.cc.ua')

        res = get_fld(
            'mercy.compute.amazonaws.com',
            fail_silently=True,
            search_private=False,
            fix_protocol=True
        )

        self.assertEqual(res, None)

        res = get_fld(
            'http://whatever.com',
            fail_silently=True,
            search_public=False
        )

        self.assertEqual(res, None)

    @log_info
    def test_8_fld_bad_patterns_exceptions(self):
        """Test exceptions."""
        res = []
        for url, params in self.bad_patterns.items():
            kwargs = params['kwargs'] if 'kwargs' in params else {}
            kwargs.update({'fail_silently': False})
            with self.assertRaises(params['exception']):
                _res = get_fld(url, **kwargs)
                res.append(_res)
        return res

    @log_info
    def test_9_tld_good_patterns_pass(self):
        """Test `get_tld` good URL patterns."""
        res = []
        for data in self.good_patterns:
            _res = get_tld(data['url'], **data['kwargs'])
            self.assertEqual(_res, data['tld'])
            res.append(_res)
        return res

    @log_info
    def test_10_tld_bad_patterns_pass(self):
        """Test `get_tld` bad URL patterns."""
        res = []
        for url, params in self.bad_patterns.items():
            _res = get_tld(url, fail_silently=True)
            self.assertEqual(_res, None)
            res.append(_res)
        return res

    @log_info
    def test_11_parse_tld_good_patterns(self):
        """Test `parse_tld` good URL patterns."""
        res = []
        for data in self.good_patterns:
            _res = parse_tld(data['url'], **data['kwargs'])
            self.assertEqual(
                _res,
                (data['tld'], data['domain'], data['subdomain'])
            )
            res.append(_res)
        return res

    @log_info
    def test_12_is_tld_good_patterns(self):
        """Test `is_tld` good URL patterns."""
        for data in self.good_patterns:
            self.assertTrue(is_tld(data['tld']))

    @log_info
    def test_13_is_tld_bad_patterns(self):
        """Test `is_tld` bad URL patterns."""
        for _tld in self.invalid_tlds:
            self.assertFalse(is_tld(_tld))

    @log_info
    def test_14_fail_update_tld_names(self):
        """Test fail `update_tld_names`."""
        set_setting('NAMES_SOURCE_URL', 'i-do-not-exist')
        # Assert raise TldIOError on wrong NAMES_SOURCE_URL
        with self.assertRaises(TldIOError):
            update_tld_names(fail_silently=False)

        # Assert return False on wrong NAMES_SOURCE_URL
        self.assertFalse(update_tld_names(fail_silently=True))

    @log_info
    def test_15_fail_get_fld_wrong_kwargs(self):
        """Test fail `get_fld` with wrong kwargs."""
        with self.assertRaises(TldImproperlyConfigured):
            get_fld(self.good_url, as_object=True)

    @log_info
    def test_16_fail_parse_tld(self):
        """Test fail `parse_tld`.

        Assert raise TldIOError on wrong `NAMES_SOURCE_URL` for `parse_tld`.
        """
        set_setting('NAMES_SOURCE_URL', 'i-do-not-exist')
        parsed_tld = parse_tld(
            self.bad_url,
            fail_silently=False
        )
        self.assertEqual(parsed_tld, (None, None, None))

    @log_info
    def test_17_get_tld_names_and_reset_tld_names(self):
        """Test fail `get_tld_names` and repair using `reset_tld_names`."""
        set_setting('NAMES_LOCAL_PATH', 'i-do-not-exist')
        set_setting('NAMES_SOURCE_URL', 'i-do-not-exist')
        reset_tld_names()
        # Assert raise TldIOError on wrong NAMES_SOURCE_URL for `get_tld_names`
        with self.assertRaises(TldIOError):
            get_tld_names(fail_silently=False)

        # Assert get None on wrong `NAMES_SOURCE_URL` for `get_tld_names`
        self.assertIsNone(get_tld_names(fail_silently=True))

    @internet_available_only
    @log_info
    def test_18_update_tld_names_cli(self):
        """Test the return code of the CLI version of `update_tld_names`."""
        res = update_tld_names_cli()
        self.assertEqual(res, 0)


if __name__ == '__main__':
    unittest.main()
