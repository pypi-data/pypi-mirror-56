"""
    zoom.sites

    Updated Zoom sites module.  Eventually, the functionality
    currently in zoom.site will make it's way here.

    Note: experimental
"""

import os
import logging

import zoom
from zoom.site import Site as BasicSite

class BackgroundJob(object):
    """Background Job"""
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.cron = '* * * * *'
        self.scheduled = 'never'
        self.status = 'paused'

    def __repr__(self):
        return 'BackgroundJob(%r)' % self.name

class Site(BasicSite):
    """a Zoom site

    A zoom site can be completely determined by the path to the
    site directory.  That directory may contain a config file,
    apps, and other assets.  If any assets are required that are
    not found in the site directory, the system will look in
    the default site as a fallback.  Any site setttings not found
    in the site config file will be obtained from the default
    site.  Any settings not found there will rely on built-in
    defaults.

    This Site object is not to be confused with the zoom.site.Site
    object, renamed here as BasicSite, which will eventually be
    phased out as that functionality is brought into this module.

    >>> site = Site()
    >>> site.name
    'localhost'

    >>> 'users' in site.db.get_tables()
    True
    """

    def __init__(self, path=None):

        # prepare a fake request adapter to satisfy the legacy api
        path = path or zoom.tools.zoompath('web', 'sites', 'localhost')
        if not os.path.isdir(path):
            raise Exception('Site missing: %s' % path)
        rest, name = os.path.split(path)
        instance, _ = os.path.split(rest)
        fake_request_adapter = zoom.utils.Bunch(
            site_path=path,
            instance=instance,
            domain=name,
            protocol='http',
            host=name,
        )

        # create a site based on the legacy api
        BasicSite.__init__(self, fake_request_adapter)
        self.instance_path = instance

        # attach the supporting database attributes
        self.db = db = zoom.database.connect_database(self.config)
        self.queues = zoom.queues.Queues(db)
        self.groups = zoom.models.Groups(db)
        self.users = zoom.models.Users(db)

    def get_background_jobs(self):
        """Returns a dict of background jobs

        >>> site = Site()
        >>> site.name
        'localhost'
        >>> site.get_background_jobs()
        [BackgroundJob('hello')]
        """
        result = []
        for path in self.apps_paths:
            app_path = os.path.realpath(os.path.join(self.path, path))
            for app_name in os.listdir(app_path):
                pathname = os.path.join(app_path, app_name, 'background.py')
                if os.path.isfile(pathname):
                    result.append(BackgroundJob(app_name, pathname))
        return result


class SiteProxy(object):
    """Site proxy"""

    def __init__(self, path):
        self.name = os.path.split(path)[-1]
        self.path = path

    def run_background_jobs(self):
        """Run background jobs

        Iterates through the apps in the site and calls
        run_background_jobs on each one.

        >>> import zoom
        >>> site_directory = zoom.tools.zoompath('web/sites/localhost')
        >>> site = SiteProxy(site_directory)
        >>> site.run_background_jobs()
        localhost
        """
        logger = logging.getLogger(__name__)
        logger.info('running background jobs for site %r', self.name)

        # create a concrete site object
        site = Site(self.path)

        print(self.name)

        logger.info('finished background jobs for site %r',self.name)

    def __repr__(self):
        return 'Site(%r)' % (self.name)

