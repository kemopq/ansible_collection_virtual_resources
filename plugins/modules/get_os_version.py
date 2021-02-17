#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
import libxml2
import os


DOCUMENTATION = r'''
---
module: get_os_version

short_description: Returns OS version name, major and minor version

version_added: "0.0.1"

description: Module checks OS version name, major and minor version of given OS image

options:
    image_path:
        description: Path to OS image
        required: false (one of the parameter image_path or vm_name is required)
        type: str
    vm_name:
        description: Virtual machine name
        required: false (one of the parameter image_path or vm_name is required)
        type: str


# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
#extends_documentation_fragment:
#    - kemopq.virt_resources.my_doc_fragment_name

author:
    - Klemen Pogacnik (@kemopq)
'''

EXAMPLES = r'''
# Pass in a message
- name: Get OS type and version
  kemopq.virtual_resources.get_os_version:
    image_path: "/home/ubuntu/downloads/ubuntu-18.04-server-cloudimg-1.0.0-amd64.qcow2"

- name: Get OS type and version
  kemopq.virtual_resources.get_os_version:
    vm_name: "faikolla-node1"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
os_version:
    description: Distro name (ubuntu, centos, debian), mijor and minor version
    type: dict
    returned: always
    sample: '[{distro: "ubuntu", major_version: "18", minor_version: "4"}]'
'''


# return OS version major and minor version
def get_os_version(image_path, vm_name):
    osVersion = {'distro': 'unknown', 'major_version': 0, 'minor_version': 0}
    if (image_path != 'unknown'):
        command = 'sudo virt-inspector --no-applications --no-icon -a ' + image_path + ' 2>/dev/null'
    elif (vm_name != 'unknown'):
        command = 'sudo virt-inspector --no-applications --no-icon -d ' + vm_name + ' 2>/dev/null'
    else:
        raise RuntimeError('No image path or vm name provided')
    stream = os.popen(command)
    xmlString = stream.read()
    try:
        xmlDoc = libxml2.parseDoc(xmlString)
    except libxml2.parserError as err:
        raise RuntimeError('OS image or vm does not exist - ' + str(err))
    xmlCtx = xmlDoc.xpathNewContext()
    xmlSection = xmlCtx.xpathEval("/operatingsystems/operatingsystem/distro")
    if ((xmlSection is None) or (len(xmlSection) <= 0)):
        raise RuntimeError('Failed to get OS distro')
    osVersion['distro'] = xmlSection[0].content
    xmlSection = xmlCtx.xpathEval("/operatingsystems/operatingsystem/major_version")
    if ((xmlSection is None) or (len(xmlSection) <= 0)):
        raise RuntimeError('Failed to get OS major version')
    osVersion['major_version'] = xmlSection[0].content
    xmlSection = xmlCtx.xpathEval("/operatingsystems/operatingsystem/minor_version")
    if ((xmlSection is None) or (len(xmlSection) <= 0)):
        raise RuntimeError('Failed to get OS minor version')
    osVersion['minor_version'] = xmlSection[0].content

    return osVersion


# module function
def run_module():
    # define available arguments/parameters a user can pass to the module and result of the module
    module_args = dict(
        image_path=dict(type='str', required=False, default='unknown'),
        vm_name=dict(type='str', required=False, default='unknown')
    )

    result = dict(
        changed=False,
        os_version={'distro': 'unknown', 'major_version': 0, 'minor_version': 0}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # module's body
    try:
        result['os_version'] = get_os_version(module.params['image_path'], module.params['vm_name'])
    except RuntimeError as err:
        module.fail_json(msg=str(err), **result)

    # return result
    module.exit_json(**result)


# main
def main():
    run_module()


if __name__ == '__main__':
    main()
