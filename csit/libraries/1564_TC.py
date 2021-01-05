import csv
ep_list = ['P-P','PL-PL','F-F','X-X','X-P','Y-Y','P-X','F-Y','Y-F']
device_list = ['5501','55A1','540']
port_type = ['LAG', '10 G_non_lag','1 G_non_lag']
with open('1564_tc.csv', 'w') as data:
    csv_writer = csv.writer(data)
    csv_writer.writerow(['Device Type','port_type','End_point_Type'])
    for item1 in ep_list:
        for item2 in port_type:
            for item3 in device_list:
                tc = [item3,item2,item1]
                csv_writer.writerow(tc)