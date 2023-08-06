#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Kitsu tracking class for Artella projects
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import logging

from tpPyUtils import decorators
from tpQtLib.core import qtutils

import artellapipe.register
from artellapipe.managers import tracking
import artellapipe.libs.kitsu as kitsu_lib
from artellapipe.libs.kitsu.core import kitsulib, kitsuclasses

LOGGER = logging.getLogger()


@decorators.Singleton
class KitsuTrackingManager(tracking.TrackingManager, object):
    def __init__(self):
        tracking.TrackingManager.__init__(self)

        self._email = None
        self._password = None
        self._store_credentials = False
        self._user_data = dict()
        self._entity_types = list()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password

    @property
    def store_credentials(self):
        return self._store_credentials

    @store_credentials.setter
    def store_credentials(self, new_store_credentials):
        self._store_credentials = new_store_credentials

    @property
    def user_data(self):
        return self._user_data

    def reset_user_info(self):
        """
        Function that resets the information stored of the user
        """

        self._email = None
        self._password = None
        self._store_credentials = False
        self._user_data = None

    def set_project(self, project):
        """
        Overrides base TrackingManager
        :param project: ArtellaProject
        """

        tracking.TrackingManager.set_project(self, project)
        self._load_user_settings()

    def update_tracking_info(self):
        print('Updating trackign info ...')

    def is_tracking_available(self):

        return kitsulib.host_is_up()

    def login(self, *args, **kwargs):

        email = kwargs.get('email', self._email)
        password = kwargs.get('password', self._password)
        store_credentials = kwargs.get('store_credentials', self._store_credentials)

        if not email or not password:
            LOGGER.warning('Impossible to login into Kitsu because username or password are not valid!')
            return False

        gazup_api = kitsu_lib.config.get('gazu_api', default=None)
        if not gazup_api:
            LOGGER.warning('Impossible to login into Kitsu because Gazu API is not available!')
            return False

        kitsulib.set_host(gazup_api)
        if not kitsulib.host_is_up():
            LOGGER.warning('Impossible to login into Kitsu because Gazu API is not available: "{}"'.format(gazup_api))
            qtutils.show_warning(
                None, 'Kitsu server is down!',
                'Was not possible to retrieve Gazu API. '
                'This usually happens when Kitsu server is down. Please contact TD!')
            return False

        try:
            valid_login = kitsulib.log_in(email, password)
            self._logged = bool(valid_login)
            self._user_data = kitsulib.get_current_user()
            self._project.settings.set('kitsu_store_credentials', store_credentials)
            if store_credentials:
                self._project.settings.set('kitsu_email', email)
                self._project.settings.set('kitsu_password', password)
            self.logged.emit()
            return True
        except Exception as exc:
            self._logged = False
            self.reset_user_info()
            return False

    def logout(self, *args, **kwargs):

        if not self.is_logged():
            LOGGER.warning('Impossible to logout from Kitsu because you are not currently logged')
            return False

        kitsulib.set_host(None)
        self._logged = False
        self.reset_user_info()

        remove_credentials = kwargs.get('remove_credentials', False)
        if remove_credentials:
            self._project.settings.set('kitsu_email', '')
            self._project.settings.set('kitsu_password', '')
            self._project.settings.set('kitsu_store_credentials', False)

        self._load_user_settings()

        return True

    def all_project_assets(self):

        if not self.is_logged():
            LOGGER.warning('Impossible to retrieve assets because user is not logged into Kitsu!')
            return

        assets_path = artellapipe.AssetsMgr().get_assets_path()
        if not artellapipe.AssetsMgr().is_valid_assets_path():
            LOGGER.warning('Impossible to retrieve assets from invalid assets path: "{}"'.format(assets_path))
            return

        project_id = kitsu_lib.config.get('project_id', default=None)
        if not project_id:
            LOGGER.warning('Impossible to retrieve assets because does not defines a valid Kitsu ID')
            return

        kitsu_assets = kitsulib.all_assets_for_project(project_id=project_id)
        asset_types = self.update_entity_types_from_kitsu(force=False)
        category_names = [asset_type.name for asset_type in asset_types]

        assets_data = list()
        for kitsu_asset in kitsu_assets:
            entity_type = self.get_entity_type_by_id(kitsu_asset.entity_type_id)
            if not entity_type:
                LOGGER.warning(
                    'Entity Type {} for Asset {} is not valid! Skipping ...'.format(entity_type, kitsu_asset.name))
                continue
            assets_data.append(
                {
                    'asset': kitsu_asset,
                    'name': kitsu_asset.name,
                    'thumb': kitsu_asset.preview_file_id,
                    'category': entity_type.name
                }
            )

        return assets_data

    def download_preview_file_thumbnail(self, preview_id, file_path):

        kitsulib.download_preview_file_thumbnail(preview_id=preview_id, file_path=file_path)

    def update_entity_types_from_kitsu(self, force=False):
        """
        Updates entity types from Kitsu project
        :param force: bool, Whether to return force the update if entity types are already retrieved
        :return: list(KitsuEntityType)
        """

        if not self.is_logged():
            return list()

        if self._entity_types and not force:
            return self._entity_types

        entity_types_list = kitsulib.get_project_entity_types()
        entity_types = [kitsuclasses.KitsuEntityType(entity_type) for entity_type in entity_types_list]
        self._entity_types = entity_types

        return self._entity_types

    def get_entity_type_by_id(self, entity_type_id, force_update=False):
        """
        Returns entity type name by the given project
        :param entity_type_id: str
        :param force_update: bool, Whether to force entity types sync if they are not already snced
        :return: str
        """

        if not self.is_logged():
            return list()

        if force_update or not self._entity_types:
            self.update_entity_types_from_kitsu(force=True)

        for entity_type in self._entity_types:
            if entity_type.id == entity_type_id:
                return entity_type

        return ''

    def _load_user_settings(self):
        """
        Internal function that tries to retrieve user data from project settings
        """

        if not self._project:
            return None

        self._email = self._project.settings.get(
            'kitsu_email') if self._project.settings.has_setting('kitsu_email') else None
        self._password = self._project.settings.get(
            'kitsu_password') if self._project.settings.has_setting('kitsu_password') else None
        self._store_credentials = self._project.settings.get(
            'kitsu_store_credentials') if self._project.settings.has_setting('kitsu_store_credentials') else False


artellapipe.register.register_class('Tracker', KitsuTrackingManager)
