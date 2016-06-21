# Copyright 2016 Telcoware
# network control management classes

from novaclient import client
from api.config import ReadConfig
import ast


class InstanceTester:

    def __init__(self, config_file):
        # Get config
        self.auth_conf = ReadConfig(config_file).get_nova_auth_conf()
        self.instance_conf = ReadConfig.get_instance_config()
        self.network_conf = ReadConfig.get_network_config()
        # Get Token and Neutron Object
        self.nova = client.Client(**self.auth_conf)

    def get_instance_list_all(self):
        instance_rst = self.nova.servers.list()
        print 'Instance All --->', instance_rst

    def get_instance_list(self, instance_opt):
        config_value = self.find_instance(instance_opt)
        if config_value:
            instance_rst = self.nova.servers.list(search_opts={'name': config_value['name']})
            if not instance_rst:
                print 'Not exist openstack --->', instance_opt, config_value
                return None
        else:
            print 'Not exist', instance_opt, 'in config --->'
            return None

        print 'Instance list --->', instance_opt, instance_rst
        return instance_rst

    def create_instance(self, instance_opt):
        config_value = self.find_instance(instance_opt)
        image = self.nova.images.find(name=config_value['image'])
        flavor = self.nova.flavors.find(name=config_value['flavor'])

        if not config_value:
            print 'Not exist in config file --->', instance_opt
            return config_value

        # Get openstack network name from network config
        net_name_list = []
        for a in config_value['networks']:
            net_conf_body = ast.literal_eval(dict(self.network_conf)[a])
            net_name_list.append(net_conf_body['network']['name'])
            # net_name_list.append(ast.literal_eval(dict(self.network_conf)[a])['network']['name'])

        # Get network uuid from openstack neutron and make nics list
        nics_list = []
        for a in net_name_list:
            nics_list.append({'net-id':  self.nova.networks.find(label=a).id})

        # TODO
        # make sg_list for security_groups name
        sg_list = ['test1', 'default']
        # sg_list = []

        # create instance
        instance_rst = self.nova.servers.create(name=config_value['name'],
                                                image=image,
                                                flavor=flavor,
                                                availability_zone=config_value['zone'],
                                                nics=nics_list,
                                                security_groups=sg_list)
        print 'Create Succ --->', instance_rst
        return instance_rst


    # TODO
    # - delete method
    def delete_instance(self):
        pass

    def find_instance(self, instance_opt):
        instance_conf = dict(self.instance_conf)[instance_opt]
        if instance_conf:
            # TODO
            # when config file is wrong, exception ...
            config_value = ast.literal_eval(instance_conf)
            return config_value
        return None


