import requests, random, json, string


class HZCloud:
    TOKEN = 'OIYKtUyFKQ9rY4LGq9CHdMRHaXhbRK5XcUnerncHkgZa3cJCmvnYC5S7I0bW8cBS'
    HEADERS = {'content-type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
    # ----------------------------------------------------------------------------------.
    SERVER = None
    # ----------------------------------------------------------------------------------.
    DATACENTERS = []
    LOCATIONS = []
    IMAGES = []
    SERVER_TYPES = []
    ISOS = []
    PRIMARY_IPS = []
    SERVERS = []

    def __init__(self, token=None, server_id=None):
        if token:
            self.TOKEN = token

        if server_id:
            self.SERVER = self.get_a_server(server_id)

    # Datacenters
    def get_all_datacenters(self):
        # https://docs.hetzner.cloud/#datacenters-get-all-datacenters
        response = requests.get('https://api.hetzner.cloud/v1/datacenters', headers=self.HEADERS).json()
        self.DATACENTERS = response
        return response

    def get_a_datacenter(self, datacenter_id):
        # https://docs.hetzner.cloud/#datacenters-get-a-datacenter
        response = requests.get(f'https://api.hetzner.cloud/v1/datacenters/{datacenter_id}',
                                headers=self.HEADERS).json()
        return response

    #
    # Images
    def get_all_images(self):
        # https://docs.hetzner.cloud/#images-get-all-images
        response = requests.get('https://api.hetzner.cloud/v1/images', headers=self.HEADERS).json()
        self.IMAGES = response
        return response

    def get_an_image(self, image_id):
        # https://docs.hetzner.cloud/#images-get-an-image
        response = requests.get(f'https://api.hetzner.cloud/v1/images/{image_id}', headers=self.HEADERS).json()
        return response

    #
    # Server Types
    def get_all_server_types(self):
        # https://docs.hetzner.cloud/#server-types-get-all-server-types
        response = requests.get('https://api.hetzner.cloud/v1/server_types', headers=self.HEADERS).json()
        self.SERVER_TYPES = response
        return response

    def get_a_server_type(self, server_type):
        # https://docs.hetzner.cloud/#server-types-get-a-server-type
        response = requests.get(f'https://api.hetzner.cloud/v1/server_types/{server_type}', headers=self.HEADERS).json()
        return response

    #
    # ISOs
    def get_all_isos(self):
        # https://docs.hetzner.cloud/#isos-get-all-isos
        response = requests.get('https://api.hetzner.cloud/v1/isos', headers=self.HEADERS).json()
        self.ISOS = response
        return response

    def get_an_iso(self, iso_id):
        # https://docs.hetzner.cloud/#isos-get-an-iso
        response = requests.get(f'https://api.hetzner.cloud/v1/isos/{iso_id}', headers=self.HEADERS).json()
        return response

    #
    # Locations
    def get_all_locations(self):
        # https://docs.hetzner.cloud/#locations-get-all-locations
        response = requests.get('https://api.hetzner.cloud/v1/locations', headers=self.HEADERS).json()
        self.LOCATIONS = response
        return response

    def get_a_location(self, location_id):
        # https://docs.hetzner.cloud/#locations-get-a-location
        response = requests.get(f'https://api.hetzner.cloud/v1/locations/{location_id}', 
                                headers=self.HEADERS).json()
        return response
    
    #
    # Ips
    def get_all_ips(self):
        # https://docs.hetzner.cloud/#primary-ips-get-all-primary-ips
        response = requests.get('https://api.hetzner.cloud/v1/primary_ips', headers=self.HEADERS).json()
        self.PRIMARY_IPS = response
        return response

    def get_a_ip(self, ip_id):
        # https://docs.hetzner.cloud/#primary-ips-get-a-primary-ip
        response = requests.get(f'https://api.hetzner.cloud/v1/primary_ips/{ip_id}', 
                                headers=self.HEADERS).json()
        return response

    def create_a_ip(self, assignee_id, datacenter, name, assignee_type='server', auto_delete=False, _type=4):
        """
        assignee_id: ID of the resource the Primary IP should be assigned to. Omitted if it should not be assigned.
        datacenter: ID or name of Datacenter the Primary IP will be bound to. Needs to be omitted if assignee_id is passed.
        _type: Allowed: ipv4, ipv6.
        """
        # https://docs.hetzner.cloud/#primary-ips-create-a-primary-ip
        if not name:
            name = f'ilda_{[random.choice(string.ascii_lowercase + string.digits) for _ in range(10)]}'

        if _type == 4:
            _type = 'ipv4'
        elif _type == 6:
            _type = 'ipb6'
        else:
            return {'error': 'type must choices between 4 or 6.'}

        data = {
            'assignee_type': assignee_type,
            'auto_delete': auto_delete,
            'name': name,
            'type': _type
        }
        if assignee_id: data['assignee_id'] = assignee_id
        if datacenter and 'assignee_id' not in data: data['datacenter'] = datacenter
            
        response = requests.post('https://api.hetzner.cloud/v1/primary_ips', data=data,
                                 headers=self.HEADERS).json()
        return response

    def delete_a_ip(self, ip_id):
        # https://docs.hetzner.cloud/#primary-ips-delete-a-primary-ip
        response = requests.delete(f'https://api.hetzner.cloud/v1/primary_ips/{ip_id}', headers=self.HEADERS)
        return response

    def assign_ip(self, ip_id, assignee_id, assignee_type='server'):
        """
        ip_id: ID of the Primary IP.
        assignee_id: ID of a resource of type assignee_type.
        assignee_type: Allowed: server, Type of resource assigning the Primary IP to.
        """
        # https://docs.hetzner.cloud/#primary-ip-actions-assign-a-primary-ip-to-a-resource
        data = {
            'assignee_id': assignee_id,
            'assignee_type': assignee_type
        }
        response = requests.post(f'https://api.hetzner.cloud/v1/primary_ips/{ip_id}/actions/assign',
                                 data=data, headers=self.HEADERS).json()
        return response
    
    def unassign_ip(self, _type):
        """
        self.SERVER["public_net"]["ipv4"]["ip"]  ["dns_ptr"]
        self.SERVER["public_net"]["ipv6"]["ip"]  ["dns_ptr"][{"dns_ptr": "", "ip":..}]
        """
        # https://docs.hetzner.cloud/#primary-ip-actions-unassign-a-primary-ip-from-a-resource
        if self.SERVER:
            if _type == 4:
                ip_id = self.SERVER["public_net"]["ipv4"]["id"]
            elif _type == 6:
                ip_id = self.SERVER["public_net"]["ipv6"]["id"]
            else:
                return {'error': 'type must choices between 4 or 6.'}

            response = requests.post(f'https://api.hetzner.cloud/v1/primary_ips/{ip_id}/actions/unassign',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    #
    # Servers
    def get_all_servers(self):
        # https://docs.hetzner.cloud/#servers-get-all-servers
        response = requests.get('https://api.hetzner.cloud/v1/servers',
                                headers=self.HEADERS).json()
        self.SERVERS = response
        return response

    def get_a_server(self, server_id):
        # https://docs.hetzner.cloud/#servers-get-a-server
        response = requests.get(f'https://api.hetzner.cloud/v1/servers/{server_id}',
                                headers=self.HEADERS).json()
        self.SERVER = response
        return response
    
    def create_a_server(self, **kwargs):
        """
        datacenter, image, location, name, server_type,
        datacenter: ID or name of Datacenter to create Server in (must not be used together with location).
        image: ID or name of the Image the Server is created from.
        location: ID or name of Location to create Server in (must not be used together with datacenter).
        name: Name of the Server to create (must be unique per Project and a valid hostname as per RFC 1123).
        server_type: ID or name of the Server type this Server should be created with.

        Response:
        action
        next_action
        root_password
        server
        """
        # https://docs.hetzner.cloud/#servers-create-a-server
        # data = {
        #     'image': image,
        #     'name': name,
        #     'server_type': server_type
        # }
        # if datacenter: data['datacenter'] = datacenter
        # if location: data['location'] = location
        response = requests.post('https://api.hetzner.cloud/v1/servers', data=json.dumps(kwargs),
                                 headers=self.HEADERS).json()
        return response

    def delete_a_server(self):
        # https://docs.hetzner.cloud/#servers-delete-a-server
        if self.SERVER:
            response = requests.delete(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}',
                                       headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    #
    # Server Actions
    def change_type_server(self, server_type, upgrade_disk=True):
        """
        server_type: ID or name of Server type the Server should migrate to.
        upgrade_disk: If false, do not upgrade the disk (this allows downgrading the Server type later).
        """
        # https://docs.hetzner.cloud/#server-actions-change-the-type-of-a-server
        if self.SERVER:
            data = {
                'server_type': server_type,
                'upgrade_disk': upgrade_disk
            }
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/change_type',
                                     data=json.dumps(data), headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def shutdown_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-shutdown-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/shutdown',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def power_off_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-power-off-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/poweroff',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def power_on_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-power-on-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/poweron',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}
    
    def soft_reboot_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-soft-reboot-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/reboot',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def hard_restart_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-reset-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/reset',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def rebuild_server(self, image):
        """
        id: ID of the Server.
        image: ID or name of Image to rebuilt from.
        """
        # https://docs.hetzner.cloud/#server-actions-rebuild-a-server-from-an-image
        if self.SERVER:
            data = {
                'image': image,
            }
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/poweroff',
                                     data=data, headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def reset_passwd_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-reset-root-password-of-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/poweroff',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def request_console_server(self):
        """
        id: ID of the Server.
        """
        # https://docs.hetzner.cloud/#server-actions-request-console-for-a-server
        if self.SERVER:
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/poweroff',
                                     headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}

    def change_ptr(self, _type=4, dns_ptr=''):
        """
        dns_ptr: Hostname to set as a reverse DNS PTR entry, reset to original value if null.
        ip: Primary IP address for which the reverse DNS entry should be set.
        """
        # https://docs.hetzner.cloud/#server-actions-change-reverse-dns-entry-for-this-server

        if self.SERVER:
            if _type == 4:
                ip = self.SERVER["public_net"]["ipv4"]["ip"]
            # elif _type == 6:
            #     ip = self.SERVER["public_net"]["ipv6"]["id"]
            else:
                return {'error': 'type must choices between 4.'}

            data = {
                'dns_ptr': dns_ptr,
                'ip': ip
            }
            response = requests.post(f'https://api.hetzner.cloud/v1/servers/{self.SERVER["server"]["id"]}/actions/change_dns_ptr',
                                     data=data, headers=self.HEADERS).json()
            return response
        return {'error': 'use get_a_server for select server.'}
