#
# kimjt Network temporarily test tool
#
from api.sonatest import SonaTest
from ConfigParser import ConfigParser
from api.reporter2 import Reporter
import os
import commands

WHITE = '\033[1;97m'
BLUE = '\033[1;94m'
YELLOW = '\033[1;93m'
GREEN = '\033[1;92m'
RED = '\033[1;91m'
BLACK = '\033[1;90m'
BG_WHITE = '\033[0;97m'
BG_BLUEW = '\033[0;37;44m'
BG_SKYW = '\033[0;37;46m'
BG_PINKW = '\033[0;37;45m'
BG_YELLOWW = '\033[0;30;43m'
BG_GREENW = '\033[0;37;42m'
BG_RED = '\033[0;91m'
BG_BLACK = '\033[0;90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

CONFIG_FILE = '../config/config.ini'

test = SonaTest(CONFIG_FILE)

MAIN_MENU = 1
SCEN_CRT_MENU = 2
SCEN_DEL_MENU = 3
ETC_MENU = 4

navi_menu = MAIN_MENU
exit_flag=True
save_scenario_dic = {}
index_save_scenario_dic = {}


SCENARIO_PATH = './'

def title_print(menu='None'):
    Reporter.PRINTB("|--------------------------|")
    print BLUE + '|' + BG_BLUEW + \
                     '       SONA-TOOL          ' + BLUE + '|'+ENDC
    Reporter.PRINTB("|--------------------------|")
    if 'None' not in menu:
        print BLUE + '|' + BG_PINKW + \
                      menu.ljust(26) + BLUE + '|'+ENDC
        Reporter.PRINTB("|--------------------------|")

def main_menu():
    os.system('clear')
    title_print()
    Reporter.PRINTB("| 1. create scenario start |")
    Reporter.PRINTB("| 2. delete scenario start |")
    Reporter.PRINTB("| 3. create scenario       |")
    Reporter.PRINTB("| 4. delete scenario       |")
    Reporter.PRINTB("| 5. etc test              |")
    Reporter.PRINTB("| 6. exit                  |")
    Reporter.PRINTB("|--------------------------|")

def state_test_menu():
    os.system('clear')
    title_print(' # etc test')
    Reporter.PRINTB("| 1. onos state            |")
    Reporter.PRINTB("| 2. traffic test          |")
    Reporter.PRINTB("| 3. return to main menu   |")
    Reporter.PRINTB("|--------------------------|")

def scen_delete_menu():
    os.system('clear')
    title_print(' # delete scenario')
    Reporter.PRINTB("| 1. delete_netowk         |")
    Reporter.PRINTB("| 2. delete_subnet         |")
    Reporter.PRINTB("| 3. delete_router         |")
    Reporter.PRINTB("| 4. delete_router_interface|")
    Reporter.PRINTB("| 5. delete_security_group |")
    Reporter.PRINTB("| 6. delete_instance       |")
    Reporter.PRINTB("| 7. delete_floatingip_all |")
    Reporter.PRINTB("| 8. test delete scenario  |")
    Reporter.PRINTB("| 9. save delete scenario  |")
    Reporter.PRINTB("| 0. return to main menu   |")
    Reporter.PRINTB("|--------------------------|")

def scen_create_menu():
    os.system('clear')
    title_print(' # create scenario')
    Reporter.PRINTB("| 1. create_netowk         |")
    Reporter.PRINTB("| 2. create_subnet         |")
    Reporter.PRINTB("| 3. create_router         |")
    Reporter.PRINTB("| 4. add_router_interface  |")
    Reporter.PRINTB("| 5. security_group        |")
    Reporter.PRINTB("| 6. create_instance       |")
    Reporter.PRINTB("| 7. floatingip_associate  |")
    Reporter.PRINTB("| 8. test create scenario  |")
    Reporter.PRINTB("| 9. save create scenario  |")
    Reporter.PRINTB("| 0. return to main menu   |")
    Reporter.PRINTB("|--------------------------|")

def report_log_viewer():
    while 1:
        sel_log = raw_input("\n Do you want to view the log? (y/n) ")
        if 'y' in sel_log:
            print 'report file : ', Reporter.report_file_name
            (exitstatus, outtext) = commands.getstatusoutput('cat '+ Reporter.report_file_name)
            print outtext
            print '\n================================== END LOG ==================================\n\n'
            raw_input(RED + "\n press any key to ENTER " + ENDC)
            break
        elif 'n' in sel_log:
            break
        else:
            Reporter.PRINTR('invalid value, retry! ')
            continue




def scenario_file_search(type):
    file_list=[]
    filenames = os.listdir(SCENARIO_PATH)
    for filename in filenames:
        full_filename = os.path.join(SCENARIO_PATH, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.ini':
            if type + '_scenario' in full_filename:
                file_name = full_filename.split('/')[-1]
                file_list.append((file_name.split('.ini'))[0])

    return file_list

def get_config_key_list(section):
    config = ConfigParser()
    config.read(CONFIG_FILE)
    item = config._sections[section]
    key_list = item.keys()
    del key_list[0]
    return key_list

def create_scenario_start():
    os.system('clear')
    #### scen file ####
    scen_list = scenario_file_search('create')
    title_print(' # create scenario start')
    for i in range(len(scen_list)):
        Reporter.PRINTB('| %d. %-22s|', i+1, scen_list[i])
    Reporter.PRINTB('| %d. return to main menu   |', len(scen_list)+1)
    Reporter.PRINTB("|--------------------------|")
    sel_scen = input('select scenario :')
    if 4 is sel_scen:
        return
    create_start_scenario(scen_list[sel_scen-1])

def delete_scenario_start():
    os.system('clear')
    #### scen file ####
    scen_list = scenario_file_search('delete')
    title_print(' # delete scenario start')
    for i in range(len(scen_list)):
        Reporter.PRINTB('| %d. %-22s|', i+1, scen_list[i])
    Reporter.PRINTB('| %d. return to main menu   |', len(scen_list)+1)
    Reporter.PRINTB("|--------------------------|")
    sel_scen = input('select scenario :')
    if 4 is sel_scen:
        return
    ##### start secnario ####
    delete_start_scenario(scen_list[sel_scen-1])

def display_scenario(scen_name):
    os.system('clear')
    scen_file = SCENARIO_PATH+scen_name+'.ini'
    scen_ini = ConfigParser()
    scen_ini.read(scen_file)

    print scen_ini._sections['network']

    net_item = (scen_ini._sections['network']).values(); del net_item[0]
    sub_item = (scen_ini._sections['subnet']).values(); del sub_item[0]
    print sub_item
    router_item = (scen_ini._sections['router']).values(); del router_item[0]
    router_if_item = (scen_ini._sections['router-interface']).values(); del router_if_item[0]
    sg_item = (scen_ini._sections['security_group']).values(); del sg_item[0]
    inst_item = (scen_ini._sections['instance']).values(); del inst_item[0]
    size_list=[]
    size_list.append(len(' | '.join(net_item)))
    size_list.append(len(' | '.join(sub_item)))
    size_list.append(len(' | '.join(router_item)))
    size_list.append(len(' | '.join(router_if_item)))
    size_list.append(len(' | '.join(sg_item)))
    size_list.append(len(' | '.join(inst_item)))
    max_size = max(size_list)

    if 'create' in scen_name:
        fip_as_item = (scen_ini._sections['floatingip_associate']).values(); del fip_as_item[0]

    title_size = (max_size/2)-2

    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))
    print YELLOW + '|' + BOLD + BG_YELLOWW + ' scenario information : ' + scen_name + \
          ' '.ljust(max_size-len(scen_name)+1) + YELLOW + '|' + ENDC
    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))
    print YELLOW + '|' + BOLD + BG_YELLOWW + '          Type         ' + \
          YELLOW + '|' + BOLD + BG_YELLOWW + ' '.ljust(title_size+1) + \
          'Value'.ljust(max_size-title_size) + YELLOW + '|' + ENDC

    Reporter.PRINTY('|=======================|%s|', ('='*(max_size+1)).ljust(max_size+1))
    Reporter.PRINTY('| Network               | %s|', ' | '.join(net_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Subnet                | %s|', ' | '.join(sub_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Router                | %s|', ' | '.join(router_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Router_Interface      | %s|', ' | '.join(router_if_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Security_Group        | %s|', ' | '.join(sg_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Instance              | %s|', ' | '.join(inst_item).ljust(max_size))
    if 'create' in scen_name:
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
        Reporter.PRINTY('| Floating_ip_associate | %s|', ' | '.join(fip_as_item).ljust(max_size))
    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))

    while 1:
        sel_scen = raw_input(" Do you want to start the scenario? (y/n) ")
        if 'y' in sel_scen:
            return True
        elif 'n' in sel_scen:
            return False
        else:
            print 'invalid value, retry ... '
            continue

def create_start_scenario(scen_name):
    Reporter.initial_test_count()
    ret = display_scenario(scen_name)
    if False is ret:
        return False

    global test
    scen_file = SCENARIO_PATH+scen_name+'.ini'
    scen_ini = ConfigParser()
    scen_ini.read(scen_file)

    # Network
    item = scen_ini._sections['network']
    for i in range(len(item)):
        if i is not 0:
            test.network.create_network(item.values()[i])

    # SubNet
    item = scen_ini._sections['subnet']
    for i in range(len(item)):
        if i is not 0:
            test.network.create_subnet((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])

    # Router
    item = scen_ini._sections['router']
    for i in range(len(item)):
        if i is not 0:
            test.network.create_router((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])

    item = scen_ini._sections['router-interface']
    for i in range(len(item)):
        if i is not 0:
            test.network.add_router_interface((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])

    # Security Group
    item = scen_ini._sections['security_group']
    arg2 = []
    for i in range(len(item)):
        if i is not 0:
            for x in range(len((item.values()[i]).split(', '))):
                if x is 0:
                    arg1 = (item.values()[i]).split(', ')[x]
                else:
                    arg2.append((item.values()[i]).split(', ')[x])

            test.network.create_securitygroup(arg1, ', '.join(arg2))

    # Instance
    item = scen_ini._sections['instance']
    for i in range(len(item)):
        if i is not 0:
            if 2 is len((item.values()[i]).split(', ')):
                test.instance.create_instance((item.values()[i]).split(', ')[0],
                                             (item.values()[i]).split(', ')[1], '')
            elif 3 is len((item.values()[i]).split(', ')):
                test.instance.create_instance((item.values()[i]).split(', ')[0],
                                             (item.values()[i]).split(', ')[1],
                                             (item.values()[i]).split(', ')[2])
            else:
                print 'invalid argument'

    # # Floating IP
    item = scen_ini._sections['floatingip_associate']
    for i in range(len(item)):
        if i is not 0:
            test.instance.floatingip_associate((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])
            test.floating_ip_check((item.values()[i]).split(', ')[0])

    test.reporter.test_summary()

    ## View Log???? ##
    report_log_viewer()

def delete_start_scenario(scen_name):
    Reporter.initial_test_count()
    ret = display_scenario(scen_name)
    if False is ret:
        return False

    # global test
    scen_file = SCENARIO_PATH+scen_name+'.ini'
    scen_ini = ConfigParser()
    scen_ini.read(scen_file)

    # Instance
    item = scen_ini._sections['instance']
    for i in range(len(item)):
        if i is not 0:
            test.instance.delete_instance((item.values()[i]).split(', ')[0])

    # Floating IP
    test.instance.delete_floatingip_all()

    # Security Group
    item = scen_ini._sections['security_group']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_seuritygroup((item.values()[i]).split(', ')[0])

    # Router interface
    item = scen_ini._sections['router-interface']
    for i in range(len(item)):
        if i is not 0:
            test.network.remove_router_interface((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])
    # Router
    item = scen_ini._sections['router']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_router((item.values()[i]).split(', ')[0])

    # SubNet
    item = scen_ini._sections['subnet']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_subnet((item.values()[i]).split(', ')[0])
    # Network
    item = scen_ini._sections['network']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_network(item.values()[i])

    test.reporter.test_summary()
    report_log_viewer()


# scenario config

# scenario save memory
def save_scenario(section, value):
    # global save_scenario_dic
    # verify check
    save_value_list = save_scenario_dic.get(section)
    if None is not save_value_list:
        if len(value) > 1:
            for x in value:
                save_value_list.append(''.join(x))
        else:
            save_value_list.append(''.join(value))

        save_scenario_dic[section] = save_value_list

    else:
        save_scenario_dic[section] = value

    display_save_scenario(save_scenario_dic)

def display_save_scenario(dic, test_num=False):
    size_list=[]
    test_index = 0
    print dic
    # Network
    net_item = dic.get('network')
    if None is not net_item:
        size_list.append(len(' | '.join(net_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['network'] = test_index

    # Subnet
    sub_item = dic.get('subnet')
    if None is not sub_item:
        size_list.append(len(' | '.join(sub_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['subnet'] = test_index

    # Router
    router_item = dic.get('router')
    if None is not router_item:
        size_list.append(len(' | '.join(router_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['router'] = test_index

    # Router Interface
    router_if_item = dic.get('router-interface')
    if None is not router_if_item:
        size_list.append(len(' | '.join(router_if_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['router-interface'] = test_index

    # Security_group
    sg_item = dic.get('security_group')
    if None is not sg_item:
        size_list.append(len(' | '.join(sg_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['security_group'] = test_index

    # Instance
    inst_item = dic.get('instance')
    if None is not inst_item:
        size_list.append(len(' | '.join(inst_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['instance'] = test_index

    # Floating Ip associate
    fip_as_item = dic.get('floatingip_associate')
    if None is not fip_as_item:
        size_list.append(len(' | '.join(fip_as_item)))
        if True is test_num:
            test_index += 1
            index_save_scenario_dic['floatingip_associate'] = test_index


    max_size = max(size_list)
    title_size = ((max_size+25-27)/2)

    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))
    if True is test_num:
        title_str = '!test scenario information!'
    else:
        title_str = 'create scenario information'
    line_size = max_size+26
    tt_size = title_size*2 + len(title_str)
    sub_size = line_size - tt_size
    if sub_size > 0:
        print YELLOW + '|' + BOLD + BG_YELLOWW + ' '.ljust(title_size) + title_str + \
              ' '.ljust(title_size+(sub_size)/2) + YELLOW + '|' + ENDC
    else:
        print YELLOW + '|' + BOLD + BG_YELLOWW + ' '.ljust(title_size) + title_str + \
              ' '.ljust(title_size) + YELLOW + '|' + ENDC
    Reporter.PRINTY('|=======================|%s|', ('='*(max_size+1)).ljust(max_size+1))

    if None is not net_item:
        if True is test_num:
            Reporter.PRINTY('| %d. Network            | %s|', index_save_scenario_dic.get('network'), ' | '.join(net_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Network               | %s|', ' | '.join(net_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if None is not sub_item:
        if True is test_num:
            Reporter.PRINTY('| %d. Subnet             | %s|', index_save_scenario_dic.get('subnet'), ' | '.join(sub_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Subnet                | %s|', ' | '.join(sub_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if None is not router_item:
        if True is test_num:
            Reporter.PRINTY('| %d. Router             | %s|', index_save_scenario_dic.get('router'), ' | '.join(router_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Router                | %s|', ' | '.join(router_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if None is not router_if_item:
        if True is test_num:
            Reporter.PRINTY('| %d. Router_Interface   | %s|', index_save_scenario_dic.get('router-interface'), ' | '.join(router_if_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Router_Interface      | %s|', ' | '.join(router_if_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if None is not sg_item:
        if True is test_num:
            Reporter.PRINTY('| %d. Security_Group     | %s|', index_save_scenario_dic.get('security_group'), ' | '.join(sg_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Security_Group        | %s|', ' | '.join(sg_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if None is not inst_item:
        if True is test_num:
            Reporter.PRINTY('| %d. Instance           | %s|', index_save_scenario_dic.get('instance'), ' | '.join(inst_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Instance              | %s|', ' | '.join(inst_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if None is not fip_as_item:
        if True is test_num:
            Reporter.PRINTY('| %d. F_ip_associate     | %s|', index_save_scenario_dic.get('floatingip_associate'), ' | '.join(fip_as_item).ljust(max_size))
        else:
            Reporter.PRINTY('| Floating_ip_associate | %s|', ' | '.join(fip_as_item).ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))

    if True is test_num:
        Reporter.PRINTY('| 0. cancel             | %s|', ' | '.join('').ljust(max_size))
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))


# scenario save config
def save_config_scenario():
    scen_name = raw_input(RED +'Enter a name for the file. : '+ENDC)
    dic = save_scenario_dic
    scen_file = SCENARIO_PATH + 'create_' + scen_name + '.ini'
    scen_ini = ConfigParser()

    # Network
    net_item = dic.get('network')
    if None is not net_item:
        scen_ini.add_section('network')
        for i in range(len(net_item)):
            set_str = 'set' + str(i+1)
            scen_ini.set('network', set_str, net_item[i])

    # Subnet
    sub_item = dic.get('subnet')
    if None is not sub_item:
        scen_ini.add_section('subnet')
        for i in range(len(sub_item)):
            set_str = 'set' + str(i+1)
            scen_ini.set('subnet', set_str, sub_item[i])

    # Router
    router_item = dic.get('router')
    if None is not router_item:
        scen_ini.add_section('router')
        for i in range(len(router_item)):
            set_str = 'set' + str(i+1)
            scen_ini.set('router', set_str, router_item[i])

    # Router Interface
    router_if_item = dic.get('router-interface')
    if None is not router_if_item:
        scen_ini.add_section('router-interface')
        for i in range(len(router_if_item)):
            set_str = 'set' + str(i+1)
            scen_ini.set('router-interface', set_str, router_if_item[i])

    # Security_group
    sg_item = dic.get('security_group')
    if None is not sg_item:
        scen_ini.add_section('security_group')
        for i in range(len(sg_item)):
            set_str = 'set' + str(i+1)
            scen_ini.set('security_group', set_str, sg_item[i])

    # Instance
    inst_item = dic.get('instance')
    if None is not inst_item:
        scen_ini.add_section('instance')
        for i in range(len(inst_item)):
            set_str = 'set' + str(i+1)
            scen_ini.set('instance', set_str, inst_item[i])

    # Floating Ip associate
    fip_as_item = dic.get('floatingip_associate')
    if None is not fip_as_item:
        scen_ini.add_section('floatingip_associate')
        for i in range(len(fip_as_item)):
            set_str = 'set_' + str(i+1)
            scen_ini.set('floatingip_associate', set_str, fip_as_item[i])

    with open(scen_file, 'w') as configfile:
        scen_ini.write(configfile)



def test_scenario():
    # display scenario
    results = None
    display_save_scenario(save_scenario_dic, True)
    while 1:
        sel = input(RED +'Select Test Item : '+ENDC)
        if 0 is sel:
            break
        else:
            for name, age in index_save_scenario_dic.items():
                if age == sel:
                    age = str(age)
                    results = name
            if None is results:
                Reporter.PRINTR('Not exist Item')
                continue
            else:
                simple_create_test(results)
                break



def simple_create_test(item_name):
    if 'network' in item_name:
        item = save_scenario_dic.get('network')
        print item
        for x in item:
            test.network.create_network(x)

    if 'subnet' in item_name:
        item = save_scenario_dic.get('subnet')
        print item
        for x in item:
            test.network.create_subnet(x.split(', ')[0], x.split(', ')[1])

    if 'router' in item_name:
        item = save_scenario_dic.get('router')
        print item
        for x in item:
            test.network.create_router(x.split(', ')[0], x.split(', ')[1])

    if 'router-interface' in item_name:
        item = save_scenario_dic.get('router-interface')
        print item
        for x in item:
            test.network.add_router_interface(x.split(', ')[0], x.split(', ')[1])

    if 'security_group' in item_name:
        item = save_scenario_dic.get('security_group')
        arg2 = []
        print item
        for x in item:
            for i in range(len(x.split(', '))):
                if i is 0:
                    arg1 = x.split(', ')[i]
                else:
                    arg2.append((x.split(', ')[i]))

            test.network.create_securitygroup(arg1, ', '.join(arg2))

    # Instance
    if 'instance' in item_name:
        item = save_scenario_dic.get('instance')
        print item
        for x in item:
            if 2 is len(x.split(', ')):
                test.instance.create_instance(x.split(', ')[0], x.split(', ')[1], '')
            elif 2 is len(x.split(', ')):
                test.instance.create_instance(x.split(', ')[0], x.split(', ')[1], x.split(', ')[2])
            else:
                print 'invalid argument'

    # Floating IP
    if 'floatingip_associate' in item_name:
        item = save_scenario_dic.get('floatingip_associate')
        print item
        for x in item:
            test.network.floatingip_associate(x.split(', ')[0], x.split(', ')[1])
            test.floating_ip_check(x.split(', ')[0])

    test.reporter.test_summary()

    ## View Log???? ##
    report_log_viewer()



# main menu function
def scen_delete_menu():
    print 'delete_scenario'

def scenario_test_start():
    print 'scenario_test_start'

# scenaro create function
def create_network():
    value_list=[]
    title_print(' # create network')
    list = get_config_key_list('network')
    for i in range(len(list)):
        for i in range(len(list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Network : '+ENDC)
        value_list.append(list[sel-1])
        choice = raw_input(RED +'Do you want to continue to create network?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")
    save_scenario('network', value_list)

def create_subnet():
    value = []
    value_list=[]
    title_print(' # create subnet')
    net_list = get_config_key_list('network')
    sub_list = get_config_key_list('subnet')
    ## network
    for i in range(len(net_list)):
        for i in range(len(net_list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, net_list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Network : '+ENDC)
        value.append(net_list[sel-1])
        Reporter.PRINTB("|--------------------------|")

        ## subnet
        for x in range(len(sub_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, sub_list[x])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Subnet : '+ENDC)
        value.append(sub_list[sel-1])

        val_str = ', '.join(value)
        value_list.append(val_str)
        value=[]
        choice = raw_input(RED +'Do you want to continue to create subnet?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")

    save_scenario('subnet', value_list)

def create_router():
    value = []
    value_list=[]
    title_print(' # create router')
    net_list = get_config_key_list('network')
    router_list = get_config_key_list('router')
    ## network
    for i in range(len(router_list)):
        for i in range(len(router_list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, router_list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Router : '+ENDC)
        value.append(router_list[sel-1])
        Reporter.PRINTB("|--------------------------|")

        ## subnet
        for x in range(len(net_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, net_list[x])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Network : '+ENDC)
        value.append(net_list[sel-1])

        val_str = ', '.join(value)
        value_list.append(val_str)
        value=[]
        choice = raw_input(RED +'Do you want to continue to create router?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")

    save_scenario('router', value_list)

def add_router_interface():
    value = []
    value_list=[]
    title_print(' # add router-interface')
    router_list = get_config_key_list('router')
    sub_list = get_config_key_list('network')
    ## network
    for i in range(len(router_list)):
        for i in range(len(router_list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, router_list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Router : '+ENDC)
        if sel > len(router_list):
            Reporter.PRINTR(" Invalid value !!")
            continue
        value.append(router_list[sel-1])
        Reporter.PRINTB("|--------------------------|")

        ## subnet
        for x in range(len(sub_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, sub_list[x])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Subnet : '+ENDC)
        if sel > len(sub_list):
            Reporter.PRINTR(" Invalid value !!")
            value=[]
            continue
        value.append(sub_list[sel-1])

        val_str = ', '.join(value)
        value_list.append(val_str)
        value=[]
        choice = raw_input(RED +'Do you want to continue to create router-interface?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")

    save_scenario('router-interface', value_list)

def create_security_group():
    value = []
    value_list=[]
    title_print(' # create security_group')
    sec_group_list = get_config_key_list('security_group')
    rule_list = get_config_key_list('security_group_rule')
    ## network
    for i in range(len(sec_group_list)):
        for i in range(len(sec_group_list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, sec_group_list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Security Group : '+ENDC)
        if sel > len(sec_group_list):
            Reporter.PRINTR(" Invalid value !!")
            continue
        value.append(sec_group_list[sel-1])
        Reporter.PRINTB("|--------------------------|")

        ## subnet
        for x in range(len(rule_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, rule_list[x])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Subnet : '+ENDC)
        if sel > len(rule_list):
            Reporter.PRINTR(" Invalid value !!")
            value=[]
            continue
        value.append(rule_list[sel-1])

        val_str = ', '.join(value)
        value_list.append(val_str)
        value=[]
        choice = raw_input(RED +'Do you want to continue to create security group?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")

    save_scenario('security_group', value_list)

def create_instance():
    value = []
    value_list=[]
    title_print(' # create instance')
    inst_list = get_config_key_list('instance')
    net_list = get_config_key_list('network')
    sg_list = get_config_key_list('security_group')
    ## network
    for i in range(len(inst_list)):
        # Instance
        for i in range(len(inst_list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, inst_list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Instance : '+ENDC)
        value.append(inst_list[sel-1])
        Reporter.PRINTB("|--------------------------|")

        # Network
        for x in range(len(net_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, net_list[x])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Network : '+ENDC)
        value.append(net_list[sel-1])

        # security group
        for x in range(len(sg_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, sg_list[x])
        Reporter.PRINTB("| %d. %-21s |", x+2, 'Do not select!')
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Security Group : '+ENDC)
        if sel < (len(sg_list)+1):
            value.append(sg_list[sel-1])

        val_str = ', '.join(value)
        value_list.append(val_str)
        value=[]
        choice = raw_input(RED +'Do you want to continue to create inatance?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")

    save_scenario('instance', value_list)

def floatingip_associate():
    value = []
    value_list=[]
    title_print(' # add floatingip_associate')
    inst_list = get_config_key_list('instance')
    net_list = get_config_key_list('network')
    ## network
    for i in range(len(inst_list)):
        for i in range(len(inst_list)):
            Reporter.PRINTB("| %d. %-21s |", i+1, inst_list[i])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Router : '+ENDC)
        if sel > len(inst_list):
            Reporter.PRINTR(" Invalid value !!")
            continue
        value.append(inst_list[sel-1])
        Reporter.PRINTB("|--------------------------|")

        ## subnet
        for x in range(len(net_list)):
            Reporter.PRINTB("| %d. %-21s |", x+1, net_list[x])
        Reporter.PRINTB("|--------------------------|")
        sel = input(RED +'Select Subnet : '+ENDC)
        if sel > len(net_list):
            Reporter.PRINTR(" Invalid value !!")
            value=[]
            continue
        value.append(net_list[sel-1])

        val_str = ', '.join(value)
        value_list.append(val_str)
        value=[]
        choice = raw_input(RED +'Do you want to continue to assoctiate Floating ip?(y/n) : '+ENDC)
        if 'n' in choice:
            break
        Reporter.PRINTB("|--------------------------|")

    save_scenario('floatingip_associate', value_list)


def onos_state():
    print 'onos_state'

def traffic_test():
    print 'traffic_test'

def termination():
    print 'termination!!!!!'
    global exit_flag
    exit_flag=False


main_menu_map = {
    1:create_scenario_start,
    2:delete_scenario_start,
    3:scen_create_menu,
    4:scen_delete_menu,
    5:state_test_menu,
    6:termination
}

scen_menu_map = {
    1:create_network,
    2:create_subnet,
    3:create_router,
    4:add_router_interface,
    5:create_security_group,
    6:create_instance,
    7:floatingip_associate,
    8:test_scenario,
    9:save_config_scenario,
    0:main_menu
}

etc_menu_map = {
    1:onos_state,
    2:traffic_test,
    3:main_menu
}


# PROMPT = BOLD + WHITE + ' Select Menu : '+ENDC
PROMPT = BOLD + RED + ' Select Menu : '+ENDC

def main():
    global exit_flag
    main_menu()
    while exit_flag:
        try:
            global navi_menu
            if MAIN_MENU is navi_menu:
                menu = input(PROMPT)
                main_menu_map.get(menu)()
                if SCEN_CRT_MENU is menu:
                    navi_menu = SCEN_CRT_MENU
                elif ETC_MENU is menu:
                    navi_menu = ETC_MENU
                elif 6 is menu:
                    break
                else:
                    main_menu()
            elif SCEN_CRT_MENU is navi_menu:
                menu = input(PROMPT)
                scen_menu_map.get(menu)()
                if 0 is menu:
                    navi_menu = MAIN_MENU
                else:
                    scen_create_menu()
            elif SCEN_DEL_MENU is navi_menu:
                menu = input(PROMPT)
                scen_menu_map.get(menu)()
                if 0 is menu:
                    navi_menu = MAIN_MENU
                else:
                    scen_delete_menu()
            elif ETC_MENU is navi_menu:
                menu = input(PROMPT)
                etc_menu_map.get(menu)()
                if 3 is menu:
                    navi_menu = MAIN_MENU
                else:
                    state_test_menu()
        except Exception, e:
            # print 'Invailid command!'
            print 'err : ', e
            if MAIN_MENU is navi_menu:
                main_menu()
            elif SCEN_CRT_MENU is navi_menu:
                scen_create_menu()
            elif SCEN_DEL_MENU is navi_menu:
                scen_delete_menu()
            elif ETC_MENU is navi_menu:
                state_test_menu()
            # print e
            continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Reporter.PRINTR("\n\nInterrupted exit!!!")
    finally:
        Reporter.stop_all_tailer('ok')
