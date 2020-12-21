
##############################################################
#Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
import json
import os
import sys
import yaml
import re
from pprint import pprint
from service import Service


# file_path =  os.path.pardir()
# print file_path
# file_path =  os.path.dirname(os.path.basename(__file__))
file_path = os.path.dirname(os.path.realpath(__file__))


def Get_Spirent_Config():
	data = yaml.load(open(file_path + '/../Topology/Spirent_Test_Topology.yaml'), Loader=yaml.Loader)

	# with open( file_path + 'Spirent_Test_Topology.yaml') as data_file:
	#     data = yaml.load(data_file,Loader=yaml.FullLoader)
	Spirent_Test_Topology = data['Spirent_Test_Topology']
	return (Spirent_Test_Topology)


class Spirent_L2_Traffic_Gen:
	def __init__(self, **kwargs):
		self.port_handle = []
		self.port_list = []


	def Port_Init(self):
		Spirent_Test_Infrastructure = Get_Spirent_Config()
		Number_of_ports = Spirent_Test_Infrastructure['Number_of_ports']
		##############################################################
		# Creation of Spirent Test config with log file
		##############################################################

		test_sta = sth.test_config(
		log='0',
		logfile='SteamConfig-WithPercentageTraffic_logfile',
		vendorlogfile='SteamConfig-WithPercentageTraffic_stcExport',
		vendorlog='0',
		hltlog='1',
		hltlogfile='SteamConfig-WithPercentageTraffic_hltExport',
		hlt2stcmappingfile='SteamConfig-WithPercentageTraffic_hlt2StcMapping',
		hlt2stcmapping='1',
		log_level='0');

		status = test_sta['status']
		if (status == '0'):
			print("run sth.test_config failed")
		##############################################################
		# config the parameters for optimization and parsing
		##############################################################

		test_ctrl_sta = sth.test_control(
			action='enable');

		status = test_ctrl_sta['status']
		if (status == '0'):
			print("run sth.test_control failed")
		##############################################################
		# connect to chassis and reserve port list
		##############################################################
		i = 0
		device = Spirent_Test_Infrastructure['Spirent_Chassis_ip']
		self.traffic_duration = Spirent_Test_Infrastructure['traffic_duration']
		self.sw_test_duration = Spirent_Test_Infrastructure['sw_test_duration']		
		self.rfc_frame_size = Spirent_Test_Infrastructure['rfc_frame_size']
		self.rfc_load_end = Spirent_Test_Infrastructure['rfc_load_end']
		self.rfc_load_start = Spirent_Test_Infrastructure['rfc_load_start']
		self.rfc_load_step = Spirent_Test_Infrastructure['rfc_load_step']
		self.Frame_Size = Spirent_Test_Infrastructure['UC_BC_MC_Frame_Size']
		port_list = list(Spirent_Test_Infrastructure['Port_Values'].values())
		self.port_list = port_list
		port_speed = list(Spirent_Test_Infrastructure['Port_Speed'].values())
		port_mode = list(Spirent_Test_Infrastructure['Port_Phy_Mode'].values())
		self.port_speed1 = port_speed
		self.port_mode1 = port_mode
		intStatus = sth.connect(
		device=device,
		port_list=port_list,
		break_locks=1,
		offline=0)
		status = intStatus['status']
		if (status == '1'):
			for port in port_list:
				self.port_handle.append(intStatus['port_handle'][device][port])
				i += 1
		else:
			print("\nFailed to retrieve port handle!\n")
		#		print(self.port_handle)
		for j in range(len(self.port_list)):
			print("**** {} is {}".format(self.port_handle[j],self.port_list[j]))
		##############################################################
		# Spirent Ports configuration
		##############################################################
		
		for i in range(len(port_list)):
			if port_mode[i] == 'copper':
				int_ret0 = sth.interface_config(
				mode='config',
				port_handle=self.port_handle[i],
				create_host='false',
				intf_mode = 'ethernet',
				phy_mode = port_mode[i],
				scheduling_mode='RATE_BASED',
				port_loadunit='PERCENT_LINE_RATE',
				port_load='50',
				enable_ping_response='0',
				control_plane_mtu='1500',
				speed=port_speed[i],
				autonegotiation = '1',
				duplex = 'full');
				status = int_ret0['status']
				if (status == '0'):
					print("run sth.interface_config failed")
				# print(int_ret0)
			else:
				int_ret0 = sth.interface_config(
				mode='config',
				port_handle=self.port_handle[i],
				create_host='false',
				intf_mode = 'ethernet',
				phy_mode = port_mode[i],
				scheduling_mode='RATE_BASED',
				port_loadunit='PERCENT_LINE_RATE',
				port_load='50',
				enable_ping_response='0',
				control_plane_mtu='1500',
				flow_control='false',
				speed=port_speed[i],
				data_path_mode='normal',
				autonegotiation='1');
				status = int_ret0['status']
				if (status == '0'):
					print("run sth.interface_config failed")
				# print(int_ret0)
	def Spirent_VLAN_Transperancy_Traffic_Testing_For_P2P_Service(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		self.l2_encap = 'ethernet_ii_vlan'
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_tpid = self.vlan_tpid,
			# vlan_id = self.vlan_id,
			vlan_id='1',
			vlan_id_repeat='0',
			vlan_id_mode='increment',
			vlan_id_count='4095',
			vlan_id_step='1',
			vlan_user_priority = self.vlan_user_priority,
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			# mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} , Traffic rate:> {}".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.Rate_Mbps))
		return(streamblock_ret)
	def Spirent_MAC_Transperancy_Traffic_Testing_For_P2P_Service(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			mac_dst_mode='random',
			mac_dst_repeat_count='0',
			mac_dst_count='1',
			mac_src_count='1',
			mac_src_mode='random',
			mac_src_repeat_count='0',
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			# mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		#print("**** {}:> DMAC:> is {} & SMAC:> {} , Traffic rate:> {}".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.Rate_Mbps))
		return(streamblock_ret)
	def Stream_Config_Creation_Without_VLAN_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if self.mac_dst == '01:00:5E:0B:01:02':
			self.Dest_ip = '224.11.1.2'
		else:
			self.Dest_ip = '192.0.0.2{}'.format(src_port_handle_index)
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l3_protocol='ipv4',
			ip_id='0',
			ip_src_addr='192.0.0.1',
			ip_dst_addr=self.Dest_ip,
			ip_ttl='255',
			ip_hdr_length='5',
			ip_protocol='253',
			ip_fragment_offset='0',
			ip_mbz='0',
			ip_precedence='0',
			ip_tos_field='0',
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			# mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} , Traffic rate:> {} Mbps, DIP:> {}".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.Rate_Mbps,self.Dest_ip))
		return(streamblock_ret)
	def Stream_Config_Creation_Without_VLAN_PPS(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'mac_dst_count' in kwargs.keys():
			self.mac_dst_count = kwargs['mac_dst_count']
		else:
			self.mac_dst_count = '1000'
		if 'Rate_PPS' in kwargs.keys():
			self.rate_pps = kwargs['Rate_PPS']
		else:
			self.rate_pps = '1000'
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap = 'ethernet_ii',
			mac_dst_mode = 'increment',
			mac_dst_repeat_count = '0',
			mac_dst_count = self.mac_dst_count,
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps=self.rate_pps,
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} , Traffic rate:> {} PPS".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.rate_pps))
		return(streamblock_ret)
	def Stream_Config_Creation_Single_Tagged_VLAN_PPS(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'mac_dst_count' in kwargs.keys():
			self.mac_dst_count = kwargs['mac_dst_count']
		else:
			self.mac_dst_count = '1000'
		if 'VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		if 'Rate_PPS' in kwargs.keys():
			self.rate_pps = kwargs['Rate_PPS']
		else:
			self.rate_pps = '1000'
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap = 'ethernet_ii_vlan',
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
			mac_dst_mode = 'increment',
			mac_dst_repeat_count = '0',
			mac_dst_count = self.mac_dst_count,
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps=self.rate_pps,
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} , Traffic rate:> {} PPS".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.rate_pps))
		return(streamblock_ret)
	def Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_PPS(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'Outer_VLAN_EtherType' in kwargs.keys():
			self.vlan_outer_tpid = str(int(kwargs['Outer_VLAN_EtherType'], 10))
		else:
			self.vlan_outer_tpid = '34984'
		if 'Outer_VLAN_Priority' in kwargs.keys():
			self.vlan_outer_user_priority = str(int(kwargs['Outer_VLAN_Priority'], 10))
		else:
			self.vlan_outer_user_priority = '2'
		if 'Outer_VLAN_ID' in kwargs.keys():
			self.vlan_id_outer = str(int(kwargs['Outer_VLAN_ID'], 10))
		else:
			self.vlan_id_outer = '1000'
		if 'Inner_VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['Inner_VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'Inner_VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['Inner_VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'Inner_VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		if 'Rate_PPS' in kwargs.keys():
			self.rate_pps = kwargs['Rate_PPS']
		else:
			self.rate_pps = '1000'
		if 'mac_dst_count' in kwargs.keys():
			self.mac_dst_count = kwargs['mac_dst_count']
		else:
			self.mac_dst_count = '1000'
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii_vlan',
			vlan_outer_tpid=self.vlan_outer_tpid,
			vlan_id_outer=self.vlan_id_outer,
			vlan_outer_user_priority = self.vlan_outer_user_priority,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
			mac_dst_mode = 'increment',
			mac_dst_repeat_count = '0',
			mac_dst_count = self.mac_dst_count,
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps=self.rate_pps,
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} , Traffic rate:> {} PPS".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.rate_pps))
		return(streamblock_ret)
	def Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'Outer_VLAN_EtherType' in kwargs.keys():
			self.vlan_outer_tpid = str(int(kwargs['Outer_VLAN_EtherType'], 10))
		else:
			self.vlan_outer_tpid = '34984'
		if 'Outer_VLAN_Priority' in kwargs.keys():
			self.vlan_outer_user_priority = str(int(kwargs['Outer_VLAN_Priority'], 10))
		else:
			self.vlan_outer_user_priority = 2
		if 'Outer_VLAN_ID' in kwargs.keys():
			self.vlan_id_outer = str(int(kwargs['Outer_VLAN_ID'], 10))
		else:
			self.vlan_id_outer = '1000'
		self.l2_encap = 'ethernet_ii_vlan'
		if 'Inner_VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['Inner_VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'Inner_VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['Inner_VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'Inner_VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		if self.mac_dst == '01:00:5E:0B:01:02':
			self.Dest_ip = '224.11.1.2'
		else:
			self.Dest_ip = '192.0.0.2{}'.format(src_port_handle_index)
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_outer_tpid=self.vlan_outer_tpid,
			vlan_id_outer=self.vlan_id_outer,
			vlan_outer_user_priority = self.vlan_outer_user_priority,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
			l3_protocol='ipv4',
			ip_id='0',
			ip_src_addr='192.0.0.1',
			ip_dst_addr=self.Dest_ip,
			ip_ttl='255',
			ip_hdr_length='5',
			ip_protocol='253',
			ip_fragment_offset='0',
			ip_mbz='0',
			ip_precedence='0',
			ip_tos_field='0',
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			#mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} ,VLAN_outer:> {}, VLAN_inner:> {} Traffic rate:> {} Mbps, DIP:> {}".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.vlan_id_outer,self.vlan_id,self.Rate_Mbps,self.Dest_ip))
		return(streamblock_ret)
	def Stream_Config_Creation_Dual_Tagged_VLAN_dot1q_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'Outer_VLAN_EtherType' in kwargs.keys():
			self.vlan_outer_tpid = str(int(kwargs['Outer_VLAN_EtherType'], 10))
		else:
			self.vlan_outer_tpid = '33024'
		if 'Outer_VLAN_Priority' in kwargs.keys():
			self.vlan_outer_user_priority = str(int(kwargs['Outer_VLAN_Priority'], 10))
		else:
			self.vlan_outer_user_priority = 2
		if 'Outer_VLAN_ID' in kwargs.keys():
			self.vlan_id_outer = str(int(kwargs['Outer_VLAN_ID'], 10))
		else:
			self.vlan_id_outer = '1000'
		self.l2_encap = 'ethernet_ii_vlan'
		if 'Inner_VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['Inner_VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'Inner_VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['Inner_VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'Inner_VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_outer_tpid=self.vlan_outer_tpid,
			vlan_id_outer=self.vlan_id_outer,
			vlan_outer_user_priority = self.vlan_outer_user_priority,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
			# l3_protocol='ipv4',
			# ip_id='0',
			# ip_src_addr='192.85.1.2',
			# ip_dst_addr='192.0.0.1',
			# ip_ttl='255',
			# ip_hdr_length='5',
			# ip_protocol='253',
			# ip_fragment_offset='0',
			# ip_mbz='0',
			# ip_precedence='0',
			# ip_tos_field='0',
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			# mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} ,Vlan :>{} Traffic rate:> {}".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.vlan_id,self.Rate_Mbps))
		return(streamblock_ret)
	def Stream_Config_Creation_Single_Tagged_VLAN_Mbps(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Stream_Name' in kwargs.keys():
			self.Stream_Name = kwargs['Stream_Name']
		else:
			self.Stream_Name = 'Test_StreamBlock'
		if 'Frame_Size' in kwargs.keys():
			self.Frame_Size = kwargs['Frame_Size']
		else:
			pass
		if 'MAC_Src' in kwargs.keys():
			self.mac_src = kwargs['MAC_Src']
		else:
			self.mac_src = '00:10:94:00:00:02'
		if 'MAC_Dest' in kwargs.keys():
			self.mac_dst = kwargs['MAC_Dest']
		else:
			self.mac_dst = '00:10:94:00:00:03'
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		if 'VLAN_EtherType' in kwargs.keys():
			self.vlan_tpid = str(int(kwargs['VLAN_EtherType'], 10))
		else:
			self.vlan_tpid = '33024'
		if 'VLAN_ID' in kwargs.keys():
			self.vlan_id = str(int(kwargs['VLAN_ID'], 10))
		else:
			self.vlan_id = '100'
		if 'VLAN_Priority' in kwargs.keys():
			self.vlan_user_priority = str(int(kwargs['Inner_VLAN_Priority'], 10))
		else:
			self.vlan_user_priority = '2'
		self.l2_encap = 'ethernet_ii_vlan'
		if self.mac_dst == '01:00:5E:0B:01:02':
			self.Dest_ip = '224.11.1.2'
		else:
			self.Dest_ip = '192.0.0.2{}'.format(src_port_handle_index)
		streamblock_ret = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap=self.l2_encap,
			vlan_tpid = self.vlan_tpid,
			vlan_id = self.vlan_id,
			vlan_user_priority = self.vlan_user_priority,
			l3_protocol='ipv4',
			ip_id='0',
			ip_src_addr='192.0.0.1',
			ip_dst_addr=self.Dest_ip,
			ip_ttl='255',
			ip_hdr_length='5',
			ip_protocol='253',
			ip_fragment_offset='0',
			ip_mbz='0',
			ip_precedence='0',
			ip_tos_field='0',
			mac_src=self.mac_src,
			mac_dst=self.mac_dst,
			enable_control_plane='0',
			l3_length='4978',
			name=self.Stream_Name,
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size=self.Frame_Size,
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			dest_port_list=self.port_handle[dest_port_handle_index],
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_mbps=self.Rate_Mbps,
			# mac_discovery_gw='192.85.1.1',
			enable_stream='false');
		print("**** {}:> DMAC:> is {} & SMAC:> {} ,VLAN:> {}, Traffic rate:> {} Mbps, DIP:> {}".format(streamblock_ret['stream_id'],self.mac_dst,self.mac_src,self.vlan_id,self.Rate_Mbps,self.Dest_ip))
		return(streamblock_ret)
	def spirent_ccm_stream_2TAG(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		self.vlan_id_outer = str(int(kwargs['Outer_VLAN_ID'], 10))
		self.vlan_id = str(int(kwargs['Inner_VLAN_ID'], 10))
		self.vlan_user_priority = '2'
		self.mac_src = kwargs['MAC_Src']
		ccm_stream_handle = []
		for looper in range(0,8):
			self.mac_dst = '01:80:C2:00:00:3{}'.format(looper)
			if looper == 5:
				md_hex = 'A'
			elif looper == 6:
				md_hex = 'C'
			elif looper == 7:
				md_hex = 'E'
			else:
				md_hex = looper * 2
			streamblock_ret1 = sth.traffic_config (
				mode = 'create',
				port_handle = self.port_handle[src_port_handle_index],
				l2_encap = 'ethernet_ii_vlan',
				mac_src = self.mac_src,
				mac_dst = self.mac_dst,
				vlan_outer_cfi = '0',
				vlan_outer_tpid = '34984',
				vlan_outer_user_priority = '0',
				vlan_id_outer = self.vlan_id_outer,
				vlan_cfi = '0',
				vlan_tpid = '33024',
				vlan_id = self.vlan_id,
				ether_type = '8902',
				vlan_user_priority = self.vlan_user_priority,
				enable_control_plane = '0',
				l3_length = '106',
				name = 'StreamBlock_40',
				fill_type = 'constant',
				fcs_error = '0',
				fill_value  = '0',
				frame_size = '128',
				traffic_state = '1',
				high_speed_result_analysis = '1',
				length_mode = 'fixed',
				tx_port_sending_traffic_to_self_en = 'false',
				disable_signature = '0',
				enable_stream_only_gen = '1',
				pkts_per_burst = '1',
				inter_stream_gap_unit = 'bytes',
				burst_loop_count = '30',
				transmit_mode = 'continuous',
				inter_stream_gap = '12',
				custom_pattern = '{}0010446000000e5000101200d4c455858582d313032333039000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000053ad5e45'.format(md_hex),
				rate_pps='100');
			streamblock_ret1['name'] = 'ccm_MD_level{}'.format(looper)
			print("*** stream name:>{} DMAC:> {} SMAC:>{} Outer_VLAN :> {} Inner_VLAN:> {}".format(streamblock_ret1['name'],self.mac_dst,self.mac_src,self.vlan_id_outer,self.vlan_id))
			ccm_stream_handle.append(streamblock_ret1)
		return(ccm_stream_handle)
	def spirent_ccm_stream_1TAG(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		self.vlan_user_priority = '2'
		self.vlan_id = str(int(kwargs['VLAN_ID'], 10))
		self.mac_src = kwargs['MAC_Src']
		ccm_stream_handle = []
		for looper in range(0,8):
			self.mac_dst = '01:80:C2:00:00:3{}'.format(looper)
			if looper == 5:
				md_hex = 'A'
			elif looper == 6:
				md_hex = 'C'
			elif looper == 7:
				md_hex = 'E'
			else:
				md_hex = looper * 2
			streamblock_ret1 = sth.traffic_config (
				mode = 'create',
				port_handle = self.port_handle[src_port_handle_index],
				l2_encap = 'ethernet_ii_vlan',
				mac_src = self.mac_src,
				mac_dst = self.mac_dst,
				vlan_cfi = '0',
				vlan_tpid = '33024',
				vlan_id = self.vlan_id,
				ether_type = '8902',
				vlan_user_priority = self.vlan_user_priority,
				enable_control_plane = '0',
				l3_length = '106',
				name = 'StreamBlock_40',
				fill_type = 'constant',
				fcs_error = '0',
				fill_value  = '0',
				frame_size = '128',
				traffic_state = '1',
				high_speed_result_analysis = '1',
				length_mode = 'fixed',
				tx_port_sending_traffic_to_self_en = 'false',
				disable_signature = '0',
				enable_stream_only_gen = '1',
				pkts_per_burst = '1',
				inter_stream_gap_unit = 'bytes',
				burst_loop_count = '30',
				transmit_mode = 'continuous',
				inter_stream_gap = '12',
				custom_pattern = '{}0010446000000e5000101200d4c455858582d313032333039000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000053ad5e45'.format(md_hex),
				rate_pps='100');
			streamblock_ret1['name'] = 'ccm_MD_level{}'.format(looper)
			print("*** stream name:>{} DMAC:> {} SMAC:>{} VLAN :> {}".format(streamblock_ret1['name'],self.mac_dst,self.mac_src,self.vlan_id))
			ccm_stream_handle.append(streamblock_ret1)
		return(ccm_stream_handle)
	def spirent_ccm_stream_0TAG(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		self.mac_src = kwargs['MAC_Src']
		ccm_stream_handle = []
		for looper in range(0,8):
			self.mac_dst = '01:80:C2:00:00:3{}'.format(looper)
			if looper == 5:
				md_hex = 'A'
			elif looper == 6:
				md_hex = 'C'
			elif looper == 7:
				md_hex = 'E'
			else:
				md_hex = looper * 2
			streamblock_ret1 = sth.traffic_config (
				mode = 'create',
				port_handle = self.port_handle[src_port_handle_index],
				l2_encap = 'ethernet_ii',
				mac_src = self.mac_src,
				mac_dst = self.mac_dst,
				# vlan_cfi = '0',
				# vlan_tpid = '33024',
				# vlan_id = self.vlan_id,
				ether_type = '8902',
				# vlan_user_priority = self.vlan_user_priority,
				enable_control_plane = '0',
				l3_length = '106',
				name = 'StreamBlock_40',
				fill_type = 'constant',
				fcs_error = '0',
				fill_value  = '0',
				frame_size = '128',
				traffic_state = '1',
				high_speed_result_analysis = '1',
				length_mode = 'fixed',
				tx_port_sending_traffic_to_self_en = 'false',
				disable_signature = '0',
				enable_stream_only_gen = '1',
				pkts_per_burst = '1',
				inter_stream_gap_unit = 'bytes',
				burst_loop_count = '30',
				transmit_mode = 'continuous',
				inter_stream_gap = '12',
				custom_pattern = '{}0010446000000e5000101200d4c455858582d313032333039000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000053ad5e45'.format(md_hex),
				rate_pps='100');
			streamblock_ret1['name'] = 'ccm_MD_level{}'.format(looper)
			print("*** stream name:>{} DMAC:> {} SMAC:>{}".format(streamblock_ret1['name'],self.mac_dst,self.mac_src))
			ccm_stream_handle.append(streamblock_ret1)
		return(ccm_stream_handle)
	def Generate_Stream_Traffic(self,StreamBlock1,StreamBlock2):
		self.StreamBlock1 = StreamBlock1['stream_id']
		self.StreamBlock2 = StreamBlock2['stream_id']
		print(f"**** Starting traffic Second Time for {self.traffic_duration} seconds")
		traffic_ctrl_ret = sth.traffic_control(
			stream_handle=[self.StreamBlock1,self.StreamBlock2],
			action='run',
			duration= self.traffic_duration);
		status = traffic_ctrl_ret['status']
		if (status == '0'):
			print("run sth.traffic_control failed")
		print("**** checking traffic statistic")
	def Generate_Stream_Traffic_timed(self,StreamBlock1,StreamBlock2,time):
		self.StreamBlock1 = StreamBlock1['stream_id']
		self.StreamBlock2 = StreamBlock2['stream_id']
		print(f"**** Starting traffic for {time} seconds")
		traffic_ctrl_ret = sth.traffic_control(
			stream_handle=[self.StreamBlock1,self.StreamBlock2],
			action='run',
			duration= time);
		status = traffic_ctrl_ret['status']
		if (status == '0'):
			print("run sth.traffic_control failed")
		print("**** checking traffic statistic")
	def Generate_Traffic(self):
		#############################################################
		# start traffic
		##############################################################
		print("**** Traffic Started First Time for 10 sec to help mac learning")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle= self.port_handle,
			action='run', duration='8');
		time.sleep(10)
		print("**** Clear stats of 10 seconds traffic")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='clear_stats');
		print("**** 10 seconds before Traffic Started Second Time")
		time.sleep(10)
		print(f"**** Traffic Started Second Time for {self.traffic_duration} seconds")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='run',
			duration=self.traffic_duration);
		status = traffic_ctrl_ret['status']
		if (status == '0'):
			print("run sth.traffic_control failed")
		# print(traffic_ctrl_ret)
		time.sleep(self.traffic_duration + 10)
		print("**** checking traffic statistic")
	def Generate_Traffic_port_based(self):
		print(f"**** Traffic Started for {self.sw_test_duration} seconds")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='run',
			duration=self.sw_test_duration);
	def Stop_Traffic_port_based(self):
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='stop');
		time.sleep(3)
		print("**** checking traffic statistic")
	def Clear_counters_port_based(self):
		print("**** clearing all Stats")
		traffic_ctrl_ret = sth.traffic_control(
			port_handle=self.port_handle,
			action='clear_stats');
		time.sleep(3)
	def Traffic_Collection(self):
		##############################################################
		# start to get the traffic results
		##############################################################
		traffic_results_ret = sth.traffic_stats(
			port_handle=self.port_handle,
			mode='all');
		print("**** Traffic collection completed")
		status = traffic_results_ret['status']
		if (status == '0'):
			print("run sth.traffic_stats failed")
		# pprint(traffic_results_ret)
		self.traffic_result = traffic_results_ret	
	def delete_streams_clear_counters(self):
		traffic_ctrl_ret = sth.traffic_control(
			port_handle= self.port_handle,
			action='reset');
		
		status = traffic_ctrl_ret['status']
		if (status == '0'):
			print("run sth.traffic_control failed")
		# print(traffic_ctrl_ret)
		print("**** All streams and Traffic stats are cleared")		
	def Clean_Up_Spirent(self):
		cleanup_sta = sth.cleanup_session(
			port_handle=self.port_handle,
			clean_dbfile='1');
		print("**** Clean up the spirent Ports, we are done")
	def Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(self,src_port_handle_index,dest_port_handle_index,**kwargs):
		if 'Rate_Mbps' in kwargs.keys():
			self.Rate_Mbps = kwargs['Rate_Mbps']
		else:
			self.Rate_Mbps = 100
		l2CP_stream_handle = []	
		streamblock_ret1 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:02',
			enable_control_plane='0',
			l3_length='537',
			name='LACP_Stream_/Slow_Protocol',
			fill_type='prbs',
			fcs_error='0',
			fill_value='0',
			frame_size='555',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9275');

		status = streamblock_ret1['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret1)
		else:
			print("***** run sth.traffic_config LACP_Stream_/Slow_Protocol successfully")
			streamblock_ret1['name'] = 'LACP_Stream_/Slow_Protocol'
			l2CP_stream_handle.append(streamblock_ret1)

		streamblock_ret2 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			ether_type='888E',
			mac_dst='01:80:C2:00:00:03',
			enable_control_plane='0',
			l3_length='537',
			name='Port_Authentication',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='555',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9164');

		status = streamblock_ret2['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret2)
		else:
			print("***** run sth.traffic_config Port_Authentication successfully")
			streamblock_ret2['name'] = 'Port_Authentication'
			l2CP_stream_handle.append(streamblock_ret2)
		

		streamblock_ret3 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			ether_type='88EE',
			mac_dst='01:80:C2:00:00:07',
			enable_control_plane='0',
			l3_length='537',
			name='E-LMI',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='555',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9148');

		status = streamblock_ret3['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret3)
		else:
			print("***** run sth.traffic_config E-LMI successfully")
			streamblock_ret3['name'] = 'E-LMI'
			l2CP_stream_handle.append(streamblock_ret3)

		streamblock_ret4 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:0E',
			enable_control_plane='0',
			l3_length='982',
			name='LLDP',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='1000',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9199');

		status = streamblock_ret4['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret4)
		else:
			print("***** run sth.traffic_config LLDP successfully")
			streamblock_ret4['name'] = 'LLDP'
			l2CP_stream_handle.append(streamblock_ret4)
		streamblock_ret5 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_dst_mode='increment',
			mac_dst_repeat_count='0',
			mac_dst_count='16',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:20',
			enable_control_plane='0',
			l3_length='537',
			name='GARP/GMRP_StreamBlock',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='555',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9147',
			enable_stream='false');

		status = streamblock_ret5['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret5)
		else:
			print("***** run sth.traffic_config GARP/GMRP_StreamBlock successfully")
			streamblock_ret5['name'] = 'GARP/GMRP'
			l2CP_stream_handle.append(streamblock_ret5)
		

		streamblock_ret6 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:02',
			enable_control_plane='0',
			l3_length='138',
			name='LACP_MARKER',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='156',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9203');

		status = streamblock_ret6['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret6)
		else:
			print("***** run sth.traffic_config LACP_MARKER successfully")
			streamblock_ret6['name'] = 'LACP_MARKER'
			l2CP_stream_handle.append(streamblock_ret6)

		streamblock_ret7 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			enable_control_plane='0',
			l3_length='128',
			name='Link_OAM',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9100');

		status = streamblock_ret7['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret7)
		else:
			print("***** run sth.traffic_config Link_OAM successfully")
			streamblock_ret7['name'] = 'Link_OAM'
			l2CP_stream_handle.append(streamblock_ret7)

		streamblock_ret8 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_8023_snap',
			custom_pattern='ABCDEFABCDEF',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:00:0C:CC:CC:CC',
			llc_control='03',
			llc_ssap='AA',
			llc_dsap='AA',
			snap_oui_id='00000C',
			snap_ether_type='2000',
			enable_control_plane='0',
			l3_length='555',
			name='Cisco_CDP_VTP',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='555',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9116');

		status = streamblock_ret8['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret8)
		else:
			print("***** run sth.traffic_config Cisco_CDP_VTP successfully")
			streamblock_ret8['name'] = 'Cisco_CDP_VTP'
			l2CP_stream_handle.append(streamblock_ret8)

		streamblock_ret9 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			ether_type='0802',
			mac_dst='01:00:0C:CC:CC:CC',
			enable_control_plane='0',
			l3_length='110',
			name='Cicso_Shared_STP_',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9223');

		status = streamblock_ret9['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret9)
		else:
			print("***** run sth.traffic_config Cicso_Shared_STP_ successfully")
			streamblock_ret9['name'] = 'Cicso_Shared_STP_'
			l2CP_stream_handle.append(streamblock_ret9)

		streamblock_ret10 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			l3_protocol='ipv4',
			l4_protocol='igmp',
			igmp_max_response_time='0',
			igmp_version='2',
			igmp_type='16',
			igmp_msg_type='report',
			igmp_group_addr='225.0.0.1',
			ip_id='0',
			ip_src_addr='192.85.1.2',
			ip_dst_addr='224.0.0.1',
			ip_ttl='255',
			ip_hdr_length='5',
			ip_protocol='2',
			ip_fragment_offset='0',
			ip_mbz='0',
			ip_precedence='0',
			ip_tos_field='0',
			mac_src='00:10:94:00:00:02',
			ether_type='0800',
			mac_dst='01:00:5E:00:00:01',
			enable_control_plane='0',
			l3_length='110',
			name='IPV4_IGMP_multicast',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9100',
			mac_discovery_gw='192.85.1.1');

		status = streamblock_ret10['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret10)
		else:
			print("***** run sth.traffic_config IPV4_IGMP_multicast successfully")
			streamblock_ret10['name'] = 'IPV4_IGMP_multicast'
			l2CP_stream_handle.append(streamblock_ret10)

		streamblock_ret11 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			custom_pattern='ABCDEFABCDEF',
			mac_src='00:10:94:00:00:02',
			ether_type='0000',
			mac_dst='01:00:0C:00:00:01',
			enable_control_plane='0',
			l3_length='110',
			name='Cisco_Inter_Switch_Protocol_(ISL)',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9100');

		status = streamblock_ret11['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret11)
		else:
			print("***** run sth.traffic_config Cisco_Inter_Switch_Protocol_(ISL) successfully")
			streamblock_ret11['name'] = 'Cisco_Inter_Switch_Protocol_(ISL)'
			l2CP_stream_handle.append(streamblock_ret11)

		streamblock_ret12 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			ether_type='8902',
			mac_dst='01:80:C2:00:00:35',
			enable_control_plane='0',
			l3_length='537',
			name='SOAM_CCM_Level_5',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='555',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9116');

		status = streamblock_ret12['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret12)
		else:
			print("***** run sth.traffic_config SOAM_CCM_Level_5 successfully")
			streamblock_ret12['name'] = 'SOAM_CCM_Level_5'
			l2CP_stream_handle.append(streamblock_ret12)

		streamblock_ret13 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:0E',
			enable_control_plane='0',
			l3_length='110',
			name='PTP_Delay_Request',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9100');

		status = streamblock_ret13['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret13)
		else:
			print("***** run sth.traffic_config PTP_Delay_Request successfully")
			streamblock_ret13['name'] = 'PTP_Delay_Request'
			l2CP_stream_handle.append(streamblock_ret13)

		streamblock_ret14 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_dst_mode='increment',
			mac_dst_repeat_count='0',
			mac_dst_count='16',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:00',
			enable_control_plane='0',
			l3_length='110',
			name='L2CP_MAC_Frame',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9100',
			enable_stream='false');

		status = streamblock_ret14['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret14)
		else:
			print("***** run sth.traffic_config L2CP_MAC_Frame successfully")
			streamblock_ret14['name'] = 'L2CP_MAC_Frame'
			l2CP_stream_handle.append(streamblock_ret14)

		streamblock_ret15 = sth.traffic_config(
			mode='create',
			port_handle=self.port_handle[src_port_handle_index],
			l2_encap='ethernet_ii',
			mac_src='00:10:94:00:00:02',
			mac_dst='01:80:C2:00:00:DD',
			enable_control_plane='0',
			l3_length='110',
			name='Provider_Bridge_MVRP_Address',
			fill_type='constant',
			fcs_error='0',
			fill_value='0',
			frame_size='128',
			traffic_state='1',
			high_speed_result_analysis='1',
			length_mode='fixed',
			tx_port_sending_traffic_to_self_en='false',
			disable_signature='0',
			enable_stream_only_gen='1',
			pkts_per_burst='1',
			inter_stream_gap_unit='bytes',
			burst_loop_count='30',
			transmit_mode='continuous',
			inter_stream_gap='12',
			rate_pps='9100');

		status = streamblock_ret15['status']
		if (status == '0'):
			print("run sth.traffic_config failed")
			print(streamblock_ret15)
		else:
			print("***** run sth.traffic_config Provider_Bridge_MVRP_Address successfully")
			streamblock_ret15['name'] = 'Provider_Bridge_MVRP_Address'
			l2CP_stream_handle.append(streamblock_ret15)
		
		return l2CP_stream_handle		
	def Validate_Traffic_Result(self):

		# regex to get rx, tx and streams from traffic_results_ret
		RX = '(streamblock\d+)\S+\s+\S+(rx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'
		TX = '(streamblock\d+).*?(tx)\S+\s+\S+total_pkt_bytes\S+\s+\S(\d+)'

		StreamBlock = 'streamblock\d+'

		print('Spirent Ports= ' + str(self.port_list) + '\nTotal Ports= ' + str(len(self.port_list)))
		PortStatus = 'Spirent Ports= ' + str(self.port_list) + '\nTotal Ports= ' + str(len(self.port_list))
		StreamBlock = re.findall(StreamBlock, self.traffic_result)
		print('Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock)))
		StreamStatus = 'Stream Configured= ' + str(StreamBlock) + '\nTotal Streams= ' + str(len(StreamBlock))
		rx_stats = re.findall(RX, self.traffic_result)
		tx_stats = re.findall(TX, self.traffic_result)

		print('rx_stats= ' + str(rx_stats))
		print('tx_stats= ' + str(tx_stats))

		stats = 'rx_stats= ' + str(rx_stats) + '\ntx_stats= ' + str(tx_stats)

		StreamResult = []
		dict5 = {}

		for i in range(0, len(StreamBlock)):
			if rx_stats[i][2] == tx_stats[i][2]:
				print(str(rx_stats[i][0] + ' = pass'))
				StreamResult.append('pass')

			else:
				print(str(rx_stats[i][0] + ' = fail'))
				StreamResult.append('fail')

		print(str(StreamResult))
		#OverallStatus = '\n' + PortStatus + '\n' + StreamStatus + '\n' + stats + '\n' + str(StreamResult)
		OverallStatus = str(StreamResult)
		# print(OverallStatus)

		return OverallStatus
	def Validate_Traffic_Result2(self):
		#print(self.port_handle)
		portA = self.port_handle[0]
		portB = self.port_handle[1]
		deviceA_tx = self.traffic_result[portA]['aggregate']['tx']['pkt_count']
		deviceA_rx = self.traffic_result[portA]['aggregate']['rx']['pkt_count']
		deviceB_tx = self.traffic_result[portB]['aggregate']['tx']['pkt_count']
		deviceB_rx = self.traffic_result[portB]['aggregate']['rx']['pkt_count']
		if deviceA_tx == deviceB_rx and deviceB_tx == deviceA_rx:
			print("***************** Test has Passed")
			print(f"**** No of Tx packets on {self.port_list[0]} are: {deviceA_tx}")
			print(f"**** No of Rx packets on {self.port_list[1]} are: {deviceB_rx}")
			print("*** ")
			print(f"**** No of Tx packets on {self.port_list[1]} are: {deviceB_tx}")
			print(f"**** No of Rx packets on {self.port_list[0]} are: {deviceA_rx}")
			test_result1 = 'pass'
		else:
			print("***************** Test has failed")
			print(f"**** No of Tx packets on {self.port_list[0]} are: {deviceA_tx}")
			print(f"**** No of Rx packets on {self.port_list[1]} are: {deviceB_rx}")
			print("*** ")
			print(f"**** No of Tx packets on {self.port_list[1]} are: {deviceB_tx}")
			print(f"**** No of Rx packets on {self.port_list[0]} are: {deviceA_rx}")
			print(f"**** No of packets dropped from {self.port_list[0]} to {self.port_list[1]} is : {int(deviceA_tx) - int(deviceB_rx) }")
			print(f"**** No of packets dropped from {self.port_list[1]} to {self.port_list[0]} is : {int(deviceB_tx) - int(deviceA_rx) }")
			test_result1 = 'fail'
		
		dict_local = {}
		dict_local[self.port_list[0]] = {}
		dict_local[self.port_list[1]] = {}
		dict_local[self.port_list[0]]['tx'] = deviceA_tx
		dict_local[self.port_list[0]]['rx'] = deviceA_rx
		dict_local[self.port_list[0]]['drop_to_othend'] = int(deviceA_tx) - int(deviceB_rx)		
		dict_local[self.port_list[1]]['tx'] = deviceB_tx
		dict_local[self.port_list[1]]['rx'] = deviceB_rx
		dict_local[self.port_list[1]]['drop_to_othend'] = int(deviceB_tx) - int(deviceA_rx)
		dict_local['result'] = test_result1
		return dict_local
	def rfc_2544_throughput_test(self,StreamBlock1,StreamBlock2):
		self.StreamBlock1 = StreamBlock1['stream_id']
		self.StreamBlock2 = StreamBlock2['stream_id']
		streamblock_handle = [self.StreamBlock1,self.StreamBlock2]

		rfc_cfg0 = sth.test_rfc2544_config (
				mode                                             = 'create',
				test_type                                        = 'throughput',
				streamblock_handle                               = streamblock_handle,
				endpoint_creation                                = '0',
				frame_size_mode                                  = 'custom',
				start_traffic_delay                              = '2',
				resolution                                       = '1',
				learning_mode                                    = 'l2',
				rate_upper_limit                                 = self.rfc_load_end,
				frame_size                                       = self.rfc_frame_size,
				enable_latency_threshold                         = '0',
				enable_detailresults                             = '1',
				rate_step                                        = self.rfc_load_step,
				stagger_start_delay                              = '0',
				learning_frequency                               = 'learn_once',
				enable_jitter_measure                            = '0',
				delay_after_transmission                         = '15',
				ignore_limit                                     = '0',
				enable_cyclic_resolution                         = '1',
				test_duration_mode                               = 'seconds',
				back_off                                         = '50',
				iteration_count                                  = '1',
				rate_lower_limit                                 = '1',
				accept_frame_loss                                = '1',
				test_duration                                    = self.traffic_duration,
				enable_learning                                  = '0',
				latency_type                                     = 'LILO',
				search_mode                                      = 'step',
				enable_seq_threshold                             = '0',
				l3_learning_retry_count                          = '5',
				initial_rate                                     = self.rfc_load_start);

		status = rfc_cfg0['status']
		if (status == '0') :
			print("run sth.test_rfc2544_config failed")
			print(rfc_cfg0)
		else:
			print("***** run sth.test_rfc2544_config successfully")

		#config part is finished

		##############################################################
		#start devices
		##############################################################

		ctrl_ret1 = sth.test_rfc2544_control (
				action                                           = 'run',
				wait                                             = '1');

		status = ctrl_ret1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_control failed")
			print(ctrl_ret1)
		else:
			print("***** run sth.test_rfc2544_control successfully")


		##############################################################
		#start to get the device results
		##############################################################

		results_ret1 = sth.test_rfc2544_info (
				test_type                                        = 'throughput',
				clear_result                                     = '0',
				enable_load_detail                               = '1');

		status = results_ret1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_info failed")
			print(results_ret1)
		else:
			print("***** run sth.test_rfc2544_info successfully, and results is:")
			pprint(results_ret1)


		dict_local = {}
		dict_local['test_duration'] = self.traffic_duration
		Short_result = results_ret1['rfc2544throughput']['load_detail']['iteration']['1']['frame_size']
		Short_result.pop('frame_size_value')
		for k1,v1 in Short_result.items():
			v1.pop('load_value')
			dict_local[k1] = {}
			for k2,v2 in v1.items():
				print (f"***** frame loss percentage for Frame size {k1} and load {k2} is {float(v2['frame_loss'])}")
				if float(v2['frame_loss']) == 0:
					dict_local[k1][k2] = 'pass'
				else:
					dict_local[k1][k2] = 'fail'
		return dict_local
	def rfc_2544_frameloss_test(self,StreamBlock1,StreamBlock2):
		self.StreamBlock1 = StreamBlock1['stream_id']
		self.StreamBlock2 = StreamBlock2['stream_id']
		streamblock_handle = [self.StreamBlock1,self.StreamBlock2]
		rfc_cfg1 = sth.test_rfc2544_config (
				mode                                             = 'create',
				# src_port                                         = ['port1','port2'],
				# dst_port                                         = '',
				test_type                                        = 'fl',
				streamblock_handle                               = streamblock_handle,
				endpoint_creation                                = '0',
				frame_size_mode                                  = 'custom',
				start_traffic_delay                              = '2',
				learning_mode                                    = 'l2',
				frame_size                                       = self.rfc_frame_size,
				enable_detailresults                             = '1',
				load_unit                                        = 'percent_line_rate',
				stagger_start_delay                              = '0',
				learning_frequency                               = 'learn_once',
				enable_jitter_measure                            = '0',
				delay_after_transmission                         = '5',
				load_step                                        = self.rfc_load_step,
				enable_cyclic_resolution                         = '1',
				load_type                                        = 'step',
				test_duration_mode                               = 'seconds',
				iteration_count                                  = '1',
				test_duration                                    = self.traffic_duration,
				load_end                                         = self.rfc_load_start,
				enable_learning                                  = '0',
				latency_type                                     = 'LILO',
				l3_learning_retry_count                          = '5',
				load_start                                       = self.rfc_load_end);

		status = rfc_cfg1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_config failed")
			print(rfc_cfg1)
		else:
			print("***** run sth.test_rfc2544_config successfully")
		
		ctrl_ret1 = sth.test_rfc2544_control (
				action                                           = 'run',
				wait                                             = '1');

		status = ctrl_ret1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_control failed")
			print(ctrl_ret1)
		else:
			print("***** run sth.test_rfc2544_control successfully")

		results_ret1 = sth.test_rfc2544_info (
				test_type                                        = 'fl',
				clear_result                                     = '1');

		status = results_ret1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_info failed")
			print(results_ret1)
		else:
			print("***** run sth.test_rfc2544_info successfully, and results is:")
			pprint(results_ret1)

		dict_local = {}
		dict_local['test_duration'] = self.traffic_duration
		Short_result = results_ret1['rfc2544fl']['detail']['iteration']['1']['frame_size']
		Short_result.pop('frame_size_value')
		for k1,v1 in Short_result.items():
			dict_local[k1] = {}
			for k2,v2 in v1['load'].items():
				print (f"***** frame lost(packets) for Frame size {k1} and load {k2} is {int(v2['frame_lost'])}")
				if int(v2['frame_lost']) == 0:
					dict_local[k1][k2] = 'pass'
				else:
					dict_local[k1][k2] = 'fail'
		return dict_local			
	def rfc_2544_backtoback_test(self,StreamBlock1,StreamBlock2):
		self.StreamBlock1 = StreamBlock1['stream_id']
		self.StreamBlock2 = StreamBlock2['stream_id']
		streamblock_handle = [self.StreamBlock1,self.StreamBlock2]
		rfc_cfg3 = sth.test_rfc2544_config (
				mode                                             = 'create',
				# src_port                                         = ['port1','port2'],
				# dst_port                                         = '',
				test_type                                        = 'b2b',
				streamblock_handle                               = streamblock_handle,
				endpoint_creation                                = '0',
				frame_size_mode                                  = 'custom',
				start_traffic_delay                              = '2',
				learning_mode                                    = 'l2',
				frame_size                                       = self.rfc_frame_size,
				enable_detailresults                             = '1',
				load_unit                                        = 'percent_line_rate',
				stagger_start_delay                              = '0',
				learning_frequency                               = 'learn_once',
				resolution_burst                                 = '100',
				enable_jitter_measure                            = '0',
				delay_after_transmission                         = '5',
				load_step                                        = self.rfc_load_step,
				enable_cyclic_resolution                         = '1',
				load_type                                        = 'step',
				test_duration_mode                               = 'seconds',
				iteration_count                                  = '1',
				accept_frame_loss                                = '0',
				test_duration                                    = self.traffic_duration,
				load_end                                         = self.rfc_load_end,
				enable_learning                                  = '0',
				latency_type                                     = 'LILO',
				l3_learning_retry_count                          = '5',
				load_start                                       = self.rfc_load_start);

		status = rfc_cfg3['status']
		if (status == '0') :
			print("run sth.test_rfc2544_config failed")
			print(rfc_cfg3)
		else:
			print("***** run sth.test_rfc2544_config successfully")

		ctrl_ret1 = sth.test_rfc2544_control (
				action                                           = 'run',
				wait                                             = '1');

		status = ctrl_ret1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_control failed")
			print(ctrl_ret1)
		else:
			print("***** run sth.test_rfc2544_control successfully")

		results_ret4 = sth.test_rfc2544_info (
				test_type                                        = 'b2b',
				clear_result                                     = '1');

		status = results_ret4['status']
		if (status == '0') :
			print("run sth.test_rfc2544_info failed")
			print(results_ret4)
		else:
			print("***** run sth.test_rfc2544_info successfully, and results is:")
			pprint(results_ret4)
	def rfc_2544_latency_test(self,StreamBlock1,StreamBlock2):
		self.StreamBlock1 = StreamBlock1['stream_id']
		self.StreamBlock2 = StreamBlock2['stream_id']
		streamblock_handle = [self.StreamBlock1,self.StreamBlock2]
		rfc_cfg0 = sth.test_rfc2544_config (
				mode                                             = 'create',
				# src_port                                         = ['port1','port2'],
				# dst_port                                         = '',
				test_type                                        = 'latency',
				streamblock_handle                               = streamblock_handle,
				endpoint_creation                                = '0',
				frame_size_mode                                  = 'custom',
				start_traffic_delay                              = '2',
				learning_mode                                    = 'l2',
				frame_size                                       = self.rfc_frame_size,
				enable_detailresults                             = '1',
				load_unit                                        = 'percent_line_rate',
				stagger_start_delay                              = '0',
				learning_frequency                               = 'learn_once',
				enable_jitter_measure                            = '0',
				delay_after_transmission                         = '5',
				load_step                                        = self.rfc_load_step,
				enable_cyclic_resolution                         = '1',
				load_type                                        = 'step',
				test_duration_mode                               = 'seconds',
				iteration_count                                  = '1',
				test_duration                                    = self.traffic_duration,
				load_end                                         = self.rfc_load_end,
				enable_learning                                  = '0',
				latency_type                                     = 'LILO',
				l3_learning_retry_count                          = '5',
				load_start                                       = self.rfc_load_start);

		status = rfc_cfg0['status']
		if (status == '0') :
			print("run sth.test_rfc2544_config failed")
			print(rfc_cfg0)
		else:
			print("***** run sth.test_rfc2544_config successfully")

		ctrl_ret1 = sth.test_rfc2544_control (
				action                                           = 'run',
				wait                                             = '1');

		status = ctrl_ret1['status']
		if (status == '0') :
			print("run sth.test_rfc2544_control failed")
			print(ctrl_ret1)
		else:
			print("***** run sth.test_rfc2544_control successfully")

		results_ret5 = sth.test_rfc2544_info (
				test_type                                        = 'latency',
				clear_result                                     = '1');

		status = results_ret5['status']
		if (status == '0') :
			print("run sth.test_rfc2544_info failed")
			print(results_ret5)
		else:
			print("***** run sth.test_rfc2544_info successfully, and results is:")
			pprint(results_ret5)

		dict_local = {}
		dict_local['test_duration'] = self.traffic_duration
		Short_result = results_ret5['rfc2544latency']['detail']['iteration']['1']['frame_size']
		Short_result.pop('frame_size_value')
		for k1,v1 in Short_result.items():
			dict_local[k1] = {}
			for k2,v2 in v1['load'].items():
				print (f"***** frame loss for Frame size {k1} and load {k2} is {float(v2['latency_avg'])}")
				if float(v2['latency_avg']) < 100:
					dict_local[k1][k2] = 'pass'
				else:
					dict_local[k1][k2] = 'fail'
		return dict_local
	def Break_Link(self, src_port_handle_index, flag):
			if flag == "UNI_fail":
				print(f"**** Shutting Spirent Port {self.port_handle[int(src_port_handle_index)]}")
				sth.interface_control(
					mode='break_link',
					port_handle=self.port_handle[int(src_port_handle_index)]
				)
				time.sleep(5)
			else:
				print(f"**** Repairing Spirent Port {self.port_handle[int(src_port_handle_index)]}")
				sth.interface_control(
					mode='restore_link',
					port_handle=self.port_handle[int(src_port_handle_index)]
				)
				time.sleep(5)
		

def Create_Spirent_L2_Gen(**kwargs):
	Spirent_L2_Gen = Spirent_L2_Traffic_Gen (**kwargs)
	return (Spirent_L2_Gen)

#Spirent_InputParam = {'Ether_Speed':'ether1000', 'Stream_Name':'Spirent_Class_Test', 'Frame_Size':2000, 'Rate_Mbps': 100}

