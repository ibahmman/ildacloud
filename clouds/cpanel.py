import requests, random, json, string


class HZCloud:
    TOKEN = 'OIYKtUyFKQ9rY4LGq9CHdMRHaXhbRK5XcUnerncHkgZa3cJCmvnYC5S7I0bW8cBS'
    HEADERS = {'content-type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
    
    DATACENTERS = []
    LOCATIONS = []
    IMAGES = []
    ISOS = []
    PRIMARY_IPS = []

    def __init__(self, token):
        if token:
            self.TOKEN = token

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

    def create_a_ip(self, assignee_id, datacenter, name, assignee_type='server', auto_delete=False, type=4):
        """
        assignee_id: ID of the resource the Primary IP should be assigned to. Omitted if it should not be assigned.
        datacenter: ID or name of Datacenter the Primary IP will be bound to. Needs to be omitted if assignee_id is passed.
        type: Allowed: ipv4, ipv6.
        """
        # https://docs.hetzner.cloud/#primary-ips-create-a-primary-ip
        if not name:
            name = f'ilda_{[random.choice(string.ascii_lowercase + string.digits) for _ in range(10)]}'

        if type == 4:
            type = 'ipv4'
        elif type == 6:
            type = 'ipb6'
        else: return {'error': 'type must seleect between 4 or 6.'}

        data = {
            'assignee_type': assignee_type,
            'auto_delete': auto_delete,
            'name': name,
            'type': type
        }
        if assignee_id: data['assignee_id'] = assignee_id
        if datacenter and 'assignee_id' not in data: data['datacenter'] = datacenter
            
        response = requests.post('https://api.hetzner.cloud/v1/primary_ips', data=json.dump(data), 
                                 headers=self.HEADERS).json()
        return response

    def delete_a_ip(self, ip_id):
        # https://docs.hetzner.cloud/#primary-ips-delete-a-primary-ip
        response = requests.delete(f'https://api.hetzner.cloud/v1/primary_ips/{ip_id}', headers=self.HEADERS)
        return response

    def assign_ip(self, ip_id):
        """
        ip_id: ID of the Primary IP.
        assignee_id: ID of a resource of type assignee_type.
        assignee_type: Allowed: server, Type of resource assigning the Primary IP to.
        """
        # https://docs.hetzner.cloud/#primary-ip-actions-assign-a-primary-ip-to-a-resource
        response = requests.post(f'https://api.hetzner.cloud/v1/primary_ips/{ip_id}/actions/assign')
        data = {
            
        }
        pass
    
    def unassign_ip(self):
        # https://docs.hetzner.cloud/#primary-ip-actions-unassign-a-primary-ip-from-a-resource
        pass
    
    def change_ptr(self):
        # https://docs.hetzner.cloud/#server-actions-change-reverse-dns-entry-for-this-server
        pass

    #
    # Servers
    def get_all_servers(self):
        # https://docs.hetzner.cloud/#servers-get-all-servers
        pass

    def get_a_server(self):
        # https://docs.hetzner.cloud/#servers-get-a-server
        pass
    
    def create_a_server(self):
        # https://docs.hetzner.cloud/#servers-create-a-server
        pass

    def delete_a_server(self):
        # https://docs.hetzner.cloud/#servers-delete-a-server
        pass

    #
    # Server Actions
    def shutdown_server(self):
        # https://docs.hetzner.cloud/#server-actions-shutdown-a-server
        pass

    def power_off_server(self):
        # https://docs.hetzner.cloud/#server-actions-power-off-a-server
        pass
    
    def power_on_server(self):
        # https://docs.hetzner.cloud/#server-actions-power-on-a-server
        pass
    
    def soft_reboot_server(self):
        # https://docs.hetzner.cloud/#server-actions-soft-reboot-a-server
        pass

    def hard_restart_server(self):
        # https://docs.hetzner.cloud/#server-actions-reset-a-server
        pass

    def rebuild_server(self):
        # https://docs.hetzner.cloud/#server-actions-rebuild-a-server-from-an-image
        pass

    def reset_passwd_server(self):
        # https://docs.hetzner.cloud/#server-actions-reset-root-password-of-a-server
        pass

    def request_console_server(self):
        # https://docs.hetzner.cloud/#server-actions-request-console-for-a-server
        pass

