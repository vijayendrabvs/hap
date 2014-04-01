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

import requests
import paramiko
import socket

from neutron.common import exceptions as n_exc
from neutron.openstack.common import jsonutils
from neutron.openstack.common import log as logging

LOG = logging.getLogger(__name__)

class HAProxyException(n_exc.NeutronException):

    """Represents exceptions thrown by HAProxyClient."""

    CONNECTION_ERROR = 1
    EXEC_ERROR = 2
    RUNTIME_ERROR = 2

    def __init__(self, error):
        self.message = _("Haproxy client error %d") % error
        super(HAProxyException, self).__init__()
        self.error = error


class HAProxyClient(object):

    """Client to operate on remote HAProxy instance via ssh."""

    session = None
    haproxy_ip = None
    username = None
    password = None
    ssh_port = None

    def __init__(self, haproxy_ip, username, password, ssh_port=22):
        if not haproxy_ip:
            msg = _("No Haproxy IP provided")
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.CONNECTION_ERROR)
        else:
            self.haproxy_ip = haproxy_ip

        if not username:
            msg = _("No username provided")
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.CONNECTION_ERROR)
        else:
            self.username = username

        if not password:
            msg = _("No password provided")
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.CONNECTION_ERROR)
        else:
            self.password = password

        try:
            self.session = paramiko.SSHClient()
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.session.connect(haproxy_ip, int(ssh_port), username, password)
        except socket.error as se:
            msg =  "Unable to connect to specified haproxy server"
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.CONNECTION_ERROR)
        except paramiko.AuthenticationException as pa:
            msg = "Failed to login using provided credential information"
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.CONNECTION_ERROR)
        except Exception as e:
            msg = "Caught exception while attempting to connect to HAProxy instance at " + haproxy_ip
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.CONNECTION_ERROR)


    def exec_cmd(self, cmd):
        """ Executes a command over the ssh session"""

        try:
            stdin,stdout,stderr = self.session.exec_command(cmd)
            rc = int(stdout.channel.recv_exit_status())
            if rc != 0:
                msg = "Command failed with exit status " + str(rc)
                #msg += stderr.readlines()
                print stderr.readlines()
                LOG.exception(msg)
                raise HAProxyException(HAProxyException.EXEC_ERROR)
        except Exception as e:
            msg = "Runtime error encountered when executing command " + cmd
            LOG.exception(msg)
            raise HAProxyException(HAProxyException.RUNTIME_ERROR)

        return rc


    #def gethaproxycfgfile(, remotefilepath, localfilepath ):
    #    """ Gets a remote haproxycfgfilepath into localfilepath """
        
    def prepare_global_section():
        pass


    def prepare_defaults_section():
        pass

