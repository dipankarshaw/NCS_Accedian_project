import csv
# ep_list = ['P-P','PL-PL','F-F','X-X','X-P','Y-Y','P-X','F-Y','Y-F']
# device_list = ['5501','55A1','540']
# port_type = ['LAG', '10 G_non_lag','1 G_non_lag']
# with open('1564_tc.csv', 'w') as data:
#     csv_writer = csv.writer(data)
#     csv_writer.writerow(['Device Type','port_type','End_point_Type'])
#     for item1 in ep_list:
#         for item2 in port_type:
#             for item3 in device_list:
#                 tc = [item3,item2,item1]
#                 csv_writer.writerow(tc)
csv_dict = {'FF_10000_Mbps': {'Polier_CIR': {'AR15': '9900000', 'AR5': '9990000'},
                   'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_1000_Mbps': {'Polier_CIR': {'AR15': '984375', 'AR5': '1001250'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_100_Mbps': {'Polier_CIR': {'AR15': '98438', 'AR5': '99844'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_2000_Mbps': {'Polier_CIR': {'AR15': '1968750', 'AR5': '2002500'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_200_Mbps': {'Polier_CIR': {'AR15': '196875', 'AR5': '199688'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_3000_Mbps': {'Polier_CIR': {'AR15': '2962500', 'AR5': '3015000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_300_Mbps': {'Polier_CIR': {'AR15': '295313', 'AR5': '300938'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_4000_Mbps': {'Polier_CIR': {'AR15': '3937500', 'AR5': '4005000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_400_Mbps': {'Polier_CIR': {'AR15': '393750', 'AR5': '399375'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_5000_Mbps': {'Polier_CIR': {'AR15': '4950000', 'AR5': '4995000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_500_Mbps': {'Polier_CIR': {'AR15': '492188', 'AR5': '500625'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_6000_Mbps': {'Polier_CIR': {'AR15': '5925000', 'AR5': '6030000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_600_Mbps': {'Polier_CIR': {'AR15': '590625', 'AR5': '601875'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_7000_Mbps': {'Polier_CIR': {'AR15': '6900000', 'AR5': '7020000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_700_Mbps': {'Polier_CIR': {'AR15': '693750', 'AR5': '697500'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_8000_Mbps': {'Polier_CIR': {'AR15': '7875000', 'AR5': '8010000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_800_Mbps': {'Polier_CIR': {'AR15': '787500', 'AR5': '798750'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_9000_Mbps': {'Polier_CIR': {'AR15': '8850000', 'AR5': '9000000'},
                  'Polier_drop': {'AR15': 0, 'AR5': 0}},
 'FF_900_Mbps': {'Polier_CIR': {'AR15': '890625', 'AR5': '900000'},
                 'Polier_drop': {'AR15': 0, 'AR5': 0}}}











node = 'AR3'
node_UNI = 'TenGigE0/0/0/15'
node2 = 'AR5'
node2_UNI = 'TenGigE0/0/0/41'
# with open('1564_tc.csv', 'w') as data:
#     csv_writer = csv.writer(data)
#     csv_writer.writerow(['DUT','EP_Type','L1_result','L1_CIR_TX','L1_CIR_FL','l2_result','L2_CIR_TX','L2_CIR_FL',f"Pol_drop_{node}",f"Pol_drop_{node2}"])
#     for k1, v1 in csv_dict.items():
#         for k2, v2 in v1.items():
#             if k2 == 'Y1564':
#                 list_send = [node,k1, v2[node]['L1'],v2[node]['L1_CIR_TX'],v2[node]['L1_CIR_FL'],v2[node]['L2'],v2[node]['L2_CIR_TX'],v2[node]['L2_CIR_FL'],v1['Polier_drop'][node],v1['Polier_drop'][node2]]
#                 csv_writer.writerow(list_send)
# with open('1564_tc.csv', 'w') as data:
#     csv_writer = csv.writer(data)
#     csv_writer.writerow(['DUT','EP_Type','l2_result','L2_CIR_TX','L2_CIR_FL',f"Pol_drop_{node}",f"Pol_drop_{node2}",f"voq_stat_{node}",f"voq_stat_{node2}"])
#     for k1, v1 in csv_dict.items():
#         for k2, v2 in v1.items():
#             if k2 == 'Y1564':
#                 list_send = [node,k1,v2[node]['L2'],v2[node]['L2_CIR_TX'],v2[node]['L2_CIR_FL'],v1['Polier_drop'][node],v1['Polier_drop'][node2],v1['voq_stat'][node][node_UNI]['TC_2']['rx_pkts'],v1['voq_stat'][node2][node2_UNI]['TC_2']['rx_pkts']]
#                 csv_writer.writerow(list_send)

with open('1.csv','w') as data:
        csv_writer = csv.writer(data)
        csv_writer.writerow(['UNI Speed','service_BW','QOS_type','AR15_CIR','AR5_CIR'])
        for k1,v1 in csv_dict.items():
                list_send = ['1G',k1,'Business2',v1['Polier_CIR']['AR15'],v1['Polier_CIR']['AR5']]
                csv_writer.writerow(list_send)



# v1['Polier_drop'][node],v1['Polier_drop'][node2]            