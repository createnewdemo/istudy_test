# ������ʼ��
import random
import sys

(ALPHA,BETA,RHO,Q)=(1.0,2.0,0.5,100.0)
# ���У���Ⱥ
(city_num,ant_num)=(50,50)
# ��ʼ�����е�λ��
distance_x = [
    178,272,176,171,650,499,267,703,408,437,491,74,532,
    416,626,42,271,359,163,508,229,576,147,560,35,714,
    757,517,64,314,675,690,391,628,87,240,705,699,258,
    428,614,36,360,482,666,597,209,201,492,294]
distance_y = [
    170,395,198,151,242,556,57,401,305,421,267,105,525,
    381,244,330,395,169,141,380,153,442,528,329,232,48,
    498,265,343,120,165,50,433,63,491,275,348,222,288,
    490,213,524,244,114,104,552,70,425,227,331]
# ���о������Ϣ��
distance_graph=[[0.0 for col in range(city_num)] for raw in range(city_num)]
pheromone_graph=[[1.0 for col in range(city_num)] for raw in range(city_num)]
class Ant(object):
# ѡ����һ������
    def __choice_next_city(self):
        next_city=-1
        # �洢ѡ����һ�����еĸ���
        select_city_prob=[0.0 for i in range(city_num)]
        total_prob=0.0
        # ��ȡ��һ�����еĸ���
        for i in range(city_num):
            if self.open_table_city[i]:
                try:
                    # �������
                    select_city_prob[i]=pow(pheromone_graph[self.current_city][i],ALPHA)*pow(distance_graph[self.current_city][i],BETA)
                    total_prob+=select_city_prob[i]
                except ZeroDivisionError as e:
                    print("��ĸΪ0")
                    sys.exit(1)
        # ����ѡ�����
        if total_prob>0.0:
            # ����һ���������
            temp_prob=random.uniform(0.0,total_prob)
            for i in range(city_num):
                # �ִεݼ�
                temp_prob-=select_city_prob[i]
                if temp_prob<0.0:
                    next_city=i
                    break
        if (next_city==-1):
            next_city=random.randint(0,city_num-1)
            while self.open_table_city[next_city]==False:
                next_city=random.randint(0,city_num-1)
        # ����ѡ�����һ�����к�
        return next_city
# ������Ϣ��
    def __update_pheromone_gragh(self):

        # ��ȡÿֻ��������·�������µ���Ϣ��
        temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1,city_num):
                start, end = ant.path[i-1], ant.path[i]
                # ��·���ϵ�ÿ�������ڳ��м�������Ϣ�أ���·���ܾ��뷴��
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]
        # �������г���֮�����Ϣ�أ�����Ϣ��˥�������µ�����Ϣ��
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]