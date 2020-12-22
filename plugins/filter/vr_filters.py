#########################################
# hello_world collection's filter plugins
#########################################

# networks_to_list filter
# Prepare a list of networks in a form suitable for vm creation
def networks_to_list(networks_in):
    # print(networks_in)
    networks_out = []
    ii = 3
    for net_name, net_data in networks_in.items():
        net_info = {}
        net_info['name'] = net_name
        net_info['type'] = net_data['type']
        if (net_data['type'] == 'bridge'):
            net_info['net'] = net_data['ext_bridge']
        else:
            net_info['net'] = net_name
        if ('cidr' in net_data.keys()):
            net_info['address'] = net_data['cidr']
        if ('interface_name' in net_data.keys()):
            net_info['interface_name'] = net_data['interface_name']
        else:
            net_info['interface_name'] = 'ens' + str(ii)
            ii += 1
        if (('boot' in net_data.keys()) and (net_data['boot'] == 'yes')):
            net_info['boot_order'] = '2'
        if ('gateway' in net_data.keys()):
            net_info['gateway'] = net_data['gateway']
        if ('domain_name' in net_data.keys()):
            net_info['domain_name'] = net_data['domain_name']
        if ('nameservers' in net_data.keys()):
            net_info['nameservers'] = net_data['nameservers']
        networks_out.append(net_info)
    # print(networks_out)
    return networks_out


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
        volumes_out.append(vol_info)
    # print(volumes_out)
    return volumes_out


# filter module
class FilterModule(object):
    def filters(self):
        return {
                'networks_to_list': networks_to_list,
                'volumes_to_list': volumes_to_list
        }
