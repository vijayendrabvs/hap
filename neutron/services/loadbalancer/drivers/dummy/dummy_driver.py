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
import random
import string

from neutron.api.v2 import attributes
from neutron.db.loadbalancer import loadbalancer_db
from neutron.openstack.common import log as logging
from neutron.plugins.common import constants
from neutron.services.loadbalancer.drivers import abstract_driver
from neutron.services.loadbalancer.drivers.dummy import haproxy_client
from neutron.services.loadbalancer.drivers.dummy import haproxy_cfg

LOG = logging.getLogger(__name__)

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
    ),
    cfg.StrOpt(
        'haproxy_ssh_port',
        help=_('SSH port to login to the server running haproxy.'),
    ),
    cfg.StrOpt(
        'haproxy_config_file',
        help=_('HAProxy config file path.'),
    ),
    cfg.StrOpt(
        'haproxy_pid_file',
        help=_('HAProxy pid file path.'),
    )
]

cfg.CONF.register_opts(HAPROXY_REMOTE_OPTS, 'dummy')


class DummyPluginDriver(abstract_driver.LoadBalancerAbstractDriver):

    hap_ip = ""
    hap_username = ""
    hap_password = ""
    hap_ssh_port = ""
    hap_cfg_file = ""

    def __init__(self, plugin):
        self.plugin = plugin
        import pdb; pdb.set_trace()
        print "inside __init__ of remote plugin driver!"
        self.hap_ip = cfg.CONF.dummy.haproxy_ip
        self.hap_username = cfg.CONF.dummy.haproxy_username
        self.hap_password = cfg.CONF.dummy.haproxy_password
        self.hap_ssh_port = cfg.CONF.dummy.haproxy_ssh_port
        self.hap_cfg_file = cfg.CONF.dummy.haproxy_config_file
        self.hap_pid_file = cfg.CONF.dummy.haproxy_pid_file
        if self.hap_ssh_port is None:
            self.hap_ssh_port = 22
        #self.client = haproxy_client.HAProxyClient(haproxy_ip,
        #                                  haproxy_username,
        #                                  haproxy_password,
        #                                  haproxy_ssh_port)
        #self.client = haproxy_client.HAProxyClient.gethaproxyclient(haproxy_ip,
        #                                  haproxy_username,
        #                                  haproxy_password,
        #                                  haproxy_ssh_port)

    def create_vip(self, context, vip):
        print "inside create_vip of remote plugin driver!"
        import pdb; pdb.set_trace()
        client = haproxy_client.HAProxyClient(self.hap_ip,
                                          self.hap_username,
                                          self.hap_password,
                                          self.hap_ssh_port)
        status = constants.ACTIVE
        # First, get the remote haproxy.cfg file here.
        randfilename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        tmpfile = "/tmp/" + randfilename
        sftps = client.session.open_sftp()
        sftps.get(self.hap_cfg_file, tmpfile)
        blk_name_t_map, blk_name_c_map = haproxy_cfg.loadhaproxycfgfile(tmpfile)
        # blk_name_t_map must either have a frontend and a backend
        # corresponding to this VIP, or if no VIP has ever existed,
        # nothing to begin with.
        # For now, assume we have nothing to begin with,
        # and that we create a new frontend and backend each time.
        frontendname = "frontend-vip-" + vip['address']
        backendname = "backend-vip-" + vip['address']
        frontend = haproxy_cfg.createfrontend(frontendname, backendname, str(vip['address']), str(vip['protocol_port']), str(vip['protocol']))
        balance = "roundrobin"
        backend = haproxy_cfg.createbackend(backendname, str(vip['protocol']), balance)
        # Add this frontend to content map.
        blk_name_c_map[frontendname] = frontend
        # Also add type to type map.
        blk_name_t_map[frontendname] = "frontend"
        # Add backend to content map.
        blk_name_c_map[backendname] = backend
        # Add backend name and type to type map.
        blk_name_t_map[backendname] = "backend"
        # Rewrite this new map to the same temp file - we don't need it anymore.
        haproxy_cfg.writehaproxycfgfile(tmpfile, blk_name_c_map, blk_name_t_map)
        # Now put this file in the remote haproxy.cfg file's place.
        sftps.put(tmpfile, self.hap_cfg_file)
        # Next reload the haproxy.
        cmd = "haproxy -f " + self.hap_cfg_file + " -p " + self.hap_pid_file
        rc = client.exec_cmd(cmd)
        #blk_name_t_map
        #rc = client.exec_cmd(cmd)
        print "rc is --> " + str(rc)
        client.session.close()
        self.plugin.update_status(context, loadbalancer_db.Vip, vip["id"],
                                  status)

    def update_vip(self, context, old_vip, vip):
        print "inside update_vip of remote plugin driver!"
        import pdb; pdb.set_trace()

    def delete_vip(self, context, vip):
        print "inside delete_vip of remote plugin driver!"
        import pdb; pdb.set_trace()
        self.plugin._delete_db_vip(context, vip['id'])

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
