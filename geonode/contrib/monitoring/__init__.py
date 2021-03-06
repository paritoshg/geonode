# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import logging
from django.utils.translation import ugettext_noop as _

from geonode.notifications_helper import NotificationsAppConfigBase, has_notifications
from django.db.models.signals import post_migrate

log = logging.getLogger(__name__)


def run_setup_hooks(*args, **kwargs):
    if not has_notifications:
        log.warning("Monitoring requires notifications app to be enabled. "
                    "Otherwise, no notifications will be send")
    from geonode.contrib.monitoring.models import populate
    populate()


class MonitoringAppConfig(NotificationsAppConfigBase):
    name = 'geonode.contrib.monitoring'
    NOTIFICATION_NAME = 'monitoring_alert'
    NOTIFICATIONS = ((NOTIFICATION_NAME,
                      _("Monitoring alert"),
                      _("Alert situation reported by monitoring"),
                     ),
                    )

    def ready(self):
        super(MonitoringAppConfig, self).ready()
        post_migrate.connect(run_setup_hooks, sender=self)


default_app_config = 'geonode.contrib.monitoring.MonitoringAppConfig'
