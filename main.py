import fileinput

class Viterbi(object):
    def __init__(self, all_nodes ):
        # 선 데이터
        line_nodes = []
        line_num = 0
        # 값 데이터
        value_nodes = []
        value_num = 0
        # 마무리 데이터
        end_nodes = []
        end_num = 0

        for nodes in all_nodes:
            if len(nodes) == 1:
                if line_num == 0:
                    line_num = int(nodes[0])
                elif value_num == 0:
                    value_num = int(nodes[0])
                elif end_num == 0:
                    end_num = int(nodes[0])

        #print(line_num, value_num, end_num)
        # 데이터 구축 완료
        line_nodes = all_nodes[1:line_num+1]
        value_nodes  = all_nodes[line_num+2:line_num+2+value_num]
        end_nodes = all_nodes[-end_num:]
        end_nodes = [nodes[0].split() for nodes in end_nodes]
        # 먼저 맵을 만들어보자.
        line_nodes2 = [l[:2] for l in line_nodes]
        # 처음 맵
        dataset = list(set(sum(line_nodes2, [])))
        del(dataset[dataset.index('<s>')])
        del(dataset[dataset.index('</s>')])
        self.dataset = dataset
        #print(dataset)
         

        
        # 단어 발생 확률 체크
        dict_value_nodes = {}
        for value_node in value_nodes:
            #print(value_node[0])
            try: 
                dict_value_nodes[value_node[0]]
            except:
                dict_value_nodes[value_node[0]] = {value_node[1] : float(value_node[2])}
            else:
                dict_value_nodes[value_node[0]][value_node[1]] = float(value_node[2])
        #print("bo1", dict_value_nodes)
        self.dict_value_nodes = dict_value_nodes
        
        dict_line_nodes = {}
        for line_node in line_nodes:
            try: 
                dict_line_nodes[line_node[0]]
            except:
                dict_line_nodes[line_node[0]] = {line_node[1] : float(line_node[2])}
            else:
                dict_line_nodes[line_node[0]][line_node[1]] = float(line_node[2])

        #print("bo2", dict_line_nodes)
        self.dict_line_nodes = dict_line_nodes
        
        # 변수들
        self.dataset = tuple(self.dataset)

        self.end_num = end_num
        self.line_num = line_num
        self.value_num = value_num

        self.end_nodes = end_nodes 
        self.line_nodes = line_nodes
        self.value_nodes = value_nodes
    
    def graph(self):
        #print(self.dataset)
        #print("self.dict_value_nodes : ",self.dict_value_nodes)
        #print("self.dict_line_nodes : ", self.dict_line_nodes)
        #print(self.end_nodes)
        # 값 전부 가져오기
        G = [{}]
        going = {}
        for end_node in self.end_nodes:
            i = 0
            # 첫번째꺼
            #print("헤", self.dict_line_nodes['<s>'])
            for nodes in self.dict_line_nodes['<s>']:
                G[0][nodes] = self.dict_line_nodes['<s>'][nodes]
                going[nodes] = nodes
            #print(G) 
            #print(going)
            # 나머지꺼
            del(self.dict_line_nodes["<s>"])

            for t,node in enumerate(end_node):
                t = t+1
                if len(end_node) <= t:
                    break
                #print("go : ", node, self.dataset)
                G.append({})
                going2 = {}
                
                # 때려 넣는 부분
                for y in self.dataset:
                    #for da in self.dataset:
                    #    print(y,t,G[t-1][da])
                    #    print(y,t,self.dict_line_nodes[da][y])
                    #    print(y,t,self.dict_value_nodes)
                    #    print(y,t,self.dict_value_nodes[y][end_node[t]])

                    (probability, where) = max((G[t-1][da] * self.dict_line_nodes[da][y] * self.dict_value_nodes[y][end_node[t]], da) for da in self.dataset)
                    #print("gggg", [(going[where])] + [y])
                    #print("ggggg", going2)
                    G[t][y] = probability
                    try:
                        going2[y] = (going[where]) + [y]
                    except:
                        going2[y] = [(going[where])] + [y]
                    #try:
                    #    going2[where]
                    #except:
                    #    going2[where] = [y]
                    #else:
                    #    going2[where].append(y)
                # 기존에 거는 기억 할 필요 없음
                going = going2
            t = t-1
            #for y in self.dataset:
                #print("Y ", y)
                #print("now : ",max((G[t][y], y)))
            (probability, where) = max((G[t][y], y) for y in self.dataset)
            return (going[where]) #[self.dataset])

    def find_moving(self):
        for end_node in self.end_nodes:
            i = 0
            for line in self.line_nodes:
                #print(i)
                if line[1] == "</s>":
                    # A    </s>    0.1
                    # B    </s>    0.1 체크 방법 찾아야지
                    i+=1
                    print((end_node))
                    print("end : ",i, line, float(line[2]))
                    continue
                #print("now : ",line, [(line[1],end_node[i])])
                print("now : ",line, self.dict_value_nodes[(line[1],end_node[i])] * float(line[2]))
                print(line[1],end_node[i], self.dict_value_nodes[(line[1],end_node[i])], float(line[2]))
                # 이제 순서에 맞게 수정만 하면 끝
                # 이 아니라 모든 케이스에 맞게 다시 만들기

    def forward(self):
        print(self.line_nodes)
        print(self.value_nodes)


if __name__ == '__main__':
    # 데이터 받기 시작
    datas = ""
    for data in fileinput.input():
        datas += data
    datas = datas.split("\n")

    # 전체 데이터 받기
    all_nodes = ([data.split("\t") for data in datas])
    
    # 클래스 만들기
    HMM = Viterbi(all_nodes)
    #print("뭐시여")
    print(" ".join(HMM.graph()))
    #HMM.find_moving()