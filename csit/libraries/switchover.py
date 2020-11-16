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
from Class_Based_Spirent_Code_Generation import Spirent_L2_Traffic_Gen,Get_Spirent_Config,Create_Spirent_L2_Gen
from get_stream_handle import *
file_path = os.path.dirname(os.path.realpath(__file__))
result = {}


def lag_test(service_obj,spirent_obj,A,B,iter):
    test_result = {}
    # pprint(service_obj.data)
    for node in service_obj.data["site_list"]:
        if node['login']['device_type'] == 'cisco_xr' and 'Bun' in node['main_interface']:
            if node['Lag_test_eligible']:
                service_obj.connect_nodes()
                test_result[node['Node_name']] = {}
                test_result[node['Node_name']]['failure'] = {}
                test_result[node['Node_name']]['repair'] = {}
                input_dict1 = {}
                input_dict1 = service_obj.create_spirent_input_dict_PPS_LAG(**node)
                # pprint(input_dict1)
                switchover_stream_handle = get_switchover_stream_handle(A,B,spirent_obj,**input_dict1)
                # print(switchover_stream_handle)                      
                for i in range(iter):
                    for fail_repair in ['failure','repair']:          
                        print(f"*** iteration {i} , {fail_repair} LAG test")
                        spirent_obj.Generate_Traffic_port_based()
                        time.sleep(spirent_obj.sw_test_duration / 10)
                        output = node['connect_obj'].send_config_set(node[f'{fail_repair}_command'])
                        print(output)
                        node['connect_obj'].commit()
                        node['connect_obj'].exit_config_mode()
                        print("**** waiting for the Traffic to stop")
                        time.sleep(spirent_obj.sw_test_duration + 10)
                        spirent_obj.Stop_Traffic_port_based()
                        spirent_obj.Traffic_Collection()
                        test_result[node['Node_name']][fail_repair][i] = spirent_obj.Validate_Traffic_Result2()
                        spirent_obj.Clear_counters_port_based()
                spirent_obj.delete_streams_clear_counters()
                service_obj.disconnect_nodes()
    pprint(test_result)
    return test_result

def fast_reroute_test(service_obj,spirent_obj,A,B,iter):
    test_result = {}
    # pprint(service_obj.data)
    for node in service_obj.data["site_list"]:
        if node['login']['device_type'] == 'cisco_xr' and node['frr_test_eligible']:
            service_obj.connect_nodes()
            test_result[node['Node_name']] = {}
            test_result[node['Node_name']]['failure'] = {}
            test_result[node['Node_name']]['repair'] = {}
            input_dict2 = {}
            input_dict2 = service_obj.create_spirent_input_dict_PPS_FRR(**node)
            switchover_stream_handle = get_switchover_stream_handle(A,B,spirent_obj,**input_dict2)
            for i in range(iter):
                for fail_repair in ['failure','repair']:          
                    print(f"*** iteration {i} , {fail_repair} Fast Reroute test")
                    spirent_obj.Generate_Traffic_port_based()
                    time.sleep(spirent_obj.sw_test_duration / 10)
                    if fail_repair == "failure":
                        failure_repair_command  = [f"interface {node['frr_primary']}", "shut"]
                    else:
                        failure_repair_command = [f"interface {node['frr_primary']}", "no shut"]
                    print(failure_repair_command)
                    output = node['connect_obj'].send_config_set(failure_repair_command)
                    print(output)
                    node['connect_obj'].commit()
                    node['connect_obj'].exit_config_mode()
                    print("**** waiting for the Traffic to stop")
                    time.sleep(spirent_obj.sw_test_duration + 10)
                    spirent_obj.Stop_Traffic_port_based()
                    spirent_obj.Traffic_Collection()
                    test_result[node['Node_name']][fail_repair][i] = spirent_obj.Validate_Traffic_Result2()
                    spirent_obj.Clear_counters_port_based()
            spirent_obj.delete_streams_clear_counters()
            service_obj.disconnect_nodes()
    pprint(test_result)
    return test_result

def LLF_test(service_obj,spirent_obj,A,B,iter):
    test_result = {}
    list1 = []
    for node in service_obj.data["site_list"]: 
        if 'EP' in node['side']:
            list1.append(node['login']['device_type'])
        else:
            pass
    if (list1 == ['accedian','accedian'] or list1 == ['cisco_xr','cisco_xr'])  and A =="PL" and B == "PL":
        print("**** Eligibile for LLF (spirent break/repair) test")
    else:
        print("**** Not Eligible for LLF (spirent break/repair) Test")
    if A =="PL" and B == "PL":
        service_obj.connect_nodes()
        for port in [0,1]:
            test_result[spirent_obj.port_list[port]] = {}
            for i in range(iter):                
                test_result[spirent_obj.port_list[port]][i+1] = {}
                UNI_Result = {}
                UNI_Result['UNI_failure'] = []
                UNI_Result['UNI_repair'] = []
                for fail_repair in ['UNI_fail','UNI_repair']:
                    test_result[spirent_obj.port_list[port]][i+1][fail_repair] = {}
                    print(f"**** Iteration {i+1}, {fail_repair} test for Spirent port-{spirent_obj.port_list[port]}*********")
                    spirent_obj.Break_Link(port,fail_repair)
                    time.sleep(10)
                    for node in service_obj.data["site_list"]:
                        # VERIFYING CISCO END POINTS.
                        if list1 == ['cisco_xr', 'cisco_xr'] and node['login']['device_type'] == 'cisco_xr':
                            print("**** Checking Port Status on {} at Port {}".format(node['Node_name'],node['main_interface']))
                            output = node['connect_obj'].send_command("show controllers {} | in Operational state".format(node["main_interface"]))
                            print(output)
                            if len(re.findall("Operational state: Down", output)) == 1 and fail_repair == 'UNI_fail':
                                UNI_Result['UNI_failure'].append('down')
                            elif len(re.findall("Operational state: Up", output)) == 1 and fail_repair == 'UNI_repair': 
                                UNI_Result['UNI_repair'].append('UP')                      
                        # VERIFYING ACCEDIAN ENDS
                        elif list1 == ['accedian', 'accedian'] and node['login']['device_type'] == 'accedian':
                            print("**** Checking Port Status on {} and Port {}******".format(node['Node_name'],node['Uni_port']))
                            output = node['connect_obj'].send_command("port show status PORT-{}".format(node["Uni_port"]))
                            print(output)
                            if len(re.findall("Status     : Down", output)) == 1 and fail_repair == 'UNI_fail':
                                    UNI_Result['UNI_failure'].append('down')
                            elif len(re.findall("Status    : Up", output)) == 1 and fail_repair == 'UNI_repair': 
                                UNI_Result['UNI_repair'].append('UP')
                    if UNI_Result['UNI_failure']  == ['down','down'] and fail_repair == 'UNI_fail':
                        test_result[spirent_obj.port_list[port]][i+1][fail_repair] = 'pass'
                    elif UNI_Result['UNI_repair']  == ['UP','UP'] and fail_repair == 'UNI_repair':
                        test_result[spirent_obj.port_list[port]][i+1][fail_repair] = 'pass'
                    else:
                        test_result[spirent_obj.port_list[port]][i+1][fail_repair] = 'fail'                    
        service_obj.disconnect_nodes()           
    # pprint(test_result)
    return test_result

def UNI_LLF_Config(node,state): 
    if state == 'UNI_fail' and node['login']['device_type'] == 'cisco_xr':
        a = "interface {} shutdown".format(node["main_interface"])  
    elif state == 'UNI_repair' and node['login']['device_type'] == 'cisco_xr':
        a = "no interface {} shutdown".format(node["main_interface"])
    elif state == 'UNI_fail' and node['login']['device_type'] == 'accedian':
        a = "port edit PORT-{} state disable".format(node["Uni_port"]) 
    elif state == 'UNI_repair' and node['login']['device_type'] == 'accedian':
        a = "port edit PORT-{} state enable".format(node["Uni_port"])
    UNI_cmd =[a]

    if node['login']['device_type'] == 'cisco_xr':
        output = node['connect_obj'].send_config_set(UNI_cmd)
        print(output)
        node['connect_obj'].commit()
        node['connect_obj'].exit_config_mode()
    elif node['login']['device_type'] == 'accedian':
        output = node['connect_obj'].send_config_set(UNI_cmd, cmd_verify=False)
        print(output)

def LLF_UNI_Test(service_obj,A,B,iter):
    test_result = {}
    list1 = []
    for node in service_obj.data["site_list"]: 
        if 'EP' in node['side']:
            list1.append(node['login']['device_type'])
    if (list1 == ['accedian','accedian'] or list1 == ['cisco_xr','cisco_xr']) and A =="PL" and B == "PL" and service_obj.data['ELAN'] == False:
        print("**** Eligibile for LLF UNI shut/unshut test")
    else:
        print("**** Not Eligible for LLF UNI shut/unshut Test")
    if A =="PL" and B == "PL" and service_obj.data['ELAN'] == False:
        service_obj.connect_nodes()
        for node in service_obj.data["site_list"]:
            if 'EP' in node['side']:
                test_result[node['Node_name']] = {}
            for i in range(iter):
                UNI_Result = {}
                UNI_Result['UNI_fail'] = []
                UNI_Result['UNI_repair'] = []
                if (node['login']['device_type'] == 'cisco_xr' and list1 == ['cisco_xr','cisco_xr']) or (list1 == ['cisco_xr', 'cisco_xr'] and node['login']['device_type'] == 'cisco_xr'):
                    test_result[node['Node_name']][i+1] = {}
                    for fail_repair in ['UNI_fail','UNI_repair']:
                        test_result[node['Node_name']][i+1][fail_repair] = {}
                        print(f"**** Iteration {i+1}, {fail_repair} test for Device-{node['Node_name']}*********")
                        UNI_LLF_Config(node,fail_repair)
                        time.sleep(10)                          
                        for node1 in service_obj.data["site_list"]:
                            # VERIFYING CISCO ENDS
                            if list1 == ['cisco_xr', 'cisco_xr'] and node1['login']['device_type'] == 'cisco_xr':
                                print("**** Checking Port Status on {} at Port {}".format(node1['Node_name'],node1['main_interface']))
                                output = node1['connect_obj'].send_command("show controllers {} | in Operational".format(node1["main_interface"]))
                                print(output)
                                if len(re.findall("Operational state: Down", output)) == 1 and fail_repair == 'UNI_fail':
                                    UNI_Result['UNI_fail'].append('down')
                                elif len(re.findall("Operational state: Up", output)) == 1 and fail_repair == 'UNI_repair': 
                                    UNI_Result['UNI_repair'].append('UP')
                                time.sleep(5)            
                            # VERIFYING ACCEDIAN ENDS
                            elif list1 == ['accedian', 'accedian'] and node1['login']['device_type'] == 'accedian':
                                print("**** Checking Port Status on {} and Port {}******".format(node1['Node_name'],node1['Uni_port']))
                                output = node1['connect_obj'].send_command("port show status PORT-{}".format(node["Uni_port"]))
                                print(output)
                                if len(re.findall("Status     : Down", output)) == 1 and fail_repair == 'UNI_fail':
                                    UNI_Result['UNI_fail'].append('down')
                                elif len(re.findall("Status    : Up", output)) == 1 and fail_repair == 'UNI_repair': 
                                    UNI_Result['UNI_repair'].append('UP')
                        if UNI_Result['UNI_fail']  == ['down','down'] and fail_repair == 'UNI_fail':
                            test_result[node['Node_name']][i+1][fail_repair] ='pass'
                        elif UNI_Result['UNI_repair']  == ['UP','UP'] and fail_repair == 'UNI_repair':
                            test_result[node['Node_name']][i+1][fail_repair] = 'pass'
                        else:
                            test_result[node['Node_name']][i+1][fail_repair] = 'fail'
        service_obj.disconnect_nodes()
        # pprint(test_result)
    return test_result
