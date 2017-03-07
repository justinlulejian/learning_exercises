#!/usr/bin/env python
"""Provide an interface to abstract away parallel I/O and CPU bound functions.

Usage:
  Create two optional dicts one that will contain IO bound funcs and the other
    CPU bound funcs and their arguments.

    io_tasks = {
        'worker': _WriteAndDeleteFiles,
        'args': [xrange(100), xrange(101, 200), xrange(201, 300)]}
    cpu_tasks = {
        'worker': _GenerateAndIterateOverList, 'args': [10000, 10000]}

    Note: The worker key may only contain one callable, and args key may only
      contain individual elements that match the arguments of the callable. E.g.
      _WriteAndDeleteFiles(cpu_tasks['args'][0])

    thread_proc_helper.ParallelWorkProcessor(
        io_tasks['worker'], io_tasks['args'], cpu_tasks['worker'],
        cpu_tasks['args'])

  There are two example functions that are IO and CPU bound that can be used for
    testing this functionality: _GenerateAndIterateOverList(...) (CPU) and
    _WriteAndDeleteFiles(...). Running 'python thread_proc_helper.py' will run
    these automatically for you and compare the time of parallel vs serial
    execution.
"""

import contextlib
import logging
import multiprocessing
import os
import string
import threading
import time


def ParallelWorkProcessor(io_worker=None, io_worker_args=None, cpu_worker=None,
                          cpu_worker_args=None):
  """Run IO and CPU worker functions and arguments in threads and processes.

  Args:
    io_worker: Function/callable object that takes a single argument.
    io_worker_args: List of arguments to provide io_workers. One element to each
      worker.
    cpu_worker: Function/callable object that takes a single argument.
    cpu_worker_args: List of arguments to provide cpu_workers. One element to
      each worker.
  """
  StartIoTasks(io_worker, io_worker_args)
  StartCpuTasks(cpu_worker, cpu_worker_args)


def StartIoTasks(io_worker, io_worker_args):
  """Begin a thread for each io_worker."""
  logging.basicConfig(
      level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

  for argument in io_worker_args:
    io_thread = threading.Thread(target=io_worker, args=(argument,))
    io_thread.daemon = True
    io_thread.start()
  logging.info('Started all IO threads.')

  all_threads = threading.enumerate()
  all_threads.remove(threading.currentThread())
  for thread in all_threads:
    thread.join()
  logging.info('All %s IO threads have finished.', len(all_threads))


def StartCpuTasks(cpu_worker, cpu_worker_args):
  """Begin a process for each cpu_worker."""
  for argument in cpu_worker_args:
    processor = multiprocessing.Process(target=cpu_worker, args=(argument,))
    processor.start()
  logging.info('Started all CPU processes.')
  processor.join()
  logging.info('Finished all CPU processes.')


def _GenerateAndIterateOverList(list_size):
  """Create two large lists and iterate over them O(N^2).

  Args:
    list_size: Number that the two list size should be.
  """
  large_list = list(xrange(list_size))
  second_large_list = list(xrange(list_size))
  for i in large_list:
    for i in second_large_list:
      continue
    continue
  logging.info('Generated list of size: %s.', list_size)


def _WriteAndDeleteFiles(file_suffixes):
  """Open multiple files, write to them, then delete them.

  Args:
    num_files: Number of files to create and delete.
  """
  file_suffixes = list(file_suffixes)
  for num in file_suffixes:
    filename = 'thread_proc_helper_file%s' % num
    with open(filename, 'a+') as test_file:
      test_file.write(string.printable * 100000)
    os.remove(filename)
  logging.info('Created, wrote, and deleted %s files.', len(file_suffixes))


def _ExampleParallelWorkProcessor():
  logging.basicConfig(
      level=logging.INFO, format='(%(threadName)-10s) %(message)s')
  io_tasks = {
      'worker': _WriteAndDeleteFiles,
      'args': [xrange(100), xrange(101, 200), xrange(201, 300)]}
  cpu_tasks = {
      'worker': _GenerateAndIterateOverList, 'args': [10000, 10000]}
  ParallelWorkProcessor(
      io_tasks['worker'], io_tasks['args'], cpu_tasks['worker'],
      cpu_tasks['args'])


@contextlib.contextmanager
def task_timer(task_name):
  """A timer context manager for timing the execution time of tasks.

  Args:
    task_name: String of the 'task' that is being times by this context manager.
  """
  start_time = time.time()
  yield
  finish_time = time.time()
  logging.info(
      '%s took %s seconds to finish', task_name, finish_time - start_time)


if __name__ == '__main__':
  """Sample of how the module functions."""

  with task_timer('parallel processor tasks'):
    _ExampleParallelWorkProcessor()

  with task_timer('serial process of tasks'):
    for arg in [xrange(100), xrange(101, 200), xrange(201, 300)]:
      _WriteAndDeleteFiles(arg)
    for arg in [10000, 10000]:
      _GenerateAndIterateOverList(arg)
