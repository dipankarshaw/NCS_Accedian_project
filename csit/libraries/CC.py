#!/usr/local/bin/python3

import time,json,os,sys,yaml,re,csv,textfsm,datetime
# import json
# import os
# import sys
# import yaml
# import re
from pprint import pprint
from netmiko import Netmiko
# import datetime
from jinja2 import Template
# import csv
# import textfsm
from service import Service
# import yaml
# import ast
from Class_Based_Spirent_Code_Generation import Spirent_L2_Traffic_Gen,Get_Spirent_Config,Create_Spirent_L2_Gen
from get_stream_handle import *
from switchover import *
from ttp import ttp
from Loopback_test import *


file_path = os.path.dirname(os.path.realpath(__file__))
result = {}


def onnet_CC(A,B):

    print("!"*1)
    print("!"*2)
    print("************** Test {}{} type EP ************* ".format(A,B))
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile_CC.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][1]['port_type'] = '{}-type'.format(B)
    my_config = Service(**dict1) ## create the object for service class.
    my_config.connect_nodes() ## connect the nodes.
    my_config.get_Lag_Status() ## get the LAG BW, A/A links, A/S Links.
    my_config.get_frr_status() ## get the LFA towards core.
    my_config.Command_Creation() ## create the commands to create and Delete service
    my_config.push_config() ## send the configs to the node.
    test_result = {} ## create a empty dictionary to hold results.
    # test_result['ccm_status'] = my_config.Validate_ccm()  ## store CCM Test results.
    my_config.disconnect_nodes()
    input_dict = {}
    input_dict = my_config.create_spirent_input_dict() # create the required dictionary for spirent Traffic.
    Spirent_L2_Gen = Create_Spirent_L2_Gen() ## create the spirent object.
    Spirent_L2_Gen.Port_Init() # reserve the port.
    # # test_result['loop_testAB'] = perform_spirent_loop_test(my_config,Spirent_L2_Gen,rfc_stream_handle[0],A,B)
    test_result['LLF_test'] = LLF_test(my_config,Spirent_L2_Gen,A,B,1)
    test_result['LLF_UNI_test'] = LLF_UNI_Test(my_config,A,B,1)
    # test_result['lag_test'] = lag_test(my_config,Spirent_L2_Gen,A,B,1) ## lag_failover_test
    # test_result['frr_test'] = fast_reroute_test(my_config,Spirent_L2_Gen,A,B,1)

    
    rfc_stream_handle = get_rfc_stream_handle(A,B,Spirent_L2_Gen,**input_dict)
    test_result['rfc_tput_test'] = Spirent_L2_Gen.rfc_2544_throughput_test(rfc_stream_handle[0],rfc_stream_handle[1])
    test_result['rfc_fl_test'] = Spirent_L2_Gen.rfc_2544_frameloss_test(rfc_stream_handle[0],rfc_stream_handle[1])
    # test_result['rfc_b2b_test'] = Spirent_L2_Gen.rfc_2544_backtoback_test(rfc_stream_handle[0],rfc_stream_handle[1])
    # test_result['rfc_latency_test'] = Spirent_L2_Gen.rfc_2544_latency_test(rfc_stream_handle[0],rfc_stream_handle[1])
    Spirent_L2_Gen.delete_streams_clear_counters()

    # test UC,MC,BC Traffic, with % of total BW
    
    for tr in ['UC','BC','MC']:
        UC_BC_MC_stream_handle = get_UC_BC_MC_stream_handle(A,B,tr,Spirent_L2_Gen,**input_dict)         
        Spirent_L2_Gen.Generate_Stream_Traffic(UC_BC_MC_stream_handle[0],UC_BC_MC_stream_handle[1]) # will generate Traffic on Stream level
        Spirent_L2_Gen.Traffic_Collection()
        test_result['Spirent_{}_traffic'.format(tr)] = Spirent_L2_Gen.Validate_Traffic_Result2()
        Spirent_L2_Gen.delete_streams_clear_counters()


    ########  test Mac/vlan Transparency for P-P service and L2CP transparency

    if (A == 'P' and B == 'P') or (A == 'PL' and B == 'PL'):
        for mt_vt in ['L2CP']:
            print("**** {} traffic is going to run".format(mt_vt))
            MT_VT_l2CP_stream_handle = get_MT_VT_l2CP_stream_handle(mt_vt,Spirent_L2_Gen,**input_dict)
            for i in range(len(MT_VT_l2CP_stream_handle[0])):
                Spirent_L2_Gen.Generate_Stream_Traffic(MT_VT_l2CP_stream_handle[0][i],MT_VT_l2CP_stream_handle[1][i])
                Spirent_L2_Gen.Traffic_Collection()
                test_result['L2CP_{}_traffic'.format(MT_VT_l2CP_stream_handle[0][i]['name'])] = Spirent_L2_Gen.Validate_Traffic_Result2()
            Spirent_L2_Gen.delete_streams_clear_counters()

    Spirent_L2_Gen.Clean_Up_Spirent()
    my_config.connect_nodes()
    my_config.check_Mac_table()
    test_result['CFM_Stats_cisco'] = my_config.mep_statistic_cisco()
    test_result['Polier_drop'] = my_config.check_QOS_counters_config()
    my_config.delete_config()
    my_config.disconnect_nodes()
    return test_result

def onnet_CC_delete(A,B):

    print("!"*1)
    print("!"*2)
    print("************** Test {}{} type EP ************* ".format(A,B))
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile_CC.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][1]['port_type'] = '{}-type'.format(B)
    test_result = {}
    my_config = Service(**dict1)
    my_config.connect_nodes()
    my_config.delete_config()
    my_config.disconnect_nodes()
    return test_result

result['FF'] = onnet_CC('F','F')
result['LL'] = onnet_CC('PL','PL')  ## not applicable for bundle & ELAN
result['XX'] = onnet_CC('X','X')
result['PP'] = onnet_CC('P','P')
result['XP'] = onnet_CC('X','P')
result['PX'] = onnet_CC('P','X')
result['FY'] = onnet_CC('F','Y')
result['YF'] = onnet_CC('Y','F')
result['YY'] = onnet_CC('Y','Y')

pprint(result)
#print(json.dumps(result,indent=4))