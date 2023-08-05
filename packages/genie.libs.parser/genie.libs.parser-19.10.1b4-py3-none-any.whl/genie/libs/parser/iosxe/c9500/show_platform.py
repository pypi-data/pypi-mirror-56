'''show_platform.py

IOSXE c9500 parsers for the following show commands:
   * show version
   * show platform
   * show redundancy
   * show inventory
'''

# Python
import re
import logging

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Or, Optional

# import parser utils
from genie.libs.parser.utils.common import Common


class ShowVersionSchema(MetaParser):
    """Schema for show version"""
    schema = {
                'version': {
                    'version_short': str,
                    'platform': str,
                    'version': str,
                    'image_id': str,
                    'rom': str,
                    'image_type': str,
                    Optional('bootldr'): str,
                    'hostname': str,
                    'uptime': str,
                    Optional('uptime_this_cp'): str,
                    Optional('jawa_revision'): str,
                    Optional('snowtrooper_revision'): str,
                    Optional('running_default_software'): bool,
                    Optional('processor_board_flash'): str,
                    Optional('last_reload_type'): str,
                    Optional('returned_to_rom_by'):  str,
                    Optional('returned_to_rom_at'): str,
                    Optional('compiled_date'): str,
                    Optional('sp_by'): str,
                    Optional('compiled_by'): str,
                    Optional('system_restarted_at'): str,
                    Optional('system_image'): str,
                    Optional('last_reload_reason'): str,
                    Optional('license_type'): str,
                    Optional('license_level'): str,
                    Optional('next_reload_license_level'): str,
                    Optional('chassis'): str,
                    Optional('processor_type'): str,
                    Optional('chassis_sn'): str,
                    Optional('rtr_type'): str,
                    'os': str,
                    'curr_config_register': str,
                    Optional('next_config_register'): str,
                    Optional('main_mem'): str,
                    Optional('number_of_intfs'): {
                        Any(): str,
                    },
                    Optional('mem_size'): {
                        Any(): str,
                    },
                    Optional('disks'): {
                        Any(): {
                            Optional('disk_size'): str,
                            Optional('type_of_disk'): str,
                        }
                    },
                    Optional('switch_num'): {
                        Any(): {
                            Optional('uptime'): str,
                            Optional('mac_address'): str,
                            Optional('mb_assembly_num'): str,
                            Optional('mb_sn'): str,
                            Optional('model_rev_num'): str,
                            Optional('mb_rev_num'): str,
                            Optional('model_num'): str,
                            Optional('system_sn'): str,
                            Optional('mode'): str,
                            Optional('model'): str,
                            Optional('sw_image'): str,
                            Optional('ports'): str,
                            Optional('sw_ver'): str,
                            Optional('active'): bool,
                        }
                    },
                    Optional('processor'): {
                        Optional('cpu_type'): str,
                        Optional('speed'): str,
                        Optional('core'): str,
                        Optional('l2_cache'): str,
                        Optional('supervisor'): str,
                    },
                    Optional('license_package'): {
                        Any(): {
                            'license_level': str,
                            'license_type': str,
                            'next_reload_license_level': str,
                        },
                    },
                    Optional('module'): {
                        Any(): {
                            Any(): {
                                Optional('suite'): str,
                                Optional('suite_current'): str,
                                Optional('type'): str,
                                Optional('suite_next_reboot'): str,
                            },
                        },
                    },
                }
            }


class ShowVersion(ShowVersionSchema):
    """Parser for show version
    parser class - implements detail parsing mechanisms for cli output.
    """
    # *************************
    # schema - class variable
    #
    # Purpose is to make sure the parser always return the output
    # (nested dict) that has the same data structure across all supported
    # parsing mechanisms (cli(), yang(), xml()).

    cli_command = 'show version'
    exclude = ['system_restarted_at', 'uptime_this_cp', 'uptime']


    def cli(self,output=None):
        """parsing mechanism: cli

        Function cli() defines the cli type output parsing mechanism which
        typically contains 3 steps: exe
        cuting, transforming, returning
        """
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        version_dict = {}
        active_dict = {}
        rtr_type = ''
        suite_flag = False
        license_flag = False

        # version
        # Cisco IOS Software [Everest], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.5, RELEASE SOFTWARE (fc3)
        # Cisco IOS Software, IOS-XE Software, Catalyst 4500 L3 Switch Software (cat4500e-UNIVERSALK9-M), Version 03.03.02.SG RELEASE SOFTWARE (fc1)
        p1 = re.compile(
            r'^[Cc]isco +IOS +[Ss]oftware\, +(?P<os>([\S]+)) +Software\, '
            r'+(?P<platform>.+) Software +\((?P<image_id>.+)\).+[Vv]ersion '
            r'+(?P<version>\S+) +.*$')

        # 16.6.5
        p2 = re.compile(r'^(?P<ver_short>\d+\.\d+).*')

        # Cisco IOS Software [Fuji], ASR1000 Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.7.1prd4, RELEASE SOFTWARE (fc1)
        # Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Experimental Version 16.8.20170924:182909 [polaris_dev-/nobackup/mcpre/BLD-BLD_POLARIS_DEV_LATEST_20170924_191550 132]
        # Cisco IOS Software, 901 Software (ASR901-UNIVERSALK9-M), Version 15.6(2)SP4, RELEASE SOFTWARE (fc3)
        
        p3 = re.compile(r'^[Cc]isco +(?P<os>[A-Z]+) +[Ss]oftware(.+)?\, '
                        r'+(?P<platform>.+) +Software +\((?P<image_id>.+)\).+( '
                        r'+Experimental)? +[Vv]ersion '
                        r'+(?P<version>[a-zA-Z0-9\.\:\(\)]+) *,?.*')

        # Copyright (c) 1986-2016 by Cisco Systems, Inc.
        p4 = re.compile(r'^Copyright +(.*)$')        

        # Technical Support: http://www.cisco.com/techsupport
        p5 = re.compile(r'^Technical +Support: +http\:\/\/www'
                        r'\.cisco\.com\/techsupport')        

        # rom
        p6 = re.compile(r'^ROM\: +(?P<rom>.+)$')
        
        # ROM: Bootstrap program is IOSv
        p7 = re.compile(r'^Bootstrap +program +is +(?P<os>.+)$')

        # bootldr
        p8 = re.compile(r'^BOOTLDR\: +(?P<bootldr>.+)$')

        # hostname & uptime
        p9 = re.compile(r'^(?P<hostname>.+) +uptime +is +(?P<uptime>.+)$')

        # uptime_this_cp
        p10 = re.compile(r'^[Uu]ptime +for +this +control +processor '
                         r'+is +(?P<uptime_this_cp>.+)$')

        # system_restarted_at
        p11 = re.compile(r'^[Ss]ystem +restarted +at '
                         r'+(?P<system_restarted_at>.+)$')

        # system_image
        # System image file is "tftp://10.1.6.241//auto/genie-ftp/Edison/cat3k_caa-universalk9.BLD__20170410_174845.SSA.bin"
        # System image file is "harddisk:test-image-PE1-13113029"
        p12 = re.compile(r'^[Ss]ystem +image +file +is '
                         r'+\"(?P<system_image>.+)\"')

        # last_reload_reason
        p13 = re.compile(r'^[Ll]ast +reload +reason\: '
                         r'+(?P<last_reload_reason>.+)$')

        # last_reload_reason
        # Last reset from power-on
        p14 = re.compile(r'^[Ll]ast +reset +from +(?P<last_reload_reason>.+)$')

        # license_type
        p15 = re.compile(r'^[Ll]icense +[Tt]ype\: +(?P<license_type>.+)$')

        # license_level
        p16 = re.compile(r'^\s*[Ll]icense +[Ll]evel\: +(?P<license_level>.+)$')

        # next_reload_license_level
        p17 = re.compile(r'^[Nn]ext +(reload|reboot) +license +Level\: '
                         r'+(?P<next_reload_license_level>.+)$')

        # chassis, processor_type, main_mem and rtr_type
        # cisco WS-C3650-24PD (MIPS) processor (revision H0) with 829481K/6147K bytes of memory.
        # cisco CSR1000V (VXE) processor (revision VXE) with 1987991K/3075K bytes of memory.
        # cisco C1111-4P (1RU) processor with 1453955K/6147K bytes of memory. 
        # Cisco IOSv (revision 1.0) with  with 435457K/87040K bytes of memory.
        # cisco WS-C3750X-24P (PowerPC405) processor (revision W0) with 262144K bytes of memory.
        # cisco ISR4451-X/K9 (2RU) processor with 1795979K/6147K bytes of memory.
        # cisco WS-C4507R+E (MPC8572) processor (revision 10) with 2097152K/20480K bytes of memory.
        p18 = re.compile(r'^(C|c)isco +(?P<chassis>[a-zA-Z0-9\-\/\+]+) '
                         r'+\((?P<processor_type>.+)\) +((processor.*)|with) '
                         r'+with +(?P<main_mem>[0-9]+)[kK](\/[0-9]+[kK])?')
        
        # chassis_sn
        p19 = re.compile(r'^[pP]rocessor +board +ID '
                         r'+(?P<chassis_sn>[a-zA-Z0-9]+)')

        # number_of_intfs
        p20 = re.compile(r'^(?P<number_of_ports>\d+) +(?P<interface>.+) '
                         r'+(interface(?:s)?|line|port(?:s)?)$')
        
        # mem_size
        p21 = re.compile(r'^(?P<mem_size>\d+)K +bytes +of '
                         r'+(?P<memories>.+) +[Mm]emory\.')

        # disks, disk_size and type_of_disk
        p22 = re.compile(r'^(?P<disk_size>\d+)K bytes of '
                         r'(?P<type_of_disk>.*) at (?P<disks>.+)$')

        # os
        # Cisco IOS Software,
        p23 = re.compile(r'^[Cc]isco +(?P<os>[a-zA-Z\-]+) '
                         r'+[Ss]oftware\,')

        # curr_config_register
        p24 = re.compile(r'^[Cc]onfiguration +register +is '
                         r'+(?P<curr_config_register>[a-zA-Z0-9]+)')

        # next_config_register
        p25 = re.compile(r'^[Cc]onfiguration +register +is +[a-zA-Z0-9]+ '
                         r'+\(will be (?P<next_config_register>[a-zA-Z0-9]+) '
                         r'at next reload\)')
        
        # switch_number
        p26 = re.compile(r'^[Ss]witch +0(?P<switch_number>\d+)$')

        # uptime
        p27 = re.compile(r'^[Ss]witch +uptime +\: +(?P<uptime>.+)$')

        # mac_address
        p28 = re.compile(r'^[Bb]ase +[Ee]thernet +MAC +[Aa]ddress '
                         r'+\: +(?P<mac_address>.+)$')

        # mb_assembly_num
        p29 = re.compile(r'^[Mm]otherboard +[Aa]ssembly +[Nn]umber +\: '
                         r'+(?P<mb_assembly_num>.+)$')
        
        # mb_sn
        p30 = re.compile(r'^[Mm]otherboard +[Ss]erial +[Nn]umber +\: '
                         r'+(?P<mb_sn>.+)$')

        # model_rev_num
        p31 = re.compile(r'^[Mm]odel +[Rr]evision +[Nn]umber +\: '
                         r'+(?P<model_rev_num>.+)$')

        # mb_rev_num
        p32 = re.compile(r'^[Mm]otherboard +[Rr]evision +[Nn]umber +\: '
                         r'+(?P<mb_rev_num>.+)$')

        # model_num
        p33 = re.compile(r'^[Mm]odel +[Nn]umber +\: +(?P<model_num>.+)$')

        # system_sn
        p34 = re.compile(r'^[Ss]ystem +[Ss]erial +[Nn]umber +\: +(?P<system_sn>.+)$')

        # IOS (tm) s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)
        p35 = re.compile(r'(?P<os>([A-Z]+)) \(\S+\)\s+(?P<platform>\S+)\s+'
                         r'Software\s+\((?P<image_id>\S+)\), Version (?P<version>\S+),'
                         r'\s*RELEASE\s+SOFTWARE\s+\(\S+\)')

        # Compiled Mon 10-Apr-17 04:35 by mcpre
        # Compiled Mon 19-Mar-18 16:39 by prod_rel_team
        p36 = re.compile(r'^Compiled +(?P<compiled_date>[\S\s]+) +by '
                         r'+(?P<compiled_by>\w+)$')

        # System returned to ROM by reload at 15:57:52 CDT Mon Sep 24 2018
        # System returned to ROM by Reload Command at 07:15:43 UTC Fri Feb 1 2019
        # System returned to ROM by reload
        # System returned to ROM by power cycle at 23:31:24 PDT Thu Sep 27 2007 (SP by power on)
        # System returned to ROM by power-on
        p37 = re.compile(r'^System +returned +to +ROM +by '
                         r'+(?P<returned_to_rom_by>[\w\s\-]+)(?: +at '
                         r'+(?P<returned_to_rom_at>[\w\s\:]+))?(?: +\(SP +by '
                         r'+(?P<sp_by>[\S\s\-]+)\))?$')

        # Last reload type: Normal Reload
        p38 = re.compile(r'^Last +reload +type\: +(?P<last_reload_type>[\S ]+)$')
        
        # P2020 CPU at 800MHz, E500v2 core, 512KB L2 Cache
        p39 = re.compile(r'^(?P<cpu_name>\S+) +(CPU|cpu|Cpu) +at '
                         r'+(?P<speed>\S+)\,(( +(?P<core>\S+) +core\, '
                         r'+(?P<l2_cache>\S+) +L2 +[Cc]ache)|( +Supervisor '
                         r'+(?P<supervisor>\S+)))$')
        
        # 98304K bytes of processor board System flash (Read/Write)
        p40 = re.compile(r'^(?P<processor_board_flash>\S+) +bytes .+$')
        
        # Running default software
        p41 = re.compile(
            r'^Running +(?P<running_default_software>\S+) +software$')

        # Jawa Revision 7, Snowtrooper Revision 0x0.0x1C
        p42 = re.compile(r'^Jawa +Revision +(?P<jawa_revision>\S+)\, '
                         r'+Snowtrooper +Revision +(?P<snowtrooper_rev>\S+)$')

        # ipbase           ipbasek9         Smart License    ipbasek9
        # securityk9       securityk9       RightToUse       securityk9
        p43 = re.compile(r'^(?P<technology>\w[\w\-]+)(?: {2,}'
                         r'(?P<license_level>\w+) {2,}(?P<license_type>\w+(?: '
                         r'+\w+)?) {2,}(?P<next_boot>\w+))?$')

        # Suite                 Suite Current         Type           Suite Next reboot
        # Technology    Technology-package           Technology-package
        p44 = re.compile(r'^(?P<aname>Suite|Technology) +((Suite +Current)|'
                         r'(Technology\-package))')

        # Suite License Information for Module:'esg'
        p45 = re.compile(r'^[Ss]uite +[Ll]icense +[Ii]nformation +for '
                         r'+[Mm]odule\:\'(?P<module>\S+)\'$')

        for line in out.splitlines():
            line = line.strip()

            # version
            # Cisco IOS Software [Everest], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.5, RELEASE SOFTWARE (fc3) 
            # Cisco IOS Software, IOS-XE Software, Catalyst 4500 L3 Switch Software (cat4500e-UNIVERSALK9-M), Version 03.03.02.SG RELEASE SOFTWARE (fc1)           
            m = p1.match(line)
            if m:
                version = m.groupdict()['version']
                # 16.6.5
                m2 = p2.match(version)
                if m2:
                    if 'version' not in version_dict:
                        version_dict['version'] = {}
                    version_dict['version']['version_short'] = \
                        m2.groupdict()['ver_short']
                    version_dict['version']['platform'] = \
                        m.groupdict()['platform']
                    version_dict['version']['version'] = \
                        m.groupdict()['version']
                    version_dict['version']['image_id'] = \
                        m.groupdict()['image_id']
                    version_dict['version']['os'] = m.groupdict()['os']
                    continue

            # Cisco IOS Software [Fuji], ASR1000 Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.7.1prd4, RELEASE SOFTWARE (fc1)
            # Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Experimental Version 16.8.20170924:182909 [polaris_dev-/nobackup/mcpre/BLD-BLD_POLARIS_DEV_LATEST_20170924_191550 132]
            # Cisco IOS Software, 901 Software (ASR901-UNIVERSALK9-M), Version 15.6(2)SP4, RELEASE SOFTWARE (fc3)
            m = p3.match(line)
            if m:
                version = m.groupdict()['version']
                # 16.6.5
                
                m2 = p2.match(version)
                
                if m2:
                    if 'version' not in version_dict:
                        version_dict['version'] = {}
                    version_dict['version']['version_short'] = \
                        m2.groupdict()['ver_short']
                    version_dict['version']['platform'] = \
                        m.groupdict()['platform']
                    version_dict['version']['version'] = \
                        m.groupdict()['version']
                    version_dict['version']['image_id'] = \
                        m.groupdict()['image_id']
                    if m.groupdict()['os']:
                        version_dict['version']['os'] = m.groupdict()['os']
                    continue

            # Copyright (c) 1986-2016 by Cisco Systems, Inc.
            m = p4.match(line)
            if m:
                version_dict.setdefault('version', {}).setdefault('image_type', 'developer image')
                continue

            # Technical Support: http://www.cisco.com/techsupport
            m = p5.match(line)
            if m:
                version_dict.setdefault('version', {}).setdefault('image_type', 'production image')
                continue

            # rom            
            m = p6.match(line)
            if m:
                rom = m.groupdict()['rom']
                version_dict['version']['rom'] = rom

                # ROM: Bootstrap program is IOSv
                m = p7.match(rom)
                if m:
                    version_dict['version']['os'] = \
                        m.groupdict()['os']
                continue

            # bootldr
            m = p8.match(line)
            if m:
                version_dict['version']['bootldr'] = \
                    m.groupdict()['bootldr']
                continue

            # hostname & uptime
            m = p9.match(line)
            if m:
                version_dict['version']['hostname'] = \
                    m.groupdict()['hostname']
                version_dict['version']['uptime'] = \
                    m.groupdict()['uptime']
                continue

            # uptime_this_cp
            m = p10.match(line)
            if m:
                version_dict['version']['uptime_this_cp'] = \
                    m.groupdict()['uptime_this_cp']
                uptime_this_cp = m.groupdict()['uptime_this_cp']
                continue

            # system_restarted_at
            m = p11.match(line)
            if m:
                version_dict['version']['system_restarted_at'] = \
                    m.groupdict()['system_restarted_at']
                continue

            # system_image
            # System image file is "tftp://10.1.6.241//auto/tftp-ssr/Edison/cat3k_caa-universalk9.BLD_V164_THROTTLE_LATEST_20170410_174845.SSA.bin"
            # System image file is "harddisk:test-image-PE1-13113029"
            m = p12.match(line)
            if m:
                version_dict['version']['system_image'] = \
                    m.groupdict()['system_image']
                continue

            # last_reload_reason
            m = p13.match(line)
            if m:
                version_dict['version']['last_reload_reason'] = \
                    m.groupdict()['last_reload_reason']
                continue

            # last_reload_reason
            # Last reset from power-on
            m = p14.match(line)
            if m:
                version_dict['version']['last_reload_reason'] = \
                    m.groupdict()['last_reload_reason']
                continue

            # license_type
            m = p15.match(line)
            if m:
                version_dict['version']['license_type'] = \
                    m.groupdict()['license_type']
                continue

            # license_level
            # License Level: entservices   Type: Permanent
            # License Level: AdvancedMetroIPAccess
            m = p16.match(line)
            if m:
                group = m.groupdict()
                if 'Type:' in group['license_level']:
                    # entservices   Type: Permanent
                    p16_1 = re.compile(r'(?P<license_level>\S+) +Type\: '
                                       r'+(?P<license_type>\S+)')
                    lic_type = group['license_level'].strip()
                    m_1 = p16_1.match(lic_type)
                    group = m_1.groupdict()
                    version_dict['version']['license_type'] = group['license_type']
                    version_dict['version']['license_level'] = group['license_level']
                else:
                    version_dict['version']['license_level'] = group['license_level']
                continue

            # next_reload_license_level
            # Next reboot license Level: entservices
            # Next reload license Level: advipservices
            m = p17.match(line)
            if m:
                version_dict['version']['next_reload_license_level'] = \
                    m.groupdict()['next_reload_license_level']
                continue

            # chassis, processor_type, main_mem and rtr_type
            # cisco WS-C3650-24PD (MIPS) processor (revision H0) with 829481K/6147K bytes of memory.
            # cisco CSR1000V (VXE) processor (revision VXE) with 1987991K/3075K bytes of memory.
            # cisco C1111-4P (1RU) processor with 1453955K/6147K bytes of memory. 
            # Cisco IOSv (revision 1.0) with  with 435457K/87040K bytes of memory.
            # cisco WS-C3750X-24P (PowerPC405) processor (revision W0) with 262144K bytes of memory.
            # cisco ISR4451-X/K9 (2RU) processor with 1795979K/6147K bytes of memory.
            m = p18.match(line)
            if m:
                version_dict['version']['chassis'] \
                    = m.groupdict()['chassis']
                version_dict['version']['main_mem'] \
                    = m.groupdict()['main_mem']
                version_dict['version']['processor_type'] \
                    = m.groupdict()['processor_type']
                if 'C3850' in version_dict['version']['chassis'] or \
                   'C3650' in version_dict['version']['chassis']:
                    version_dict['version']['rtr_type'] = rtr_type = 'Edison'
                elif 'ASR1' in version_dict['version']['chassis']:
                    version_dict['version']['rtr_type'] = rtr_type = 'ASR1K'
                elif 'CSR1000V' in version_dict['version']['chassis']:
                    version_dict['version']['rtr_type'] = rtr_type = 'CSR1000V'
                elif 'C11' in version_dict['version']['chassis']:
                    version_dict['version']['rtr_type'] = rtr_type = 'ISR'
                else:
                    version_dict['version']['rtr_type'] = rtr_type = version_dict['version']['chassis']
                continue

            # chassis_sn
            m = p19.match(line)
            if m:
                version_dict['version']['chassis_sn'] \
                    = m.groupdict()['chassis_sn']
                continue

            # number_of_intfs
            # 1 External Alarm interface
            # 1 FastEthernet interface
            # 12 Gigabit Ethernet interfaces
            # 2 Ten Gigabit Ethernet interfaces
            # 1 terminal line
            # 8 Channelized T1 ports
            m = p20.match(line)
            if m:
                interface = m.groupdict()['interface']
                if 'number_of_intfs' not in version_dict['version']:
                    version_dict['version']['number_of_intfs'] = {}
                version_dict['version']['number_of_intfs'][interface] = \
                    m.groupdict()['number_of_ports']
                continue

            # mem_size
            m = p21.match(line)
            if m:
                memories = m.groupdict()['memories']
                if 'mem_size' not in version_dict['version']:
                    version_dict['version']['mem_size'] = {}
                version_dict['version']['mem_size'][memories] = \
                    m.groupdict()['mem_size']
                continue

            # disks, disk_size and type_of_disk
            m = p22.match(line)
            if m:
                disks = m.groupdict()['disks']
                if 'disks' not in version_dict['version']:
                    version_dict['version']['disks'] = {}
                if disks not in version_dict['version']['disks']:
                    version_dict['version']['disks'][disks] = {}
                version_dict['version']['disks'][disks]['disk_size'] = \
                    m.groupdict()['disk_size']
                version_dict['version']['disks'][disks]['type_of_disk'] = \
                    m.groupdict()['type_of_disk']
                continue

            # os
            m = p23.match(line)
            if m:
                version_dict['version']['os'] = m.groupdict()['os']
            
                continue

            # curr_config_register
            m = p24.match(line)
            if m:
                version_dict['version']['curr_config_register'] \
                    = m.groupdict()['curr_config_register']

            # next_config_register
            m = p25.match(line)
            if m:
                version_dict['version']['next_config_register'] \
                    = m.groupdict()['next_config_register']
                continue

            # switch_number
            m = p26.match(line)
            if m:
                switch_number = m.groupdict()['switch_number']
                if 'Edison' in rtr_type:
                    if 'switch_num' not in version_dict['version']:
                        version_dict['version']['switch_num'] = {}
                    if switch_number not in version_dict['version']['switch_num']:
                        version_dict['version']['switch_num'][switch_number] = {}
                continue

            # uptime
            m = p27.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    continue
                version_dict['version']['switch_num'][switch_number]['uptime'] = m.groupdict()['uptime']
                continue

            # mac_address
            m = p28.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('mac_address', m.groupdict()['mac_address'])
                    continue
                version_dict['version']['switch_num'][switch_number]['mac_address'] = m.groupdict()['mac_address']
                continue

            # mb_assembly_num
            m = p29.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('mb_assembly_num', m.groupdict()['mb_assembly_num'])
                    continue
                version_dict['version']['switch_num'][switch_number]['mb_assembly_num'] = m.groupdict()['mb_assembly_num']
                continue

            # mb_sn
            m = p30.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('mb_sn', m.groupdict()['mb_sn'])
                    continue
                version_dict['version']['switch_num'][switch_number]['mb_sn'] = m.groupdict()['mb_sn']
                continue

            # model_rev_num
            m = p31.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('model_rev_num', m.groupdict()['model_rev_num'])
                    continue
                version_dict['version']['switch_num'][switch_number]['model_rev_num'] = m.groupdict()['model_rev_num']
                continue

            # mb_rev_num
            m = p32.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('mb_rev_num', m.groupdict()['mb_rev_num'])
                    continue
                version_dict['version']['switch_num'][switch_number]['mb_rev_num'] = m.groupdict()['mb_rev_num']
                continue

            # model_num
            m = p33.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('model_num', m.groupdict()['model_num'])
                    continue
                version_dict['version']['switch_num'][switch_number]['model_num'] = m.groupdict()['model_num']
                continue

            # system_sn
            m = p34.match(line)
            if m:
                if 'switch_num' not in version_dict['version']:
                    active_dict.setdefault('system_sn', m.groupdict()['system_sn'])
                    continue
                version_dict['version']['switch_num'][switch_number]['system_sn'] = m.groupdict()['system_sn']
                continue

            # IOS (tm) s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF7, RELEASE SOFTWARE (fc1)
            m = p35.match(line)
            if m:
                group = m.groupdict()
                os = group['os']
                platform = group['platform']
                image_id = group['image_id']
                version = group['version']
                
                # 16.6.5
                result = p2.match(version)
                version_short_dict = result.groupdict()
                version_short = version_short_dict['ver_short']

                version_dict2 = version_dict.setdefault('version', {})

                version_dict2['os'] = os
                version_dict2['version_short'] = version_short
                version_dict2['platform'] = platform
                version_dict2['version'] = version
                version_dict2['image_id'] = image_id

                continue

            # Compiled Mon 10-Apr-17 04:35 by mcpre
            # Compiled Mon 19-Mar-18 16:39 by prod_rel_team
            m36 = p36.match(line)
            if m36:
                group = m36.groupdict()
                version_dict['version']['compiled_date'] = group['compiled_date']
                version_dict['version']['compiled_by'] = group['compiled_by']

                continue

            # System returned to ROM by reload at 15:57:52 CDT Mon Sep 24 2018
            # System returned to ROM by Reload Command at 07:15:43 UTC Fri Feb 1 2019
            # System returned to ROM by reload
            # System returned to ROM by power cycle at 23:31:24 PDT Thu Sep 27 2007 (SP by power on)
            # System returned to ROM by power-on
            m37 = p37.match(line)
            if m37:
                group = m37.groupdict()
                
                if group['returned_to_rom_at']:
                    version_dict['version']['returned_to_rom_by'] = group['returned_to_rom_by']
                    version_dict['version']['returned_to_rom_at'] = group['returned_to_rom_at']
                else:
                    version_dict['version']['returned_to_rom_by'] = group['returned_to_rom_by']

                if group['sp_by']:
                    version_dict['version']['sp_by'] = group['sp_by']

                continue

            # Last reload type: Normal Reload
            m38 = p38.match(line)
            if m38:
                version_dict['version']['last_reload_type'] = m38.groupdict()['last_reload_type']

                continue

            # P2020 CPU at 800MHz, E500v2 core, 512KB L2 Cache
            # MPC8572 CPU at 1.5GHz, Supervisor 7
            m39 = p39.match(line)
            if m39:
                group = m39.groupdict()
                cpu_dict = version_dict['version'].setdefault('processor', {})
                if group['supervisor']:
                    cpu_dict['cpu_type'] = group['cpu_name']
                    cpu_dict['speed'] = group['speed']
                    cpu_dict['supervisor'] = group['supervisor']
                else:
                    cpu_dict['cpu_type'] = group['cpu_name']
                    cpu_dict['speed'] =  group['speed']
                    cpu_dict['core'] = group['core']
                    cpu_dict['l2_cache'] = group['l2_cache']

                continue

            # 98304K bytes of processor board System flash (Read/Write)
            m40 = p40.match(line)
            if m40:
                flash_dict = version_dict['version']
                in_kb = m40.groupdict()['processor_board_flash']
                flash_dict['processor_board_flash'] = in_kb

                continue

            # Running default software
            m41 = p41.match(line)
            if m41:
                version_dict['version']['running_default_software'] = True

                continue

            # Jawa Revision 7, Snowtrooper Revision 0x0.0x1C
            m42 = p42.match(line)
            if m42:
                version_dict['version']['jawa_revision'] = m42.groupdict()['jawa_revision']
                version_dict['version']['snowtrooper_revision']= m42.groupdict()['snowtrooper_rev']

                continue
            
            # ipbase           ipbasek9         Smart License    ipbasek9
            # securityk9       securityk9       RightToUse       securityk9
            m43 = p43.match(line)
            if m43:
                group = m43.groupdict()

                if license_flag:
                    lic_initial_dict = version_dict['version'].setdefault('license_package', {})
                    license_dict = lic_initial_dict.setdefault(group['technology'], {})
                    
                    if group['license_type']:
                        license_dict.update({'license_type': group['license_type']})
                    
                    if group['license_level']:
                        license_dict.update({'license_level': group['license_level']})
                    
                    if group['next_boot']:
                        license_dict.update(
                            {'next_reload_license_level': group['next_boot']})
                
                if suite_flag:
                    suite_lic_dict = suite_dict.setdefault(group['technology'], {})

                    if group['license_level']:
                        suite_lic_dict.update(
                            {'suite_current': group['license_level']})

                    if group['license_type']:
                        suite_lic_dict.update({'type': group['license_type'].strip()})
                    
                    if group['next_boot']:
                        suite_lic_dict.update({'suite_next_reboot': group['next_boot']})
                
                continue

            # Suite                 Suite Current         Type           Suite Next reboot
            # Technology    Technology-package           Technology-package
            m44 = p44.match(line)
            if m44:
                if 'Suite' in m44.groupdict()['aname']:
                    suite_flag = True
                
                if 'Technology' in m44.groupdict()['aname']: 
                    license_flag = True
                    suite_flag = False

                continue
        
            # Suite License Information for Module:'esg'
            m45 = p45.match(line)
            if m45:
                module_dict = version_dict['version'].setdefault('module', {})
                suite_dict = module_dict.setdefault(m45.groupdict()['module'], {})

                continue

        # table2 for C3850
        tmp2 = genie.parsergen.oper_fill_tabular(right_justified=True,
                                           header_fields=
                                                  [ "Switch",
                                                    "Ports",
                                                    "Model             ",
                                                    'SW Version       ',
                                                    "SW Image              ",
                                                    "Mode   "],
                                              label_fields=
                                                  [ "switch_num",
                                                    "ports",
                                                    "model",
                                                    "sw_ver",
                                                    'sw_image',
                                                    'mode'],
                                              index=[0,],
                                              table_terminal_pattern=r"^\n",
                                              device_output=out,
                                              device_os='iosxe')

        # switch_number
        # license table for Cat3850
        tmp = genie.parsergen.oper_fill_tabular(right_justified=True,
                                          header_fields=
                                                  [ "Current            ",
                                                    "Type            ",
                                                    "Next reboot  "],
                                              label_fields=
                                                  [ "license_level",
                                                    "license_type",
                                                    "next_reload_license_level"],
                                              table_terminal_pattern=r"^\n",
                                              device_output=out,
                                              device_os='iosxe')

        if tmp.entries:
            res = tmp 
            for key in res.entries.keys():
                for k, v in res.entries[key].items():
                    version_dict['version'][k] = v
            if tmp2.entries:
                res2 = tmp2
                for key in res2.entries.keys():
                    if 'switch_num' not in version_dict['version']:
                        version_dict['version']['switch_num'] = {}
                    if '*' in key:
                        p = re.compile(r'\**\ *(?P<new_key>\d)')
                        m = p.match(key)
                        switch_no = m.groupdict()['new_key']
                        if m:
                            if switch_no not in version_dict['version']['switch_num']:
                                version_dict['version']['switch_num'][switch_no] = {}
                            for k, v in res2.entries[key].items():
                                if 'switch_num' != k:
                                    version_dict['version']['switch_num'][switch_no][k] = v
                            version_dict['version']['switch_num'][switch_no]['uptime'] = uptime_this_cp
                            version_dict['version']['switch_num'][switch_no]['active'] = True
                            version_dict['version']['switch_num'][switch_no].\
                                update(active_dict) if active_dict else None
                    else:
                        for k, v in res2.entries[key].items():
                            if key not in version_dict['version']['switch_num']:
                                version_dict['version']['switch_num'][key] = {}
                            if 'switch_num' != k:
                                version_dict['version']['switch_num'][key][k] = v
                        version_dict['version']['switch_num'][key]['active'] = False 

        return version_dict


class ShowRedundancySchema(MetaParser):
    """Schema for show redundancy """
    schema = {
                'red_sys_info': {
                    'available_system_uptime': str,
                    'switchovers_system_experienced': str,
                    'standby_failures': str,
                    'last_switchover_reason': str,
                    'hw_mode': str,
                    'conf_red_mode': str,
                    'oper_red_mode': str,
                    'maint_mode': str,
                    'communications': str,
                    Optional('communications_reason'): str,
                    },
                'slot': {
                    Any(): {
                        'curr_sw_state': str,
                        'uptime_in_curr_state': str,
                        'image_ver': str,
                        Optional('boot'): str,
                        Optional('config_file'): str,
                        Optional('bootldr'): str,
                        'config_register': str,
                    }
                }
            }


class ShowRedundancy(ShowRedundancySchema):
    """Parser for show redundancy
    parser class - implements detail parsing mechanisms for cli output.
    """
    # *************************
    # schema - class variable
    #
    # Purpose is to make sure the parser always return the output
    # (nested dict) that has the same data structure across all supported
    # parsing mechanisms (cli(), yang(), xml()).

    cli_command = 'show redundancy'
    exclude = ['available_system_uptime', 'uptime_in_curr_state']


    def cli(self,output=None):
        """parsing mechanism: cli

        Function cli() defines the cli type output parsing mechanism which
        typically contains 3 steps: exe
        cuting, transforming, returning
        """
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        redundancy_dict = {}
        for line in out.splitlines():
            line = line.rstrip()

            # available_system_uptime
            p1 = re.compile(
                r'\s*[Aa]vailable +[Ss]ystem +[Uu]ptime +\= +(?P<available_system_uptime>.+)$')
            m = p1.match(line)
            if m:
                redundancy_dict.setdefault('red_sys_info', {})
                redundancy_dict['red_sys_info']['available_system_uptime'] = \
                    m.groupdict()['available_system_uptime']
                continue

            # switchovers_system_experienced
            p2 = re.compile(
                r'\s*[Ss]witchovers +system +experienced +\= +(?P<switchovers_system_experienced>\d+)$')
            m = p2.match(line)
            if m:
                redundancy_dict['red_sys_info']['switchovers_system_experienced'] = \
                    m.groupdict()['switchovers_system_experienced']
                continue

            # standby_failures
            p3 = re.compile(
                r'\s*[Ss]tandby +failures +\= +(?P<standby_failures>\d+)$')
            m = p3.match(line)
            if m:
                redundancy_dict['red_sys_info']['standby_failures'] = \
                    m.groupdict()['standby_failures']
                continue

            # last_switchover_reason
            p4 = re.compile(
                r'^\s*[Ll]ast +[Ss]witchover +[Rr]eason +\= +(?P<last_switchover_reason>.+)$')
            m = p4.match(line)
            if m:
                redundancy_dict['red_sys_info']['last_switchover_reason'] = \
                    m.groupdict()['last_switchover_reason']
                continue

            # hw_mode
            p5 = re.compile(
                r'\s*[Hh]ardware +[Mm]ode +\= +(?P<hw_mode>\S+)$')
            m = p5.match(line)
            if m:
                redundancy_dict['red_sys_info']['hw_mode'] = \
                    m.groupdict()['hw_mode']
                continue

            # conf_red_mode
            p6 = re.compile(
                r'\s*[Cc]onfigured +[Rr]edundancy +[Mm]ode +\= +(?P<conf_red_mode>\S+)$')
            m = p6.match(line)
            if m:
                redundancy_dict['red_sys_info']['conf_red_mode'] = \
                    m.groupdict()['conf_red_mode']
                continue

            # oper_red_mode
            p7 = re.compile(
                r'\s*[Oo]perating +[Rr]edundancy +[Mm]ode +\= +(?P<oper_red_mode>.+)$')
            m = p7.match(line)
            if m:
                redundancy_dict['red_sys_info']['oper_red_mode'] = \
                    m.groupdict()['oper_red_mode']
                continue

            # maint_mode
            p7 = re.compile(
                r'\s*[Mm]aintenance +[Mm]ode +\= +(?P<maint_mode>\S+)$')
            m = p7.match(line)
            if m:
                redundancy_dict['red_sys_info']['maint_mode'] = \
                    m.groupdict()['maint_mode']
                continue

            # communications
            p8 = re.compile(r'^\s*[Cc]ommunications +\= +(?P<communications>\S+)$')
            m = p8.match(line)
            if m:
                redundancy_dict['red_sys_info']['communications'] = \
                    m.groupdict()['communications']

            # communications_reason
            p8 = re.compile(r'^\s*[Cc]ommunications +\= +(?P<communications>\S+)\s+[Rr]eason\: +(?P<communications_reason>.+)$')
            m = p8.match(line)
            if m:
                redundancy_dict['red_sys_info']['communications'] = \
                    m.groupdict()['communications']
                redundancy_dict['red_sys_info']['communications_reason'] = \
                    m.groupdict()['communications_reason']
                continue

            # slot number
            p9 = re.compile(r'^\s*\S+ +[Ll]ocation +\= +(?P<slot>.+)$')
            m = p9.match(line)
            if m:
                slot = m.groupdict()['slot']
                if 'slot' not in redundancy_dict:
                    redundancy_dict['slot'] = {}
                if slot not in redundancy_dict['slot']:
                    redundancy_dict['slot'][slot] = {}
                continue

            # curr_sw_state
            p10 = re.compile(r'^\s*[Cc]urrent +[Ss]oftware +[Ss]tate +\= +(?P<curr_sw_state>.+)$')
            m = p10.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['curr_sw_state'] = \
                        m.groupdict()['curr_sw_state']
                continue

            # uptime_in_curr_state
            p11 = re.compile(r'^\s*[Uu]ptime +[Ii]n +[Cc]urrent +[Ss]tate +\= +(?P<uptime_in_curr_state>.+)$')
            m = p11.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['uptime_in_curr_state'] = \
                        m.groupdict()['uptime_in_curr_state']
                continue

            # image_ver
            p12 = re.compile(r'^\s*[Ii]mage +[Vv]ersion +\= +(?P<image_ver>.+)$')
            m = p12.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['image_ver'] = \
                        m.groupdict()['image_ver']
                continue

            # boot
            p13 = re.compile(r'^\s*BOOT +\= +(?P<boot>.+)$')
            m = p13.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['boot'] = \
                        m.groupdict()['boot']
                continue

            # config_file
            p14 = re.compile(r'\s*CONFIG_FILE +\= +(?P<config_file>.?)$')
            m = p14.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['config_file'] = \
                        m.groupdict()['config_file']
                continue

            # bootldr
            p15 = re.compile(r'\s*BOOTLDR +\= +(?P<bootldr>.?)$')
            m = p15.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['bootldr'] = \
                        m.groupdict()['bootldr']
                continue

            # config_register
            p16 = re.compile(r'^\s*[Cc]onfiguration +[Rr]egister = (?P<config_register>.+)$')
            m = p16.match(line)
            if m:
                if 'slot' in redundancy_dict:
                    redundancy_dict['slot'][slot]['config_register'] = \
                        m.groupdict()['config_register']
                continue

        return redundancy_dict


# =====================
# Schema for:
#   * 'show inventory'
# =====================
class ShowInventorySchema(MetaParser):

    ''' Schema for:
        * 'show inventory'
    '''

    schema = {
        Optional('main'):
            {Optional('swstack'): bool,
            Optional('chassis'):
                {Any():
                    {Optional('name'): str,
                    Optional('descr'): str,
                    Optional('pid'): str,
                    Optional('vid'): str,
                    Optional('sn'): str,
                    },
                },
            },
        'slot':
            {Any():
                {Optional('rp'):
                    {Any():
                        {Optional('name'): str,
                        Optional('descr'): str,
                        Optional('pid'): str,
                        Optional('vid'): str,
                        Optional('sn'): str,
                        Optional('swstack_power'): str,
                        Optional('swstack_power_sn'): str,
                        Optional('subslot'):
                            {Any(): 
                                {Any(): 
                                    {Optional('name'): str,
                                    Optional('descr'): str,
                                    Optional('pid'): str,
                                    Optional('vid'): str,
                                    Optional('sn'): str,
                                    },
                                },
                            },
                        },
                    },
                Optional('lc'):
                    {Any():
                        {Optional('name'): str,
                        Optional('descr'): str,
                        Optional('pid'): str,
                        Optional('vid'): str,
                        Optional('sn'): str,
                        Optional('swstack_power'): str,
                        Optional('swstack_power_sn'): str,
                        Optional('subslot'):
                            {Any(): 
                                {Any(): 
                                    {Optional('name'): str,
                                    Optional('descr'): str,
                                    Optional('pid'): str,
                                    Optional('vid'): str,
                                    Optional('sn'): str,
                                    },
                                },
                            },
                        },
                    },
                Optional('other'):
                    {Any():
                        {Optional('name'): str,
                        Optional('descr'): str,
                        Optional('pid'): str,
                        Optional('vid'): str,
                        Optional('sn'): str,
                        Optional('swstack_power'): str,
                        Optional('swstack_power_sn'): str,
                        Optional('subslot'):
                            {Any(): 
                                {Any(): 
                                    {Optional('name'): str,
                                    Optional('descr'): str,
                                    Optional('pid'): str,
                                    Optional('vid'): str,
                                    Optional('sn'): str,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


# ====================
# Parser for:
#   * 'show inventory'
# ====================
class ShowInventory(ShowInventorySchema):
    
    ''' Parser for:
        * 'show inventory'
    '''

    cli_command = ['show inventory']

    def cli(self, output=None):

        if output is None:
            # Build command
            cmd = self.cli_command[0]
            # Execute command
            out = self.device.execute(cmd)
        else:
            out = output

        # Init vars
        ret_dict = {}
        name = descr = slot = subslot = pid = ''
        asr900_rp = False

        # NAME: "Switch 1", DESCR: "WS-C3850-24P-E"
        # NAME: "StackPort5/2", DESCR: "StackPort5/2"
        # NAME: "Switch 5 - Power Supply A", DESCR: "Switch 5 - Power Supply A"
        # NAME: "subslot 0/0 transceiver 2", DESCR: "GE T"
        # NAME: "NIM subslot 0/0", DESCR: "Front Panel 3 ports Gigabitethernet Module"
        p1 = re.compile(r'^NAME: +\"(?P<name>.*)\",'
                         ' +DESCR: +\"(?P<descr>.*)\"$')

        # PID: ASR-920-24SZ-IM   , VID: V01  , SN: CAT1902V19M
        # PID: SFP-10G-LR        , VID: CSCO , SN: CD180456291
        # PID: A900-IMA3G-IMSG   , VID: V01  , SN: FOC2204PAP1
        # PID: SFP-GE-T          , VID: V02  , SN: MTC2139029X
        # PID: ISR4331-3x1GE     , VID: V01  , SN:
        # PID: ISR4331/K9        , VID:      , SN: FDO21520TGH
        # PID: ISR4331/K9        , VID:      , SN:
        # PID: , VID: 1.0  , SN: 1162722191
        p2 = re.compile(r'^PID: +(?P<pid>\S+)? *, +VID:(?: +(?P<vid>(\S+)))? *,'
                         ' +SN:(?: +(?P<sn>(\S+)))?$')

        for line in out.splitlines():
            line = line.strip()

            # NAME: "Switch 1", DESCR: "WS-C3850-24P-E"
            # NAME: "StackPort5/2", DESCR: "StackPort5/2"
            # NAME: "Switch 5 - Power Supply A", DESCR: "Switch 5 - Power Supply A"
            # NAME: "subslot 0/0 transceiver 2", DESCR: "GE T"
            # NAME: "NIM subslot 0/0", DESCR: "Front Panel 3 ports Gigabitethernet Module"
            m = p1.match(line)
            if m:
                group = m.groupdict()
                name = group['name'].strip()
                descr = group['descr'].strip()

                # Switch 1
                # module 0
                p1_1 = re.compile(r'^(Switch|[Mm]odule) +(?P<slot>(\S+))')
                m1_1 = p1_1.match(name)
                if m1_1:
                    slot = m1_1.groupdict()['slot']
                    # Creat slot_dict
                    slot_dict = ret_dict.setdefault('slot', {}).setdefault(slot, {})

                # Power Supply Module 0
                # Power Supply Module 1
                p1_2 = re.compile(r'Power Supply Module')
                m1_2 = p1_2.match(name)
                if m1_2:
                    slot = name.replace('Power Supply Module ', 'P')
                    # Creat slot_dict
                    slot_dict = ret_dict.setdefault('slot', {}).setdefault(slot, {})

                # SPA subslot 0/0
                # IM subslot 0/1
                # NIM subslot 0/0
                p1_3 = re.compile(r'^(SPA|IM|NIM) +subslot +(?P<slot>(\d+))/(?P<subslot>(\d+))')
                m1_3 = p1_3.match(name)
                if m1_3:
                    group = m1_3.groupdict()
                    slot = group['slot']
                    subslot = group['subslot']
                    # Creat slot_dict
                    slot_dict = ret_dict.setdefault('slot', {}).setdefault(slot, {})

                # subslot 0/0 transceiver 0
                p1_4 = re.compile(r'^subslot +(?P<slot>(\d+))\/(?P<subslot>(.*))')
                m1_4 = p1_4.match(name)
                if m1_4:
                    group = m1_4.groupdict()
                    slot = group['slot']
                    subslot = group['subslot']
                    # Creat slot_dict
                    slot_dict = ret_dict.setdefault('slot', {}).setdefault(slot, {})

                # StackPort1/1
                p1_5 = re.compile(r'^StackPort(?P<slot>(\d+))/(?P<subslot>(\d+))$')
                m1_5 = p1_5.match(name)
                if m1_5:
                    group = m1_5.groupdict()
                    slot = group['slot']
                    subslot = group['subslot']
                    # Create slot_dict
                    slot_dict = ret_dict.setdefault('slot', {}).setdefault(slot, {})

                # Fan Tray
                p1_6 = re.compile(r'^Fan +Tray$')
                m1_6 = p1_6.match(name)
                if m1_6:
                    slot = name.replace(' ', '_')
                    # Create slot_dict
                    slot_dict = ret_dict.setdefault('slot', {}).setdefault(slot, {})
                # go to next line
                continue

            # PID: ASR-920-24SZ-IM   , VID: V01  , SN: CAT1902V19M
            # PID: SFP-10G-LR        , VID: CSCO , SN: CD180456291
            # PID: A900-IMA3G-IMSG   , VID: V01  , SN: FOC2204PAP1
            # PID: SFP-GE-T          , VID: V02  , SN: MTC2139029X
            # PID: ISR4331-3x1GE     , VID: V01  , SN:
            # PID: ISR4331/K9        , VID:      , SN: FDO21520TGH
            # PID: ISR4331/K9        , VID:      , SN:
            m = p2.match(line)
            if m:
                group = m.groupdict()
                pid = group['pid'] or ''
                vid = group['vid'] or ''
                sn = group['sn'] or ''

                # NAME: "Chassis", DESCR: "Cisco ASR1006 Chassis"
                if 'Chassis' in name:
                    main_dict = ret_dict.setdefault('main', {}).\
                                         setdefault('chassis', {}).\
                                         setdefault(pid, {})
                    main_dict['name'] = name
                    main_dict['descr'] = descr
                    main_dict['pid'] = pid
                    main_dict['vid'] = vid
                    main_dict['sn'] = sn

                # PID: STACK-T1-50CM     , VID: V01  , SN: LCC1921G250
                if 'STACK' in pid:
                    main_dict = ret_dict.setdefault('main', {})
                    main_dict['swstack'] = True

                if ('ASR-9') in pid and ('PWR' not in pid) and ('FAN' not in pid):
                    rp_dict = ret_dict.setdefault('slot', {}).\
                                       setdefault('0', {}).\
                                       setdefault('rp', {}).\
                                       setdefault(pid, {})
                    rp_dict['name'] = name
                    rp_dict['descr'] = descr
                    rp_dict['pid'] = pid
                    rp_dict['vid'] = vid
                    rp_dict['sn'] = sn
                    asr900_rp = True

                # Ensure name, slot have been previously parsed
                if not name or not slot:
                    continue

                # PID: ASR1000-RP2       , VID: V02  , SN: JAE153408NJ
                # PID: ASR1000-RP2       , VID: V03  , SN: JAE1703094H
                # PID: WS-C3850-24P-E    , VID: V01  , SN: FCW1932D0LB
                if ('RP' in pid) or ('WS-C' in pid) or ('R' in name):
                    rp_dict = slot_dict.setdefault('rp', {}).\
                                        setdefault(pid, {})
                    rp_dict['name'] = name
                    rp_dict['descr'] = descr
                    rp_dict['pid'] = pid
                    rp_dict['vid'] = vid
                    rp_dict['sn'] = sn

                # PID: ASR1000-SIP40     , VID: V02  , SN: JAE200609WP
                # PID: ISR4331/K9        , VID:      , SN: FDO21520TGH
                # PID: ASR1002-X         , VID: V07, SN: FOX1111P1M1
                # PID: ASR1002-HX        , VID:      , SN:
                elif ('SIP' in pid) or ('ISR' in pid) or ('-X' in pid) or ('-HX' in pid):
                    lc_dict = slot_dict.setdefault('lc', {}).\
                                        setdefault(pid, {})
                    lc_dict['name'] = name
                    lc_dict['descr'] = descr
                    lc_dict['pid'] = pid
                    lc_dict['vid'] = vid
                    lc_dict['sn'] = sn

                # PID: SP7041-E          , VID: E    , SN: MTC164204VE
                # PID: SFP-GE-T          , VID: V02  , SN: MTC2139029X   
                elif subslot:
                    if ('STACK' in pid) or asr900_rp:
                        subslot_dict = rp_dict.setdefault('subslot', {}).\
                                               setdefault(subslot, {}).\
                                               setdefault(pid, {})
                    else:
                        subslot_dict = lc_dict.setdefault('subslot', {}).\
                                               setdefault(subslot, {}).\
                                               setdefault(pid, {})
                    subslot_dict['name'] = name
                    subslot_dict['descr'] = descr
                    subslot_dict['pid'] = pid
                    subslot_dict['vid'] = vid
                    subslot_dict['sn'] = sn

                # PID: ASR1006-PWR-AC    , VID: V01  , SN: ART1210Q049
                # PID: ASR1006-PWR-AC    , VID: V01  , SN: ART1210Q04C
                # PID: ASR-920-FAN-M     , VID: V01  , SN: CAT1903V028
                else:
                    other_dict = slot_dict.setdefault('other', {}).\
                                           setdefault(pid, {})
                    other_dict['name'] = name
                    other_dict['descr'] = descr
                    other_dict['pid'] = pid
                    other_dict['vid'] = vid
                    other_dict['sn'] = sn

                # Reset to avoid overwrite
                name = descr = slot = subslot = ''
                continue

        return ret_dict


class ShowPlatformSchema(MetaParser):
    """Schema for show platform"""
    schema = {
                Optional('main'): {
                    Optional('switch_mac_address'): str,
                    Optional('mac_persistency_wait_time'): str,
                    Optional('chassis'): str,
                    Optional('swstack'): bool
                },
                'slot': {
                    Any(): {
                        Optional('rp'): {
                            Any(): {
                                Optional('sn'): str,
                                'state': str,
                                Optional('num_of_ports'): str,
                                Optional('mac_address'): str,
                                Optional('hw_ver'): str,
                                Optional('sw_ver'): str,
                                Optional('swstack_role'): str,
                                Optional('swstack_priority'): str,
                                Optional('ports'): str,
                                Optional('role'): str,
                                Optional('name'): str,
                                Optional('slot'): str,
                                Optional('priority'): str,
                                Optional('insert_time'): str,
                                Optional('fw_ver'): str,
                                Optional('cpld_ver'): str,
                            }
                        },
                        Optional('lc'): {
                            Any(): {
                                Optional('cpld_ver'): str,
                                Optional('fw_ver'): str,
                                Optional('insert_time'): str,
                                Optional('name'): str,
                                Optional('slot'): str,
                                Optional('state'): str,
                                Optional('subslot'): {
                                    Any(): {
                                        Any(): {
                                            Optional('insert_time'): str,
                                            Optional('name'): str,
                                            Optional('state'): str,
                                            Optional('subslot'): str,
                                        }
                                    }
                                }
                            }
                        },
                        Optional('other'): {
                            Any(): {
                                Optional('cpld_ver'): str,
                                Optional('fw_ver'): str,
                                Optional('insert_time'): str,
                                Optional('name'): str,
                                Optional('slot'): str,
                                Optional('state'): str,
                                Optional('subslot'): {
                                    Any(): {
                                        Any(): {
                                            Optional('insert_time'): str,
                                            Optional('name'): str,
                                            Optional('state'): str,
                                            Optional('subslot'): str,
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }


class ShowPlatform(ShowPlatformSchema):
    """Parser for show platform
    parser class - implements detail parsing mechanisms for cli output.
    """
    # *************************
    # schema - class variable
    #
    # Purpose is to make sure the parser always return the output
    # (nested dict) that has the same data structure across all supported
    # parsing mechanisms (cli(), yang(), xml()).

    cli_command = 'show platform'
    exclude = ['insert_time']

    def cli(self, output=None):
        """parsing mechanism: cli

        Function cli() defines the cli type output parsing mechanism which
        typically contains 3 steps: exe
        cuting, transforming, returning
        """
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        platform_dict = {}
        sub_dict = {}

        # ----------      C3850    -------------

        # Switch/Stack Mac Address : 0057.d21b.cc00 - Local Mac Address
        p1 = re.compile(
            r'^[Ss]witch\/[Ss]tack +[Mm]ac +[Aa]ddress +\: +'
             '(?P<switch_mac_address>[\w\.]+) *(?P<local>[\w\s\-]+)?$')

        # Mac persistency wait time: Indefinite
        p2 = re.compile(r'^[Mm]ac +persistency +wait +time\: +(?P<mac_persistency_wait_time>[\w\.\:]+)$')

        # Switch  Ports    Model                Serial No.   MAC address     Hw Ver.       Sw Ver. 
        # ------  -----   ---------             -----------  --------------  -------       --------
        #  1       32     WS-C3850-24P-E        FCW1947C0HH  0057.d21b.cc00  V07           16.6.1
        p3 = re.compile(r'^(?P<switch>\d+) +(?P<ports>\d+) +'
                         '(?P<model>[\w\-]+) +(?P<serial_no>\w+) +'
                         '(?P<mac_address>[\w\.\:]+) +'
                         '(?P<hw_ver>\w+) +(?P<sw_ver>[\w\.]+)$')


        #                                     Current
        # Switch#   Role        Priority      State 
        # -------------------------------------------
        # *1       Active          3          Ready
        p4 = re.compile(r'^\*?(?P<switch>\d+) +(?P<role>\w+) +'
                         '(?P<priority>\d+) +(?P<state>[\w\s]+)$')


        # ----------      ASR1K    -------------
        # Chassis type: ASR1006
        p5 = re.compile(r'^[Cc]hassis +type: +(?P<chassis>\w+)$')

        # Slot      Type                State                 Insert time (ago) 
        # --------- ------------------- --------------------- ----------------- 
        # 0         ASR1000-SIP40       ok                    00:33:53
        #  0/0      SPA-1XCHSTM1/OC3    ok                    2d00h
        p6 = re.compile(r'^(?P<slot>\w+)(\/(?P<subslot>\d+))? +(?P<name>\S+) +'
                         '(?P<state>\w+(\, \w+)?) +(?P<insert_time>[\w\.\:]+)$')

        # 4                             unknown               2d00h
        p6_1 = re.compile(r'^(?P<slot>\w+) +(?P<state>\w+(\, \w+)?)'
                         ' +(?P<insert_time>[\w\.\:]+)$')

        # Slot      CPLD Version        Firmware Version                        
        # --------- ------------------- --------------------------------------- 
        # 0         00200800            16.2(1r) 
        p7 = re.compile(r'^(?P<slot>\w+) +(?P<cpld_version>\d+|N\/A) +'
                         '(?P<fireware_ver>[\w\.\(\)\/]+)$')

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                if 'main' not in platform_dict:
                    platform_dict['main'] = {}
                platform_dict['main']['switch_mac_address'] = m.groupdict()['switch_mac_address']
                platform_dict['main']['swstack'] = True
                continue


            m = p2.match(line)
            if m:
                if 'main' not in platform_dict:
                    platform_dict['main'] = {}
                platform_dict['main']['mac_persistency_wait_time'] = m.groupdict()['mac_persistency_wait_time'].lower()
                continue

            m = p3.match(line)
            if m:
                slot = m.groupdict()['switch']
                model = m.groupdict()['model']
                if 'slot' not in platform_dict:
                    platform_dict['slot'] = {}
                if slot not in platform_dict['slot']:
                    platform_dict['slot'][slot] = {}
                if ('WS-C' in model) or ('C9500' in model):
                    lc_type = 'rp'
                else:
                    lc_type = 'other'

                if lc_type not in platform_dict['slot'][slot]:
                    platform_dict['slot'][slot][lc_type] = {}
                if model not in platform_dict['slot'][slot][lc_type]:
                    platform_dict['slot'][slot][lc_type][model] = {}
                platform_dict['slot'][slot][lc_type][model]['hw_ver'] = m.groupdict()['hw_ver']
                platform_dict['slot'][slot][lc_type][model]['mac_address'] = m.groupdict()['mac_address']
                platform_dict['slot'][slot][lc_type][model]['name'] = model
                platform_dict['slot'][slot][lc_type][model]['ports'] = m.groupdict()['ports']
                platform_dict['slot'][slot][lc_type][model]['slot'] = slot
                platform_dict['slot'][slot][lc_type][model]['sn'] = m.groupdict()['serial_no']
                platform_dict['slot'][slot][lc_type][model]['sw_ver'] = m.groupdict()['sw_ver']
                continue

            m = p4.match(line)
            if m:
                slot = m.groupdict()['switch']
                if 'slot' not in platform_dict:
                    continue
                if slot not in platform_dict['slot']:
                    continue

                for key, value in platform_dict['slot'][slot].items():
                    for key, last in value.items():
                        last['swstack_priority'] = m.groupdict()['priority']
                        last['swstack_role'] = m.groupdict()['role']
                        last['state'] = m.groupdict()['state']
                continue

            m = p5.match(line)
            if m:
                if 'main' not in platform_dict:
                    platform_dict['main'] = {}
                platform_dict['main']['chassis'] = m.groupdict()['chassis']
                continue

            m = p6.match(line)
            if m:
                slot = m.groupdict()['slot']
                subslot = m.groupdict()['subslot']
                name = m.groupdict()['name']
                if not name:
                    continue

                # subslot
                if subslot:
                    try:
                        if slot not in platform_dict['slot']:
                            continue
                        for key, value in platform_dict['slot'][slot].items():
                            for key, last in value.items():
                                if 'subslot' not in last:
                                    last['subslot'] = {}
                                if subslot not in last['subslot']:
                                    last['subslot'][subslot] = {}
                                if name not in last['subslot'][subslot]:
                                    last['subslot'][subslot][name] = {}
                                sub_dict = last['subslot'][subslot][name]
                        sub_dict['subslot'] = subslot
                    except Exception:
                        continue
                else:
                    if 'slot' not in platform_dict:
                        platform_dict['slot'] = {}
                    if slot not in platform_dict['slot']:
                        platform_dict['slot'][slot] = {}
                    if re.match(r'^ASR\d+-(\d+T\S+|SIP\d+|X)', name) or ('ISR' in name):
                        if 'R' in slot:
                            lc_type = 'rp'
                        elif re.match(r'^\d+', slot):
                            lc_type = 'lc'
                        else:
                            lc_type = 'other'
                    elif re.match(r'^ASR\d+-RP\d+', name):
                        lc_type = 'rp'
                    elif re.match(r'^CSR\d+V', name):
                        if 'R' in slot:
                            lc_type = 'rp'
                        else:
                            lc_type = 'other'
                    else:
                        lc_type = 'other'

                    if lc_type not in platform_dict['slot'][slot]:
                        platform_dict['slot'][slot][lc_type] = {}

                    if name not in platform_dict['slot'][slot][lc_type]:
                        platform_dict['slot'][slot][lc_type][name] = {}
                    sub_dict = platform_dict['slot'][slot][lc_type][name]
                    sub_dict['slot'] = slot

                sub_dict['name'] = name
                sub_dict['state'] = m.groupdict()['state'].strip()
                sub_dict['insert_time'] = m.groupdict()['insert_time']
                continue

            m = p6_1.match(line)
            if m:                    
                slot = m.groupdict()['slot']
                if 'slot' not in platform_dict:
                    platform_dict['slot'] = {}
                if slot not in platform_dict['slot']:
                    platform_dict['slot'][slot] = {}

                if 'other' not in platform_dict['slot'][slot]:
                    platform_dict['slot'][slot]['other'] ={}
                    platform_dict['slot'][slot]['other'][''] ={}
                platform_dict['slot'][slot]['other']['']['slot'] = slot
                platform_dict['slot'][slot]['other']['']['name'] = ''
                platform_dict['slot'][slot]['other']['']['state'] = m.groupdict()['state']
                platform_dict['slot'][slot]['other']['']['insert_time'] = m.groupdict()['insert_time']
                continue

            m = p7.match(line)
            if m:
                fw_ver = m.groupdict()['fireware_ver']
                cpld_ver = m.groupdict()['cpld_version']
                slot = m.groupdict()['slot']
                if 'slot' not in platform_dict:
                    continue
                if slot not in platform_dict['slot']:
                    continue

                for key, value in platform_dict['slot'][slot].items():
                    for key, last in value.items():
                        last['cpld_ver'] = m.groupdict()['cpld_version']
                        last['fw_ver'] = m.groupdict()['fireware_ver']
                continue

        return platform_dict


