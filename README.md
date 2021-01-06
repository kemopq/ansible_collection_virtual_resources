# kemopq.virtual_resources collection
Collection for creating virtual resources (virtual machines, networks, volumes) on different virtualization platforms (currently only libvirt is supported).  
For virtual machines type and number of instances are defined. VMs are created with names:  
_<vm_type>-node1, <vm_type>-node2, ..._   
Each VM can have several network interfaces and volumes attached. Image can be provided for boot volume (currently only ubuntu18.04 is supported). VM can also boot from network interface (pxe or uefi boot is possible - ovfm package should be installed on main host for uefi boot).

### Installing collection  
Install this collection locally:
```
ansible-galaxy collection install kemopq.virtual_resources -p ./collections
```
_./collections_ folder should be included to _collections_path_ parameter in ansible configuration file (ansible.cfg). See:
https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings-locations
```
[defaults]
collections_path = ./collection
```

### Using collection  
Roles and module can be used on your ansible playbook. It can be  referenced by its fully qualified collection name (FQCN):
```
- name: Your playbook
  hosts: all
  gather_facts: no

  collections:
      - kemopq.virtual_resources

  tasks:
    - name: Include virtual_resources role
      import_role:
        name: libvirt

    - name: Get MAC list of osnode VMs for os_internal network
      kemopq.virtual_resources.getmac:
        vm_type: 'osnode'
        network: 'os_internal'
      register: getmac_result

    - name: Print mac list
      debug:
        msg: "{{ getmac_result.mac_list }}"
```

### Configuration parameters
Template of configuration file is in config folder. It's well commented. The configuration file has three parts:
- storage pool definition
- network definition   
- virtual machines definition

### Running your playbook
When running your playbook a path to configuration file should be provided. Additionaly a parameter _mkaction_ should be set. Possible values are:
- 'deploy': virtual resources are created
- 'destroy': virtual resources are destroyed
- 'vmstart': VMs, which didn't start immediately after creation, are started

```
ansible-playbook  -i localhost, -e mkaction=[deploy/destroy/vmstart] -e "@<your_config_file>.yml" <your_playbook>.yml
```

### Plugins
Filters:
- netint_to_list (network interfaces configuration data is transformed to list of interfaces for easier VM creation) 
- volumes_to_int (volumes configuration data is transformed to list of volumes for easier VM creation)

Modules:
- getmac (returns a list of MAC addresses for a given network for all instances of vm type)

