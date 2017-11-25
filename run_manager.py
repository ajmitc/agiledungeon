from manager.manager import AgileDungeonManager
from client.agiledungeon_client import AgileDungeonClient
import multiprocessing
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument( "-m", "--manager", dest="is_manager", action="store_const", default=False, const=True, help="Run manager" )

def start_manager():
    manager = AgileDungeonManager()
    #p = multiprocessing.Process( target=manager.run )
    #p.start()
    #return p
    manager.run()

def start_client():
    client = AgileDungeonClient()
    #p = multiprocessing.Process( target=client.run )
    #p.start()
    #return p
    client.run()
    
if __name__ == "__main__":
    args = parser.parse_args()
    if args.is_manager:
        start_manager()
    else:
        start_client()
    #manager_process = start_manager()
    #client_process  = start_client()
    #client_process.join()
    #manager_process.join()
    
