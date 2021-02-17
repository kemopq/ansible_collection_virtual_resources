# kemopq.virtual_resources collection plugins
Filters:
- netint_to_list (network interfaces configuration data is transformed to list of interfaces for easier VM creation) 
- volumes_to_int (volumes configuration data is transformed to list of volumes for easier VM creation)

Modules:
- getmac (returns a list of MAC addresses for a given network for all instances of vm type)
- get_os_version (returns OS version name, major and minor version of given OS image)
