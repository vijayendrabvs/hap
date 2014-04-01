#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo.config import cfg

from neutron.api.v2 import attributes
from neutron.db.loadbalancer import loadbalancer_db
from neutron.openstack.common import log as logging
from neutron.plugins.common import constants
from neutron.services.loadbalancer.drivers import abstract_driver

LOG = logging.getLogger(__name__)

#OPTS = None
#cfg.CONF.register_opts(OPTS, 'dummy')

HAPROXY_REMOTE_OPTS = [
    cfg.StrOpt(
        'haproxy_ip',
        help=_('The ip to reach the haproxy lb.'),
    ),
    cfg.StrOpt(
        'haproxy_username',
        help=_('Username to login to the server running haproxy.'),
    ),
    cfg.StrOpt(
        'haproxy_password',
        help=_('Password to login to the server running haproxy.'),
    )
]

cfg.CONF.register_opts(HAPROXY_REMOTE_OPTS, 'dummy')


class DummyPluginDriver(abstract_driver.LoadBalancerAbstractDriver):

    def __init__(self, plugin):
        self.plugin = plugin
        import pdb; pdb.set_trace()
        print "inside __init__ of remote plugin driver!"
        haproxy_ip = cfg.CONF.dummy.haproxy_ip
        haproxy_username = cfg.CONF.dummy.haproxy_username
        haproxy_password = cfg.CONF.dummy.haproxy_password
        #self.client = ncc_client.NSClient(ncc_uri,
        #                                  ncc_username,
        #                                  ncc_password)

    def create_vip(self, context, vip):
        print "inside create_vip of remote plugin driver!"
        import pdb; pdb.set_trace()
        status = constants.ACTIVE
        self.plugin.update_status(context, loadbalancer_db.Vip, vip["id"],
                                  status)

    def update_vip(self, context, old_vip, vip):
        print "inside update_vip of remote plugin driver!"
        import pdb; pdb.set_trace()

    def delete_vip(self, context, vip):
        print "inside delete_vip of remote plugin driver!"
        import pdb; pdb.set_trace()

    def create_pool(self, context, pool):
        print "inside create_pool of remote plugin driver!"
        import pdb; pdb.set_trace()
        status = constants.ACTIVE
        self.plugin.update_status(context, loadbalancer_db.Pool,
                                  pool['id'], status)

    def update_pool(self, context, old_pool, pool):
        print "inside update_pool of remote plugin driver!"
        import pdb; pdb.set_trace()

    def delete_pool(self, context, pool):
        print "inside delete_pool of remote plugin driver!"
        import pdb; pdb.set_trace()
        self.plugin._delete_db_pool(context, pool['id'])

    def create_member(self, context, member):
        print "inside create_pool of remote plugin driver!"
        import pdb; pdb.set_trace()

    def update_member(self, context, old_member, member):
        print "inside update_member of remote plugin driver!"
        import pdb; pdb.set_trace()

    def delete_member(self, context, member):
        print "inside delete_member of remote plugin driver!"
        import pdb; pdb.set_trace()

    def create_pool_health_monitor(self, context, health_monitor, pool_id):
        print "inside create_pool_health_monitor in remote plugin driver!"
        import pdb; pdb.set_trace()

    def update_pool_health_monitor(self, context, old_health_monitor,
                                   health_monitor, pool_id):
        print "inside update_pool_health_monitor in remote plugin driver!"
        import pdb; pdb.set_trace()

    def delete_pool_health_monitor(self, context, health_monitor, pool_id):
        print "inside delete_pool_health_monitor of remote plugin driver!"
        import pdb; pdb.set_trace()

    def stats(self, context, pool_id):
        print "inside stats of remote plugin driver!"
        import pdb; pdb.set_trace()
