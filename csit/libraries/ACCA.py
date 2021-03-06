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
from Class_Based_Spirent_Code_Generation import Spirent_L2_Traffic_Gen,Get_Spirent_Config,Create_Spirent_L2_Gen
from get_stream_handle import *
from switchover import *

file_path = os.path.dirname(os.path.realpath(__file__))
result = {}
def onnet_CCM_Y1564_ACCA(A,B):

    print("!"*1)
    print("!"*2)
    print("************** Test {}{} type EP ************* ".format(A,B))
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile_ACCA.yml'),Loader=yaml.Loader)
    qos_dict = yaml.load(open(file_path + '/../Topology/qos_class.yml'),Loader=yaml.Loader)
    dict1.update(qos_dict)
    dict1['site_list'][0]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][1]['port_type'] = '{}-type'.format(B)
    dict1['site_list'][2]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][3]['port_type'] = '{}-type'.format(B)
    my_config = Service(**dict1) ## initialize the object.
    my_config.connect_nodes() ## connect the nodes.
    my_config.gather_facts() ## Update the dictionary with info from Nodes.
    my_config.parse_accedian() ## perse accedian for MEG,MEP index
    my_config.SRTE_Config() ## do SRTE config via H-policy tool & attach the PW class to the Service.
    my_config.Command_Creation() ## create the commands to create and Delete service
    my_config.push_config() ## send the configs to the node.
    test_result,input_dict  = {},{} ## create a empty dictionary to hold results.
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Y1564'] = my_config.Y1564_test() ## perform Y1564 test on Cisco(7.1.2) to Cisco, Acc to Acc, or Acc to Cisco
    # my_config.disconnect_nodes() ## release netmiko connection from NCS and Accedian.
    # input_dict = my_config.create_spirent_input_dict() # create the required dictionary for spirent Traffic.
    # Spirent_L2_Gen = Create_Spirent_L2_Gen() ## create the spirent object.
    # Spirent_L2_Gen.Port_Init() # reserve the port.
    # test_result['ccm_transparency'] = ccm_transparency_test(A,B,my_config,Spirent_L2_Gen,**input_dict) # perform ccm transparency test(same level and lower should not pass)
    # test_result['l2CP'] = l2CP_transparency_test(A,B,my_config,Spirent_L2_Gen,**input_dict) # perform L2CP test for P,PL EP's
    # test_result['UC_traffic'] = UC_BC_MC_test(A,B,'UC',Spirent_L2_Gen,**input_dict) # test Known Unicast Traffic.
    # test_result['BC_traffic'] = UC_BC_MC_test(A,B,'BC',Spirent_L2_Gen,**input_dict) # test Broadcast Traffic.
    # test_result['MC_traffic'] = UC_BC_MC_test(A,B,'MC',Spirent_L2_Gen,**input_dict) # test Multicast Traffic.
    # test_result['LLF_Spi_test'] = LLF_test(my_config,Spirent_L2_Gen,A,B,1) # do LLF test by breaking from spirent side.
    # test_result['LLF_UNI_test'] = LLF_UNI_Test(my_config,A,B,1) # do LLF test by shutting UNI
    # test_result['lag_test'] = lag_test(my_config,Spirent_L2_Gen,A,B,1) # perfrom LAG test with UNI LAG and NNI LAG with Accedian.
    # test_result['frr_test'] = fast_reroute_test(my_config,Spirent_L2_Gen,A,B,1) # perform FRR test ( Local shut)
    # rfc_stream_handle = get_rfc_stream_handle(A,B,Spirent_L2_Gen,**input_dict) 
    # test_result['rfc_fl_test'] = Spirent_L2_Gen.rfc_2544_frameloss_test(rfc_stream_handle[0],rfc_stream_handle[1]) # perform rfc Framelost Test.
    # #test_result['rfc_tput_test'] = Spirent_L2_Gen.rfc_2544_throughput_test(rfc_stream_handle[0],rfc_stream_handle[1])
    # # test_result['rfc_b2b_test'] = Spirent_L2_Gen.rfc_2544_backtoback_test(rfc_stream_handle[0],rfc_stream_handle[1])
    # # test_result['rfc_latency_test'] = Spirent_L2_Gen.rfc_2544_latency_test(rfc_stream_handle[0],rfc_stream_handle[1])
    # Spirent_L2_Gen.delete_streams_clear_counters() # delete all the spirent streams and clear all counters.
    # Spirent_L2_Gen.Clean_Up_Spirent() ## Clean UP Spirent.
    # my_config.connect_nodes()
    # my_config.check_Mac_table()
    test_result['CFM_Stats_ACC'] = my_config.mep_statistic_accedian()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    my_config.disconnect_nodes()
    return test_result

result['FF'] = onnet_CCM_Y1564_ACCA('F','F')
# result['XX'] = onnet_CCM_Y1564_ACCA('X','X')
# result['PP'] = onnet_CCM_Y1564_ACCA('P','P')
# result['PP'] = onnet_CCM_Y1564_ACCA('PL','PL')
# result['XP'] = onnet_CCM_Y1564_ACCA('X','P')
# result['PX'] = onnet_CCM_Y1564_ACCA('P','X')
# result['FY'] = onnet_CCM_Y1564_ACCA('F','Y')
# result['YF'] = onnet_CCM_Y1564_ACCA('Y','F')
# result['YY'] = onnet_CCM_Y1564_ACCA('Y','Y')

pprint(result)