#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
import libvirt
import libxml2


DOCUMENTATION = r'''
---
module: getmac

short_description: Returns list of MAC addresses of VMs

version_added: "0.0.1"

description: Module reads MAC addr of all instances of VM type for given network

options:
    vm_type:
        description: Type of VM
        required: true
        type: str
    vm_suffix:
        description: Suffix of a vm name
        required: false
        type: str
        default: "-node"
    network:
        description: network name
        required: true
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
#extends_documentation_fragment:
#    - kemopq.hello_world.my_doc_fragment_name

author:
    - Klemen Pogacnik (@kemopq)
'''

EXAMPLES = r'''
# Pass in a message
- name: Insert user and date to file
  kemopq.virtual_resources.getmac:
    vm_type: "osnode"
    network: "os-internal"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
mac_list:
    description: List of MACs
    type: list
    returned: always
    sample: '[{name: "osnode-node1", network: "os-internal", mac: "52:54:00:e1:fc:9e"}]'
'''


# return MAC VMs for given network
def get_mac_of_vm(xmlCtx, networkName):
    interfaces = xmlCtx.xpathEval("/domain/devices/interface")
    for interface in interfaces:
        xmlCtx.setContextNode(interface)
        # read network name
        xmlSection = xmlCtx.xpathEval("source/@network")
        if ((xmlSection is not None) and (len(xmlSection) > 0)):
            xmlNetwork = xmlSection[0].content
            # read MAC
            if xmlNetwork == networkName:
                xmlSection = xmlCtx.xpathEval("mac/@address")
                if ((xmlSection is not None) and (len(xmlSection) > 0)):
                    return xmlSection[0].content
    # not found
    return "Unknown"


# return list of VMs of vmType
def get_vm_list(libvirtConn, vmType, vmSuffix):
    vmList = []
    # domains (VMs), which are not running
    domainNamesNotRunning = libvirtConn.listDefinedDomains()
    if domainNamesNotRunning is None:
        raise RuntimeError('Failed to get a list of domain names')
    for domainName in domainNamesNotRunning:
        if (domainName.startswith(vmType + vmSuffix)):
            vmList.append(domainName)

    # running domains (VMs)
    domainIDs = libvirtConn.listDomainsID()
    if domainIDs is None:
        raise RuntimeError('Failed to get a list of domain IDs')

    for domainID in domainIDs:
        domain = libvirtConn.lookupByID(domainID)
        domainName = domain.name()
        if (domainName.startswith(vmType + vmSuffix)):
            vmList.append(domainName)

    return vmList


# return list of VMs and MACs for given network
def get_mac_list(vmType, vmSuffix, network):
    macList = []
    # Connect to libvirt
    libvirtConn = libvirt.openReadOnly('qemu:///system')
    if libvirtConn is None:
        raise RuntimeError('Failed to open connection to the hypervisor')

    try:
        vmList = get_vm_list(libvirtConn, vmType, vmSuffix)
    except RuntimeError as err:
        raise RuntimeError(str(err))

    for domainName in vmList:
        # Open domain object
        domain = libvirtConn.lookupByName(domainName)
        if domain is not None:
            # Read domain's XML
            xmlDesc = domain.XMLDesc(0)
            xmlDoc = libxml2.parseDoc(xmlDesc)
            xmlCtx = xmlDoc.xpathNewContext()
            domainData = {"name": domainName, "network": network, "mac": get_mac_of_vm(xmlCtx, network)}
            macList.append(domainData)

    return macList


# module function
def run_module():
    # define available arguments/parameters a user can pass to the module and result of the module
    module_args = dict(
        vm_type=dict(type='str', required=True),
        vm_suffix=dict(type='str', required=False, default='-node'),
        network=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        mac_list=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # module's body
    try:
        result['mac_list'] = get_mac_list(module.params['vm_type'], module.params['vm_suffix'], module.params['network'])
    except RuntimeError as err:
        module.fail_json(msg=str(err), **result)

    # return result
    module.exit_json(**result)


# main
def main():
    run_module()


if __name__ == '__main__':
    main()
