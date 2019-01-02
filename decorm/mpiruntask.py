import mpi4py

from os.path import realpath, dirname, join, exists
from sys import executable, argv
from subprocess import Popen
from decorm.serialization import serialize, deserialize
from decorm.exceptions import ExceptionInfo
from tblib import pickling_support
pickling_support.install()

THIS_SCRIPT = realpath(__file__)
MPIRUN = join(dirname(mpi4py.get_config()['mpicc']), 'mpirun')
if not exists(MPIRUN):
    raise RuntimeError('Cannot find mpirun')


def mpirun_cmds(**kwargs):
    cmds = [MPIRUN]
    for k in kwargs:
        mpiarg = '-{}'.format(str(k).replace('_', '-'))
        cmds.append(mpiarg)
        v = kwargs[k]
        if v is not None:
            cmds.append(str(v))
    cmds.extend([executable, THIS_SCRIPT])
    return cmds


def subprocess_mpirun_task_file(task_file, result_file, **kwargs):
    p = Popen(mpirun_cmds(**kwargs) + [task_file, result_file])
    p.wait()
    if p.returncode != 0:
        raise RuntimeError('Task failed to run')


def mpirun_task_file(task_file, result_file):
    from mpi4py import MPI
    rank = MPI.COMM_WORLD.Get_rank()
    task = deserialize(file=task_file)
    try:
        result = task.compute()
    except:
        result = ExceptionInfo(rank)
    results = MPI.COMM_WORLD.gather(result)
    if rank == 0:
        serialize(results, file=result_file)


if __name__ == '__main__':
    t_file = argv[1]
    r_file = argv[2]
    mpirun_task_file(t_file, r_file)