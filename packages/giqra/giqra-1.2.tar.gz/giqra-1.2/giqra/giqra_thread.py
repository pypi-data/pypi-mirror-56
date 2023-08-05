import threading

threads = {}

def threadfun(f):
    def run_thread(*args, **kwargs):
        stop(f)
        
        event = threading.Event()
        kwargs['_event'] = event
        threads[f] = {
            't': threading.Thread(
                target=f, args=args, kwargs=kwargs, daemon=True),
            'e': event
        }
        threads[f]['t'].start()
    
    return run_thread

def stop(f):
    if f in threads:
        threads[f]['e'].set()
        threads[f]['t'].join(5)
        if threads[f]['t'].is_alive():
            raise RuntimeError(
                'could not stop running thread. function: {}'.format(f))

def stop_all():
    for f in threads:
        stop(f)

def is_alive(f):
    return f in threads and threads[f][t].is_alive()

