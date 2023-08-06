# Copyright 2019 Comcast Cable Communications Management, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import pyrunner.core.constants as constants
import pyrunner.logger.file as lg
from pyrunner.worker.abstract import Worker

import os, sys
import time
import multiprocessing
import importlib
import traceback
import inspect

from time import gmtime, strftime

class ExecutionNode:
  """
  The 'mechanical' representation of a Worker. The Node is responsible for
  containing the user-defined worker and managing its execution at runtime.
  
  Each Node maintains a reference to it's parent and child nodes, in addition
  to a variety of runtime statistics/state information.
  """
  
  def __init__(self, id=-1, name=None):
    if int(id) < -1:
      raise ValueError('id must be -1 or greater')
    
    # Node Definition
    self._id = int(id)
    self.name = name
    self.worker_dir = None
    self.logfile = None
    self.module = None
    self.worker = None
    self.argv = []
    self.parent_nodes = set()
    self.child_nodes = set()
    
    # Runtime Properties
    self.context = None
    self.attempts = 0
    self._max_attempts = 1
    self._retry_wait_time = 0
    self.must_wait = False
    self.wait_start = 0
    self.start_time = 0
    self.end_time = 0
    self._retcode = multiprocessing.Value('i', 0)
    self.thread = None
    
    return
  
  def __hash__(self):
    return hash(self._id)
  def __eq__(self, other):
    return self._id == other._id
  def __ne__(self, other):
    return not (self._id == other._id)
  def __lt__(self, other):
    return self._id < other._id
  
  
  # ########################## SETTERS + GETTERS ########################## #
  
  def _validate_string(self, name, value, nullable=False):
    try:
      if nullable and value.strip() in ['', None]:
        return
      str(value)
    except:
      raise ValueError('Provided value is not castable to string')
    if not value or not str(value).strip():
      raise ValueError('{} cannot be None, blank, or only spaces'.format(name))
  
  @property
  def id(self):
    return self._id
  @id.setter
  def id(self, value):
    if int(value) < -1:
      raise ValueError('id must be -1 or greater')
    self._id = int(value)
    return self
  
  @property
  def retcode(self):
    return self._retcode.value
  @retcode.setter
  def retcode(self, value):
    if int(value) < -2:
      raise ValueError('retcode must be -2 or greater - received: {}'.format(value))
    self._retcode.value = int(value)
    return self
  
  @property
  def arguments(self):
    return self.argv
  @arguments.setter
  def arguments(self, value):
    self.argv = [ str(x) for x in value ] if value else []
    return self
  
  @property
  def max_attempts(self):
    return getattr(self, '_max_attempts', 1)
  @max_attempts.setter
  def max_attempts(self, value):
    if int(value) < 1:
      raise ValueError('max_attempts must be >= 1')
    self._max_attempts = int(value)
    return self
  
  @property
  def retry_wait_time(self):
    return getattr(self, '_retry_wait_time', 0)
  @retry_wait_time.setter
  def retry_wait_time(self, value):
    if int(value) < 0:
      raise ValueError('retry_wait_time must be >= 0')
    self._retry_wait_time = int(value)
    return self
  
  @property
  def worker_class(self):
    return getattr(importlib.import_module(self.module), self.worker)
  
  # ########################## GENERATE WORKER ########################## #
  
  def generate_worker(self):
    """
    * For backwards compatibility with earlier versions. *
    
    Returns a generic Worker object which extends the user-defined parent
    class. This is done in order to expose the context, logger, and argv
    attributes to the user-defined worker.
    """
    parent_class = self.worker_class
    
    class Worker(parent_class):
      
      def __init__(self, context, retcode, logfile, argv):
        self.context = context
        self._retcode = retcode
        self.logfile = logfile
        self.logger = lg.FileLogger(logfile).open()
        self.argv = argv
        return
      
      @property
      def context(self):
        return getattr(self, '_context', None)
      @context.setter
      def context(self, value):
        self.context = value
        return self
      
      @property
      def retcode(self):
        return self._retcode.value
      @retcode.setter
      def retcode(self, value):
        if int(value) < 0:
          raise ValueError('retcode must be 0 or greater - received: {}'.format(value))
        self._retcode.value = int(value)
        return self
      
      # TODO: Need to deprecate
      def set_return_code(self, value):
        self.retcode = int(value)
        return
      
      def protected_run(self):
        '''Initiate worker class run method and additionally trigger methods if defined
        for other lifecycle steps.'''
        
        # RUN
        try:
          self.retcode = super().run() or self.retcode
        except Exception as e:
          self.logger.error("Uncaught Exception from Worker Thread (RUN)")
          self.logger.error(str(e))
          self.logger.error(traceback.format_exc())
          self.retcode = 901
        
        if not self.retcode:
          # ON SUCCESS
          if parent_class.__dict__.get('on_success'):
            try:
              self.retcode = super().on_success() or self.retcode
            except Exception as e:
              self.logger.error('Uncaught Exception from Worker Thread (ON_SUCCESS)')
              self.logger.error(str(e))
              self.logger.error(traceback.format_exc())
              self.retcode = 902
        else:
          # ON FAIL
          if parent_class.__dict__.get('on_fail'):
            try:
              self.retcode = super().on_fail() or self.retcode
            except Exception as e:
              self.logger.error('Uncaught Exception from Worker Thread (ON_FAIL)')
              self.logger.error(str(e))
              self.logger.error(traceback.format_exc())
              self.retcode = 903
        
        # ON EXIT
        if parent_class.__dict__.get('on_exit'):
          try:
            self.retcode = super().on_exit() or self.retcode
          except Exception as e:
            self.logger.error('Uncaught Exception from Worker Thread (ON_EXIT)')
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())
            self.retcode = 904
        
        self.logger.close()
        
        return
    
    return Worker
  
  # ########################## EXECUTE ########################## #
  
  def execute(self):
    '''Spawn and new process via run method of worker class.'''
    # Return early if retry triggered and wait time has not yet fully elapsed
    if self.must_wait and (time.time() - self.wait_start) < self._retry_wait_time:
      return
    
    self._retcode.value = 0
    self.must_wait = False
    self.attempts += 1
    
    if not self.start_time:
      self.start_time = time.time()
    
    try:
      C = self.worker_class
      if issubclass(C, Worker):
        worker = C(self.context, self._retcode, self.logfile, self.argv)
      else:
        worker = self.generate_worker()(self.context, self._retcode, self.logfile, self.argv)
      self.thread = multiprocessing.Process(target=worker.protected_run, daemon=False)
      self.thread.start()
    except Exception as e:
      logger = lg.FileLogger(self.logfile)
      logger.open()
      logger.error(str(e))
      logger.close()
    
    return
  
  # ########################## POLL ########################## #
  
  def poll(self, wait=False):
    '''Poll the running process for completion and return the worker's return code.'''
    if not self.thread:
      self.retcode = 905
      return self.retcode
    
    running = self.thread.is_alive()
    
    if not running or wait:
      self.thread.join()
      self.end_time = time.time()
      if self.retcode > 0:
        if self.attempts < self.max_attempts:
          logger = lg.FileLogger(self.logfile)
          logger.open(False)
          logger.info('Waiting {} seconds before retrying...'.format(self._retry_wait_time))
          self.must_wait = True
          self.wait_start = time.time()
          logger.restart_message(self.attempts)
          self._retcode.value = -1
    
    return self.retcode if not running or wait else None
  
  def terminate(self):
    if self.thread.is_alive():
      self.thread.terminate()
    return
  
  
  # ########################## MISC ########################## #
  
  def get_node_by_id(self, id):
    if self._id == id:
      return self
    elif not self.child_nodes:
      return None
    else:
      for n in self.child_nodes:
        temp = n.get_node_by_id(id)
        if temp:
          return temp
    return None
  
  def get_node_by_name(self, name):
    if self.name == name:
      return self
    elif not self.child_nodes:
      return None
    else:
      for n in self.child_nodes:
        temp = n.get_node_by_name(name)
        if temp:
          return temp
    return None
  
  def add_parent_node(self, parent):
    self.parent_nodes.add(parent)
    return
  
  def add_child_node(self, child, parent_id_list, named_deps=False):
    if (named_deps and self.name in [ x for x in parent_id_list ]) or (not named_deps and self._id in [ int(x) for x in parent_id_list ]):
      child.add_parent_node(self)
      self.child_nodes.add(child)
    for c in self.child_nodes:
      c.add_child_node(child, parent_id_list, named_deps)
    return
  
  def pretty_print(self, indent=''):
    print('{}{} - {}'.format(indent, self._id, self.name))
    for c in self.child_nodes:
      c.pretty_print('{}  '.format(indent))
    return
  
  def get_elapsed_time(self):
    end_time = self.end_time if self.end_time else time.time()
    
    if self.start_time and end_time and end_time > self.start_time:
      elapsed_time = end_time - self.start_time
      return time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    else:
      return '00:00:00'