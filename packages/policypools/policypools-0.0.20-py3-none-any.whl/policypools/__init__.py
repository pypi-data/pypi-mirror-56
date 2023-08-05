from policypools._process import DiscardOldestProcessPool, DiscardNewestProcessPool, DiscardThisProcessPool
from policypools._thread import DiscardOldestThreadPool, DiscardNewestThreadPool, DiscardThisThreadPool

__all__ = ['Policies', 'PolicyProcessPoolFactory', 'PolicyThreadPoolFactory']


class Policies:
    """
    Class that holds all of the possible policies for the pools
    """

    discard_oldest = "DiscardOldest"
    discard_newest = "DiscardNewest"
    discard_this = "DiscardThis"


class PolicyProcessPoolFactory:
    """
    Factory class for providing different policy process pools
    """

    __policy_mapping = {Policies.discard_oldest: DiscardOldestProcessPool,
                        Policies.discard_newest: DiscardNewestProcessPool,
                        Policies.discard_this: DiscardThisProcessPool}

    @staticmethod
    def get_policy_pool(policy: str, max_q_size: int = 1, max_workers: int = 1):
        """
        Factory method for getting an instance of a process policy pool
        :param policy: the policy to use for the desired pool
        :param max_q_size: the max size of the queue for workers waiting to be run
        :param max_workers: the maximum number of concurrent running workers
        :return: instance of a process policy pool
        :rtype: PolicyProcessPool
        """
        return PolicyProcessPoolFactory.__policy_mapping[policy](max_q_size, max_workers)


class PolicyThreadPoolFactory:
    """
    Factory class for providing different policy thread pools
    """

    __policy_mapping = {Policies.discard_oldest: DiscardOldestThreadPool,
                        Policies.discard_newest: DiscardNewestThreadPool,
                        Policies.discard_this: DiscardThisThreadPool}

    @staticmethod
    def get_policy_pool(policy: str, max_q_size: int = 1, max_workers: int = 1):
        """
        Factory method for getting an instance of a thread policy pool
        :param policy: the policy to use for the desired pool
        :param max_q_size: the max size of the queue for workers waiting to be run
        :param max_workers: the maximum number of concurrent running workers
        :return: instance of a process policy pool
        :rtype: ThreadProcessPool
        """
        return PolicyThreadPoolFactory.__policy_mapping[policy](max_q_size, max_workers)
