#########################################
# hello_world collection's filter plugins
#########################################
import ipaddress


# netint_to_list filter
# Prepare a list of network interfaces in a form suitable for vm creation
def netint_to_list(netint_in):
    # print(netint_in)
    netint_out = []
    ii = 0
    for netint_name, netint_data in netint_in.items():
        net_info = {}
        net_info['name'] = netint_name
        if ('ext_bridge' in netint_data.keys()):
            net_info['type'] = 'bridge'
            net_info['network'] = netint_data['ext_bridge']
        else:
            net_info['type'] = 'network'
            net_info['network'] = netint_data['network']
        if (('boot' in netint_data.keys()) and (netint_data['boot'] == 'yes')):
            net_info['boot_order'] = '2'
        if ('address_cidr' in netint_data.keys()):
            net_info['address_cidr'] = netint_data['address_cidr']
            interface = ipaddress.ip_interface(netint_data['address_cidr'])
            net_info['ip_address'] = str(interface.ip)
            network = ipaddress.ip_network(interface.network)
            net_info['network_address'] = str(network.network_address)
            net_info['network_broadcast'] = str(network.broadcast_address)
            net_info['network_netmask'] = str(network.netmask)
            net_info['network_prefix'] = str(network.prefixlen)
        if ('interface_name' in netint_data.keys()):
            net_info['interface_name'] = netint_data['interface_name']
        else:
            net_info['interface_name_id'] = str(ii)
            ii += 1
        if ('gateway' in netint_data.keys()):
            net_info['gateway'] = netint_data['gateway']
        if ('nameservers' in netint_data.keys()):
            net_info['nameservers'] = netint_data['nameservers']
        if ('search_domains' in netint_data.keys()):
            net_info['search_domains'] = netint_data['search_domains']
        netint_out.append(net_info)
    # print(netint_out)
    return netint_out


# volume_to_list filter
# Prepare a list of volumes in a form suitable for vm creation
def volumes_to_list(volumes_in):
    # print(volumes_in)
    volumes_out = []
    ii_char = 'a'
    for vol_name, vol_data in volumes_in.items():
        vol_info = {}
        vol_info['name'] = vol_name
        vol_info['size'] = vol_data['size']
        if ('dev' in vol_data.keys()):
            vol_info['dev'] = vol_data['dev']
        else:
            vol_info['dev'] = 'vd' + ii_char
            ii_char = chr(ord(ii_char) + 1)
        if (vol_name == 'boot'):
            vol_info['boot_order'] = '1'
            volumes_out.insert(0, vol_info)
        else:
            volumes_out.append(vol_info)
    # print(volumes_out)
    return volumes_out


# filter module
class FilterModule(object):
    def filters(self):
        return {
                'netint_to_list': netint_to_list,
                'volumes_to_list': volumes_to_list
        }
