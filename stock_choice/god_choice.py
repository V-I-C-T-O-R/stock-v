import sys,os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
import logging
from stock_choice import work_flow
from stock_choice import settings

#执行时间最好是15点以后，例如15:30
def run():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%b-%d-%H:%M:%S', filename=current_dir + '/logs/info.log')
    logging.getLogger().setLevel(logging.INFO)
    settings.init()
    work_flow.process()

if __name__ == '__main__':
    run()