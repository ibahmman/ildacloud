import requests


class HZCloud:
    TOKEN = 'OIYKtUyFKQ9rY4LGq9CHdMRHaXhbRK5XcUnerncHkgZa3cJCmvnYC5S7I0bW8cBS'
    HEADERS = {'content-type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
    DATACENTERS = []
    IMAGES = []

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

    def get_an_image(self):
        # https://docs.hetzner.cloud/#images-get-an-image
        response = requests.get('', headers=self.HEADERS)
        pass

    #
    # ISOs
    def get_all_isos(self):
        # https://docs.hetzner.cloud/#isos-get-all-isos
        pass

    def get_an_iso(self):
        # https://docs.hetzner.cloud/#isos-get-an-iso
        pass

    #
    # Locations
    def get_all_locations(self):
        # https://docs.hetzner.cloud/#locations-get-all-locations
        pass

    def get_a_location(self):
        # https://docs.hetzner.cloud/#locations-get-a-location
        pass
    
    #
    # Ips
    def get_all_ips(self):
        # https://docs.hetzner.cloud/#primary-ips-get-all-primary-ips
        pass

    def get_a_ip(self):
        # https://docs.hetzner.cloud/#primary-ips-get-a-primary-ip
        pass

    def create_a_ip(self):
        # https://docs.hetzner.cloud/#primary-ips-create-a-primary-ip
        pass

    def delete_a_ip(self):
        # https://docs.hetzner.cloud/#primary-ips-delete-a-primary-ip
        pass

    def assign_ip(self):
        # https://docs.hetzner.cloud/#primary-ip-actions-assign-a-primary-ip-to-a-resource
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

