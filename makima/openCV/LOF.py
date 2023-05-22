import math
from typing import List

class DataNode:
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs
        self.distance = 0.0
        self.k_distance = 0.0
        self.reach_density = 0.0
        self.k_neighbor = []
        self.lof = 0.0

    def set_distance(self, dist):
        self.distance = dist

    def set_k_distance(self, k_dist):
        self.k_distance = k_dist

    def set_reach_density(self, rd):
        self.reach_density = rd

    def set_k_neighbor(self, neighbor):
        self.k_neighbor = neighbor

    def set_lof(self, lof):
        self.lof = lof

class LofComparator:
    def __call__(self, node1, node2):
        return -1 if node1.lof > node2.lof else 1

class LOF:
    INT_K = 9  # 正整数K

    def __init__(self, int_k=9,all_nodes=None):
        self.INT_K = int_k
        self.all_nodes = all_nodes

    def set_k(self, int_k):
        self.INT_K = int_k

    def get_distance(self, node1, node2):
        # 计算两个样本点之间的欧几里得距离
        attrs1 = node1.attrs
        attrs2 = node2.attrs
        sum_val = 0.0
        for i in range(len(attrs1)):
            sum_val += (attrs1[i] - attrs2[i]) ** 2
        return math.sqrt(sum_val)

    def get_kd_and_kn(self, all_nodes):
        # 获取每个点的k-距离（k_distance）和k-领域（k_neighbor）
        node_num = len(all_nodes)
        kd_and_kn_list = []
        for i in range(node_num):
            node1 = all_nodes[i]
            dis_list = []
            for j in range(node_num):
                if i != j:
                    node2 = all_nodes[j]
                    dist = self.get_distance(node1, node2)
                    dis_list.append((j, dist))
            # 按距离从小到大排序
            dis_list = sorted(dis_list, key=lambda x: x[1])
            # 计算第k领域的样本点
            k_neighbor = [all_nodes[item[0]] for item in dis_list[:self.INT_K]]
            node1.set_k_neighbor(k_neighbor)
            # 计算第k距离
            k_distance = dis_list[self.INT_K - 1][1]
            node1.set_k_distance(k_distance)
            kd_and_kn_list.append(node1)
        return kd_and_kn_list

    def cal_reach_dis(self, kd_and_kn_list):
        # 计算每个点的可达距离 reach_dis(p, o) = max{ k_distance(o), distance(p, o) }
        for node in kd_and_kn_list:
            k_neighbor = node.k_neighbor
            for neighbor in k_neighbor:
                k_distance = neighbor.k_distance
                distance = self.get_distance(node, neighbor)
                reach_dis = max(k_distance, distance)
                neighbor.set_reach_dis(reach_dis)

    def cal_reach_density(self, kd_and_kn_list):
        # 计算每个点的可达密度 reach_density(p) = INT_K / sum(reach_dis(p, o))
        for node in kd_and_kn_list:
            k_neighbor = node.k_neighbor
            sum_val = sum([neighbor.reach_dis for neighbor in k_neighbor])
            reach_density = self.INT_K / sum_val
            node.set_reach_density(reach_density)

    def cal_lof(self, kd_and_kn_list):
        # 计算每个点的局部离群点因子 lof(p) = sum(reach_density(o) / reach_density(p)) / INT_K
        for node in kd_and_kn_list:
            k_neighbor = node.k_neighbor
            lof_sum = 0.0
            for neighbor in k_neighbor:
                rd = neighbor.reach_density
                lof_sum += rd / node.reach_density
            lof = lof_sum / self.INT_K
            node.set_lof(lof)

    def get_outlier_nodes(self):
        # 获取离群点列表
        kd_and_kn_list = self.get_kd_and_kn(self.all_nodes)
        self.cal_reach_dis(kd_and_kn_list)
        self.cal_reach_density(kd_and_kn_list)
        self.cal_lof(kd_and_kn_list)
        # 降序排序
        kd_and_kn_list.sort(key=lambda x: x.lof, reverse=True)
        return kd_and_kn_list
