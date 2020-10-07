import time

def register(info):
    info.info(name="test module", description='some test module', args=[1, 2, 3, 4])

def run(args):
    time.sleep(1)
    print('run!')
