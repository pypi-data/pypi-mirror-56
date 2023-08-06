"""" Represents an Airfinder Site. """
import logging

from conductor.airfinder.base import AirfinderSubject
from conductor.airfinder.area import Area
from conductor.airfinder.devices.access_point import AccessPoint
from conductor.airfinder.devices.location import Location
from conductor.airfinder.devices.tag import Tag
from conductor.util import find_cls

LOG = logging.getLogger(__name__)


class SiteUser():
    """
    This class is used to manage other Airfinder SiteUsers,
    given the User has Admin-level permissions.
    """
    subject_name = 'SiteUser'

    SITE_USER_PERMISSIONS = {
        "Admin": False,
        "Status": True,
        "AddTags": True,
        "EditDeleteTags": True,
        "EditDeleteGroupsCategories": False
    }

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    @property
    def can_add_tags(self):
        """ Can the SiteUser add tags? """
        return bool(self._md.get('AddTags'))

    @property
    def is_admin(self):
        """ Is the SiteUser an Admin? """
        return bool(self._md.get('Admin'))

    @property
    def can_edit_delete_groups_categories(self):
        """ Can the SiteUser Edit/Delete Groups and Categories? """
        return bool(self._md.get('EditDeleteGroupsCategories'))

    @property
    def can_edit_delete_tags(self):
        """ Can the SiteUser Edit/Delete tags? """
        return bool(self._md.get('EditDeleteTags'))

    @property
    def email(self):
        """ The SiteUser's email address. """
        return self._md.get('email')

    @property
    def user_id(self):
        return self._md.get('userId')

    @property
    def status(self):
        return bool(self._md.get('Status'))

    @property
    def site(self):
        return Site(self.session, self._md.get('siteId'))

    def forgot_password(self):
        """ Sends the site user an email to reset their password. """
        url = ''.join([self._af_network_asset_url, 'users/forgotPassword'])
        params = {'email': self.email}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def resend_email(self):
        """ Resends the site user an email to reset their password. """
        url = ''.join([self._af_network_asset_url, 'users/resend'])
        params = {'email': self.email}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


class Site(AirfinderSubject):
    """ Represents an Airfinder Site. """
    subject_name = 'Site'

    def _get_registered_asset_by_site(self, subject_name, subject_id,
                                      group_by=""):
        """ Gets a registered asset by site-id. """
        url = ''.join([self._af_network_asset_url, '/{}/{}/'.format(
            subject_name, subject_id)])
        params = {'siteId': self.subject_id, 'groupBy': group_by}
        return self._get(url, params)

    def _get_registered_assets_by_site(self, asset_name, group_by=""):
        """ Gets all the registered assets by site-id. """
        url = ''.join([self._af_network_asset_url, asset_name])
        params = {'siteId': self.subject_id, 'groupBy': group_by}
        return self._get(url, params=params)

    def rename(self, name):
        """ Rename an existing site. """
        # TODO
        url = ''.join([self._af_network_asset_url, "/sites"])
        params = {'siteId': self.subject_id}
        updates = {
            "name": name,
        }
        self._data = self._put(url, params, updates)

    def get_site_users(self):
        """ Gets all the site-users, in the site. """
        return [SiteUser(self.session, x.get('id'), _data=x) for x in
                self._get_registered_assets_by_site('users')]

    def get_site_user(self, site_user_id):
        """ Gets a site-user in a site. """
        x = self._get_registered_asset_by_site("/user", site_user_id)
        return SiteUser(self.session, x.get('id'), _data=x)

    def get_areas(self):
        """ Gets all the areas for a site. """
        return [Area(self.session, x.get('id'), self, _data=x) for x in
                self._get_registered_assets_by_site("/areas")]

    def create_area(self, name):
        """ Create an area as a part of this Site. """
        url = ''.join([self._af_network_asset_url, "/area"])
        params = {'siteId': self.subject_id}
        return self._get(url, params)

    def delete_area(self, area_id):
        """ Delete an area. """
        url = ''.join([self._af_network_asset_url, "area"])
        params = {'siteId': self.subject_id}
        return self._delete(url, params)

    def get_area(self, area_id):
        """ Gets an area in a site. """
        x = self._get_registered_asset_by_site('area', area_id)
        return Area(self.session, x.get('id'), self, _data=x)

    def remove_location(self, locations):
        """ Remove locations from a Site. """
        # TODO: test
        url = ''.join([self._af_network_asset_url, 'location'])
        data = {
            "nodeAddresses": [locations],
            "siteId": self.subject_id
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_access_points(self):
        assets = self._get_registered_assets_by_site('/accesspoints')
        aps = []
        for x in assets:
            subject_id = x['nodeAddress']
            cls = find_cls(AccessPoint, x['registrationToken'])
            if cls:
                aps.append(cls(session=self.session, subject_id=subject_id,
                               instance=self.instance, _data=x))
            else:
                LOG.error("{} {}".format(subject_id, x['registrationToken']))
                aps.append(AccessPoint(session=self.session,
                                       subject_id=subject_id,
                                       instance=self.instance,
                                       _data=x))
        return aps

    def get_locations(self):
        """ Gets all the locations in a site. """
        nodes = []
        for x in self._get_registered_assets_by_site('/locations', 'none'):
            subject_id = x.get('id') if 'id' in x else x.get('nodeAddress')
            obj = find_cls(Location, x['registrationToken'])
            if obj:
                nodes.append(obj(self.session, subject_id, self.instance, x))
            else:
                dev = x['assetInfo']['metadata']['props'].get('deviceType')
                LOG.error("No device conversion for {}".format(dev))
                nodes.append(Location(self.session, subject_id, self.instance, x))
        return nodes

    def get_location(self, mac_id):
        """ Gets a location in the site. """
        return self._get_registered_asset_by_site('/tag', mac_id)

    def get_tags(self):
        """ Gets all the tags in a site. """
        nodes = []
        for x in self._get_registered_assets_by_site('/tags', 'none'):
            subject_id = x.get('id') if 'id' in x else x.get('nodeAddress')
            obj = find_cls(Tag, x['registrationToken'])
            if obj:
                nodes.append(obj(self.session, subject_id, self.instance, x))
            else:
                dev = x['assetInfo']['metadata']['props'].get('deviceType')
                LOG.error("No device conversion for {}".format(dev))
                nodes.append(Tag(self.session, subject_id, self.instance, x))
        return nodes

    def get_tag(self, mac_id):
        """ Gets a tag in the site. """
        return self._get_registered_asset_by_site('/tag', mac_id)

    def add_tag(self, mac_id, field1="", field2="", category="",
                description=""):
        """ Adds a tag in the site. """
        url = ''.join([self._af_network_asset_url, '/tags'])
        data = {
            "accountId": self._md.get('accountId'),
            "macAddress": mac_id.mac_address,
            "siteId": self.subject_id,
            "description": description,
            "categoryId": category,
            "field1": field1,
            "field2": field2,
        }
        print(data)
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def bulk_add_tags(self, file_name):
        """ Bulk-add tags to an airfinder site. """
        raise NotImplementedError

    def remove_tag(self, mac_id):
        """ Remove a tag to an airfinder site. """
        url = ''.join([self._af_network_asset_url, '/tag'])
        data = {
            "nodeAddress": str(mac_id),
            "accountId": self._md.get('accountId'),
            "siteId": self.subject_id
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()

#    def bulk_add_locations(self, file_name):
#        """ Bulk-add locations to a site. """
#        raise NotImplemented

#    def get_groups(self):
#        """ Get all the groups in a site. """
#        return self._get_registered_assets_by_site('groups')

#    def get_group(self, group_id):
#        """ Get a group from a site. """
#        return self._get_registered_asset_by_site('group', group_id)

#    def get_categories(self):
#        """ Get all the categories in a site."""
#        return self._get_registered_assets_by_site('categories')

#    def get_category(self, category_id):
#        """ Get a category in a site. """
#        return self._get_registered_asset_by_site('category', category_id)

    def get_asset_group(self):
        """ Get the Site as an Asset Group. """
        x = _get_registered_asset_by_site('assetGroup')
        return AssetGroup(self.session, x['id'], _data=x)

    @property
    def area_count(self):
        """ Returns the number of Areas within the Site. """
        val = self._md.get('areaCount')
        return int(val) if val else None

