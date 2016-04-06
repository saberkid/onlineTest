from parse_task import *
from core import *


global GRAPHS
global CORES
GRAPHS = []
CORES = []
CORE_NUM = 10

def run_graph(graph):
    global CYCLE
    CYCLE = 0
    finished = 0
    while not finished:
        finished = 1
        CYCLE += 1

        for i in xrange(len(CORES)):
            print "cycle:",CYCLE,'-----------------------'
            if  CORES[i].status:
                print "core%d"%(i+1), CORES[i].status.task_id
            else:
                print "core%d"%(i+1), "vacant"
            if not CORES[i].status:
                if len(CORES[i].task_list):
                    if CORES[i].task_list[0].is_executable():
                        CORES[i].status = CORES[i].task_list[0]
                        del CORES[i].task_list[0]
                        finished = 0
            else:
                finished = 0
                CORES[i].status.runtime += 1
                if CORES[i].status.is_finished():
                    CORES[i].status = None





if __name__ == '__main__':
    global GRAPHS
    global CORES


    for i in range(CORE_NUM):
        CORES.append(core(i+1))
    filename = raw_input("ENTER YOUR TG FILENAME:\n")
    file_object = open(filename)
    try:
        tgff_file = file_object.read()
    finally:
        file_object.close()
    parse_task(tgff_file, CORES, GRAPHS)

    for graph_num in xrange(len(GRAPHS)):
        run_graph(GRAPHS[graph_num])



