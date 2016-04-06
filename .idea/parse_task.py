from random import *


class Graph(object):
    def __init__(self, graph_id):
        self.graph_id = graph_id
        self.task_dic = {}
    # def append_task(self,task):
    #     self.task_list.append(task)


class Arc(object):
    def __init__(self, arc_id, type, task_end):
        self.task_id = arc_id
        self.type = type
        self.task_end = task_end


class Task(object):
    def __init__(self, task_id, type):
        self.task_id = task_id
        self.type = type
        self.child = []
        self.parent = []
        self.runtime_required = 2
        self.runtime = 0
        self.finished = 0

    def is_executable(self):
        if not len(self.parent):
            exe_en = 1
        else:
            exe_en = 1
            for i in xrange(len(self.parent)):
                if not self.parent[i].finished:
                    exe_en = 0
                    break
        return exe_en

    def is_finished(self):
        if self.runtime >= self.runtime_required:
            self.finished = 1
        return  self.finished

def core_allocation(task, CORES):
    core_num = randint(0, 9)
    # while (CORES[core_num].task_len >= 10):
    #     core_num = randint(0, 9)
    CORES[core_num].task_list.append(task)
    CORES[core_num].task_len += 1;


def parse_task(file, CORES, GRAPHS):
    lines = (file.lower().split("\n"))
    graph_num = 0
    for line_num in xrange(len(lines)):
        if lines[line_num] == "":
            continue
        elif lines[line_num].find('@') == 0:
            if lines[line_num].find('task_graph') == 1:
                line_elements = lines[line_num].split()
                GRAPHS.append(Graph(line_elements[1]))
                graph_num += 1
        elif lines[line_num].find('#') == 0:
            continue
        else:
            if graph_num:
                line_elements = lines[line_num].split()
                if line_elements[0] == 'task':
                    task_new = Task(line_elements[1], line_elements[3])
                    GRAPHS[graph_num-1].task_dic[line_elements[1]] = task_new
                    core_allocation(task_new, CORES)

                elif line_elements[0] == 'arc':
                    GRAPHS[graph_num-1].task_dic[line_elements[3]].child.append(GRAPHS[graph_num-1].task_dic[line_elements[5]])
                    GRAPHS[graph_num-1].task_dic[line_elements[5]].parent.append(GRAPHS[graph_num-1].task_dic[line_elements[3]])
    #
    # print GRAPHS[0].task_dic['t0_1'].parent




