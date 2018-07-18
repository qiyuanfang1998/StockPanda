import threading
import queue

'''
This module is a implementation of python thread, that puts result in a queue
'''

class sThread(threading.Thread):
    '''
    generic thread implementation to run stockinfo functions inside python thread
    '''
    def __init__(self,func,symbol,out_queue,threadID):
        threading.Thread.__init__(self)
        self.func = func
        self.symbol = symbol
        self.out_queue = out_queue
        self.threadID = threadID

    def run(self):
         res_enum = (self.threadID, self.func(self.symbol))
         self.out_queue.put(res_enum)
