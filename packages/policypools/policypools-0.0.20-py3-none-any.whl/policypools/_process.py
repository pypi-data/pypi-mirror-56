from abc import ABC
from multiprocessing import Lock, Process
from typing import Dict, Tuple

from policypools.base import PolicyPool

__all__ = ['DiscardNewestProcessPool', 'DiscardOldestProcessPool', 'DiscardThisProcessPool']


class PolicyProcessPool(PolicyPool, ABC):

    def __init__(self, max_q_size: int, max_workers: int):
        super().__init__(lock=Lock(), max_q_size=max_q_size, max_workers=max_workers)

    def submit(self, target=None, name: str = None, args: Tuple = (), kwargs: Dict = None, *, daemon: bool = None):
        name = self._get_unique_name(name, prefix="Process")  # Setting name to be unique since used as key for mapping

        def __wrapped_target(*args, **kwargs):
            """
            The wrapped target is how we look to replace a finished worker with a worker in the worker queue
            :return: None
            """
            target(*args, **kwargs)
            with self._rotation_lock:
                del self._active_workers[name]
                try:
                    worker = self._worker_queue.popleft()
                    self._active_workers[worker.name] = worker
                    self._active_workers[worker.name].start()
                except IndexError:
                    pass

        worker = Process(target=__wrapped_target, args=args, kwargs=kwargs)
        worker.name = name
        if daemon is not None:
            worker.daemon = daemon
        self._execute(name, worker)

    submit.__doc__ = PolicyPool.submit.__doc__


class DiscardNewestProcessPool(PolicyProcessPool):

    def _rotate_workers(self, process: Process):
        self._worker_queue.pop()
        self._worker_queue.append(process)

    _rotate_workers.__doc__ = PolicyPool._rotate_workers.__doc__


class DiscardOldestProcessPool(PolicyProcessPool):

    def _rotate_workers(self, process: Process):
        self._worker_queue.popleft()
        self._worker_queue.append(process)

    _rotate_workers.__doc__ = PolicyPool._rotate_workers.__doc__


class DiscardThisProcessPool(PolicyProcessPool):

    def _rotate_workers(self, process: Process):
        pass

    _rotate_workers.__doc__ = PolicyPool._rotate_workers.__doc__




