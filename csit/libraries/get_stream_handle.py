#!/usr/local/bin/python3

import time
import json
import os
import sys
import yaml
import re
from pprint import pprint
from netmiko import Netmiko
import datetime
from jinja2 import Template
import csv
import textfsm
from service import Service
import yaml
import ast
import Class_Based_Spirent_Code_Generation

file_path = os.path.dirname(os.path.realpath(__file__))
result = {}



def get_rfc_stream_handle(A,B,Spirent_L2_Gen,**input_dict):
    if A == 'Y':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**input_dict['Spirent_2TAG_AZ']['UC'])
    elif A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**input_dict['Spirent_1TAG_AZ']['UC'])
    else:                 
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
    if B == 'Y':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**input_dict['Spirent_2TAG_ZA']['UC'])
    elif B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**input_dict['Spirent_1TAG_ZA']['UC'])
    else:
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    rfc_stream_handle = []
    rfc_stream_handle.append(StreamHandle1)
    rfc_stream_handle.append(StreamHandle2)
    return rfc_stream_handle
def UC_BC_MC_test(A,B,tr,Spirent_L2_Gen,**input_dict):
    UC_BC_MC_result = 'dummy'
    if A == 'Y':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**input_dict['Spirent_2TAG_AZ'][tr])
    elif A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**input_dict['Spirent_1TAG_AZ'][tr])
    else:                 
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(0,1,**input_dict['Spirent_0TAG_AZ'][tr])
    
    if B == 'Y':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**input_dict['Spirent_2TAG_ZA'][tr])
    elif B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**input_dict['Spirent_1TAG_ZA'][tr])
    else:
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(1,0,**input_dict['Spirent_0TAG_ZA'][tr])   
    UC_BC_MC_stream = []
    UC_BC_MC_stream.append(StreamHandle1)
    UC_BC_MC_stream.append(StreamHandle2)         
    Spirent_L2_Gen.Generate_Stream_Traffic(UC_BC_MC_stream[0],UC_BC_MC_stream[1]) # will generate Traffic on Stream level
    Spirent_L2_Gen.Traffic_Collection()
    UC_BC_MC_result = Spirent_L2_Gen.Validate_Traffic_Result2()['result']
    Spirent_L2_Gen.delete_streams_clear_counters()
    return UC_BC_MC_result
def get_switchover_stream_handle(A,B,Spirent_L2_Gen,**input_dict):
    if A == 'Y':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_PPS(0,1,**input_dict['Spirent_2TAG_AZ']['UC'])
    elif A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_PPS(0,1,**input_dict['Spirent_1TAG_AZ']['UC'])
    else:                 
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_PPS(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
    
    if B == 'Y':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_PPS(1,0,**input_dict['Spirent_2TAG_ZA']['UC'])
    elif B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_PPS(1,0,**input_dict['Spirent_1TAG_ZA']['UC'])
    else:
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_PPS(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])   
    switchover_stream_handle = []
    switchover_stream_handle.append(StreamHandle1)
    switchover_stream_handle.append(StreamHandle2)
    return switchover_stream_handle
def ccm_transparency_test(A,B,my_config,Spirent_L2_Gen,**input_dict):
    ccm_result = {}
    if A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.spirent_ccm_stream_1TAG(0,1,**input_dict['Spirent_1TAG_AZ']['UC'])
    elif A == 'P' or A == 'PL':
        StreamHandle1 = Spirent_L2_Gen.spirent_ccm_stream_0TAG(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
    else:
        StreamHandle1 = Spirent_L2_Gen.spirent_ccm_stream_2TAG(0,1,**input_dict['Spirent_2TAG_AZ']['UC'])
    if B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.spirent_ccm_stream_1TAG(1,0,**input_dict['Spirent_1TAG_ZA']['UC'])
    elif B == 'P' or B == 'PL':
        StreamHandle2 = Spirent_L2_Gen.spirent_ccm_stream_0TAG(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    else:
        StreamHandle2 = Spirent_L2_Gen.spirent_ccm_stream_2TAG(1,0,**input_dict['Spirent_2TAG_ZA']['UC'])
    ccm_stream_handle = []
    ccm_stream_handle.append(StreamHandle1)
    ccm_stream_handle.append(StreamHandle2)
    for i in range(len(ccm_stream_handle[0])):
        print(f"*** verify ccm transparancy for {ccm_stream_handle[0][i]['name']} ***")
        Spirent_L2_Gen.Generate_Stream_Traffic_timed(ccm_stream_handle[0][i],ccm_stream_handle[1][i],1)
        Spirent_L2_Gen.Traffic_Collection()
        ccm_result['{}_traffic'.format(ccm_stream_handle[0][i]['name'])] = Spirent_L2_Gen.Validate_Traffic_Result2()['result']
        Spirent_L2_Gen.Clear_counters_port_based()
    Spirent_L2_Gen.delete_streams_clear_counters()
    return ccm_result
def l2CP_transparency_test(A,B,my_config,Spirent_L2_Gen,**input_dict):
    l2cp_result = {}
    if (A == 'P' and B == 'P') or (A == 'PL' and B == 'PL'):
        StreamHandle1 = Spirent_L2_Gen.Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
        StreamHandle2 = Spirent_L2_Gen.Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
        l2CP_stream_handle = []
        l2CP_stream_handle.append(StreamHandle1)
        l2CP_stream_handle.append(StreamHandle2)
        for i in range(len(l2CP_stream_handle[0])):
            print(f"*** verify ccm transparancy for {l2CP_stream_handle[0][i]['name']} ***")
            Spirent_L2_Gen.Generate_Stream_Traffic_timed(l2CP_stream_handle[0][i],l2CP_stream_handle[1][i],1)
            Spirent_L2_Gen.Traffic_Collection()
            l2cp_result['L2CP_{}'.format(l2CP_stream_handle[0][i]['name'])] = Spirent_L2_Gen.Validate_Traffic_Result2()['result']
            Spirent_L2_Gen.Clear_counters_port_based()
        Spirent_L2_Gen.delete_streams_clear_counters()   
    return l2cp_result
def mtu_modification_test(my_config):
    temp_result = {}
    my_config.netconf_set_random_MTU('random')
    temp_result['random_mtu'] = my_config.get_netconf_XC_status()
    my_config.netconf_set_random_MTU('9186')
    temp_result['fix_mtu'] = my_config.get_netconf_XC_status()
    return temp_result
def bgp_shut_unshut_test(my_config):
    my_config.get_netconf_BGP_status() ### Check BGP Status and obtain all BGP neighbors.
    my_config.netconf_shut_bgp_neighbor('true') ### Shut down all BGP Neighbors.
    my_config.get_netconf_BGP_status() ### Check BGP Status and obtain all BGP neighbors.
    my_config.netconf_shut_bgp_neighbor('false') ### No shut down all BGP Neighbors.
    my_config.get_netconf_BGP_status() ### Check BGP Status and obtain all BGP neighbors.


