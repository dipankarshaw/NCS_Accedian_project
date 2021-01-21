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
csv_dict = {'FF_10000_Mbps_Business1_Percent': {'Polier_drop': {'AR3': 16171800, 'AR5': 2},
                                     'Y1564': {'AR3': {'L2': 'fail',
                                                       'L2_CIR_FL': '16171787',
                                                       'L2_CIR_TX': '43234071',
                                                       'L2_EIR_FL': '0',
                                                       'L2_EIR_TX': '0'},
                                               'AR5': 'Not_supported'},
                                     'ccm_status': {'AR3': 'pass',
                                                    'AR5': 'pass'}},
 'FF_10000_Mbps_Business2_Percent': {'Polier_drop': {'AR3': 103327,
                                                     'AR5': 10947},
                                     'Y1564': {'AR3': {'L2': 'fail',
                                                       'L2_CIR_FL': '114269',
                                                       'L2_CIR_TX': '43233824',
                                                       'L2_EIR_FL': '0',
                                                       'L2_EIR_TX': '0'},
                                               'AR5': 'Not_supported'},
                                     'ccm_status': {'AR3': 'pass',
                                                    'AR5': 'pass'}},
 'FF_10000_Mbps_Business3_Percent': {'Polier_drop': {'AR3': 99917,
                                                     'AR5': 11193},
                                     'Y1564': {'AR3': {'L2': 'fail',
                                                       'L2_CIR_FL': '111105',
                                                       'L2_CIR_TX': '43233817',
                                                       'L2_EIR_FL': '0',
                                                       'L2_EIR_TX': '0'},
                                               'AR5': 'Not_supported'},
                                     'ccm_status': {'AR3': 'pass',
                                                    'AR5': 'pass'}},
 'FF_10000_Mbps_Premium_Percent': {'Polier_drop': {'AR3': 16172282, 'AR5': 0},
                                   'Y1564': {'AR3': {'L2': 'fail',
                                                     'L2_CIR_FL': '16172269',
                                                     'L2_CIR_TX': '43233808',
                                                     'L2_EIR_FL': '0',
                                                     'L2_EIR_TX': '0'},
                                             'AR5': 'Not_supported'},
                                   'ccm_status': {'AR3': 'pass',
                                                  'AR5': 'pass'}},
 'FF_10000_Mbps_Standard_Percent': {'Polier_drop': {'AR3': 178659,
                                                    'AR5': 14675},
                                    'Y1564': {'AR3': {'L2': 'fail',
                                                      'L2_CIR_FL': '193330',
                                                      'L2_CIR_TX': '43233978',
                                                      'L2_EIR_FL': '0',
                                                      'L2_EIR_TX': '0'},
                                              'AR5': 'Not_supported'},
                                    'ccm_status': {'AR3': 'pass',
                                                   'AR5': 'pass'}}}










node = 'AR3'
node2 = 'AR5'
# with open('1564_tc.csv', 'w') as data:
#     csv_writer = csv.writer(data)
#     csv_writer.writerow(['DUT','EP_Type','L1_result','L1_CIR_TX','L1_CIR_FL','l2_result','L2_CIR_TX','L2_CIR_FL',f"Pol_drop_{node}",f"Pol_drop_{node2}"])
#     for k1, v1 in csv_dict.items():
#         for k2, v2 in v1.items():
#             if k2 == 'Y1564':
#                 list_send = [node,k1, v2[node]['L1'],v2[node]['L1_CIR_TX'],v2[node]['L1_CIR_FL'],v2[node]['L2'],v2[node]['L2_CIR_TX'],v2[node]['L2_CIR_FL'],v1['Polier_drop'][node],v1['Polier_drop'][node2]]
#                 csv_writer.writerow(list_send)
with open('1564_tc.csv', 'w') as data:
    csv_writer = csv.writer(data)
    csv_writer.writerow(['DUT','EP_Type','l2_result','L2_CIR_TX','L2_CIR_FL',f"Pol_drop_{node}",f"Pol_drop_{node2}"])
    for k1, v1 in csv_dict.items():
        for k2, v2 in v1.items():
            if k2 == 'Y1564':
                list_send = [node,k1,v2[node]['L2'],v2[node]['L2_CIR_TX'],v2[node]['L2_CIR_FL'],v1['Polier_drop'][node],v1['Polier_drop'][node2]]
                csv_writer.writerow(list_send)
            