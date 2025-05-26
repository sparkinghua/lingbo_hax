import os
import numpy as np
import matplotlib.pyplot as plt

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            value = float(line.strip())
            if value > 60000:
                break
            data.append(value)
    return data

def merge_packets(data):
    merged_data = []
    packet_counts = []
    prev_time = data[0]
    count = 1
    for i in range(1, len(data)):
        if data[i] == prev_time:
            count += 1
        else:
            merged_data.append(prev_time)
            packet_counts.append(count)
            prev_time = data[i]
            count = 1
    merged_data.append(prev_time)
    packet_counts.append(count)
    return merged_data, packet_counts

def calculate_bandwidth(merged_data, packet_counts):
    packet_size = 1500*8   # Convert bytes to bits
    time_diff = np.diff(merged_data)
    total_packets = packet_counts[1:]
    #print('total_packets:', total_packets, '\ntime_diff:', time_diff)
    bandwidth = [packet_size * count / (t / 1000) for count, t in zip(total_packets, time_diff)]  # Convert ms to seconds
    bandwidth = [x / 1000000 for x in bandwidth]  # Convert bits to Mbits
    #print('bandwidth:', bandwidth)
    return bandwidth

def plot_cdf(data):
    sorted_data = np.sort(data)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
    plt.plot(sorted_data, yvals)

    percentiles = np.percentile(sorted_data, [0,5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95,100])
    # print(f"Percentiles for {label}:")
    for i, p in enumerate(percentiles, start=0):
        print(f"{i*5}th Percentile: {p:.2f} Mbits/s")

# 指定数据集文件夹路径
dataset_folder = 'dataset'
# dataset_folder = 'fcc/test'
# 获取文件夹中的所有文件
files = os.listdir(dataset_folder)
bw_list = []
for file in files:
    if file == 'wired24' or file == '12mbps':
        continue
    # if file != 'test_norway_train.vestby-oslo-report.2011-02-11_1729CET.log_1020':
    #     continue
    file_path = os.path.join(dataset_folder, file)
    data = read_data_from_file(file_path)
    merged_data, packet_counts = merge_packets(data)
    bandwidth = calculate_bandwidth(merged_data, packet_counts)
    avg_bandwidth = np.mean(bandwidth)
    bw_list.append(avg_bandwidth)
    if avg_bandwidth > 20:
        print(file, avg_bandwidth)
    # bw_list = bandwidth
    # print(f"Average Bandwidth for {file}: {avg_bandwidth:.2f} Mbits/s")
plot_cdf(bw_list)

plt.xlabel('Bandwidth (Mbits/s)')
plt.ylabel('CDF')
plt.title('Bandwidth CDF')
plt.legend()
plt.grid(True)
save_path = 'bandwidth_cdf.png'
plt.savefig(save_path)