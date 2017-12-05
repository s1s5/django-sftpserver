# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys


import paramiko

from django.contrib.auth import get_user_model
from django.test import TestCase

from django_sftpserver import models, sftpserver

if sys.version_info[0] == 2:
    import backports.unittest_mock
    backports.unittest_mock.install()

from unittest.mock import Mock  # NOQA


class TestDjango_sftpserver_sftpserver(TestCase):
    valid_username = 'user'
    invalid_username = 'user2'
    valid_root_name = 'root'
    valid_root_name_2 = 'root_2'

    def setUp(self):
        self.user = get_user_model().objects.create(username=self.valid_username)
        self.valid_key = Mock()
        self.valid_key.get_base64 = Mock(return_value='public_key')
        self.invalid_key = Mock()
        self.invalid_key.get_base64 = Mock(return_value='public_key2')
        models.AuthorizedKey.objects.create(user=self.user, key='public_key')
        root = models.Root.objects.create(name=self.valid_root_name)
        root.users.add(self.user)
        models.Root.objects.create(name=self.valid_root_name_2)

    def test_auth_all(self):
        server = sftpserver.StubServer()
        self.assertEqual(server.check_auth_publickey(self.valid_username, self.valid_key),
                         paramiko.AUTH_SUCCESSFUL)

        self.assertEqual(server.check_auth_publickey(self.valid_username, self.invalid_key),
                         paramiko.AUTH_FAILED)
        self.assertEqual(server.check_auth_publickey(self.invalid_username, self.valid_key),
                         paramiko.AUTH_FAILED)
        self.assertEqual(server.check_auth_publickey(self.invalid_username, self.invalid_key),
                         paramiko.AUTH_FAILED)

    def test_auth_root(self):
        server = sftpserver.StubServer()
        name = '{}:{}'.format(self.valid_username, self.valid_root_name)
        self.assertEqual(server.check_auth_publickey(name, self.valid_key),
                         paramiko.AUTH_SUCCESSFUL)

        name = '{}:{}'.format(self.valid_username, self.valid_root_name_2)
        self.assertEqual(server.check_auth_publickey(name, self.valid_key),
                         paramiko.AUTH_FAILED)

        name = '{}:{}invalid'.format(self.valid_username, self.valid_root_name)
        self.assertEqual(server.check_auth_publickey(name, self.valid_key),
                         paramiko.AUTH_FAILED)

    def test_auth_root_with_branch(self):
        pass


class TestDjango_sftpserver_sftpserver_with_root(TestCase):
    def setUp(self):
        self.root = models.Root.objects.create(name="root_example")
        self.server = sftpserver.StubServer()
        self.server.user = None
        self.server.root = self.root
        self.sftpserver = sftpserver.StubSFTPServer(self.server)
        self.sftpserver.session_started()


class TestDjango_sftpserver_sftpserver_without_root(TestCase):
    def setUp(self):
        pass