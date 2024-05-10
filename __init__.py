# based on https://github.com/ivanszl/ComfyUI_Custom_Nodes_AlekPet/blob/master/__init__.py

import os
import importlib.util
import sys
import __main__
import pkgutil
import re

python = sys.executable

# User extension files in custom_nodes
extension_folder = os.path.dirname(os.path.realpath(__file__))

#
DEBUG = False
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
humanReadableTextReg = re.compile('(?<=[a-z])([A-Z])|(?<=[A-Z])([A-Z][a-z]+)')
module_name_cut_version = re.compile("[>=<]")

installed_modules = list(m[1] for m in pkgutil.iter_modules(None))

def log(*text):
  if DEBUG:
    print(''.join(map(str, text)))


def information(datas):
  for info in datas:
    if DEBUG:
      print(info, end="")


def addComfyUINodesToMapping(nodeElement):
    log(f"  -> Find class execute node <{nodeElement}>, add NODE_CLASS_MAPPINGS ...")
    node_folder = os.path.join(extension_folder, nodeElement)
    for f in os.listdir(node_folder):
      ext = os.path.splitext(f)
      # Find files extensions .py
      if os.path.isfile(os.path.join(node_folder, f)) and not f.startswith('__') and ext[1] == '.py' and ext[0] != '__init__':
        # remove extensions .py
        module_without_py = f.replace(ext[1], '')
        # Import module
        spec = importlib.util.spec_from_file_location(module_without_py, os.path.join(node_folder, f))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes_names = list(filter(lambda p: callable(getattr(module, p)) and p.find('Node') != -1, dir(module)))
        for class_module_name in classes_names:
          # Check module
          if class_module_name and class_module_name not in NODE_CLASS_MAPPINGS.keys():
            log(f"    [*] Class node found '{class_module_name}' add to NODE_CLASS_MAPPINGS...")
            NODE_CLASS_MAPPINGS.update({
                class_module_name: getattr(module, class_module_name)
            })
            NODE_DISPLAY_NAME_MAPPINGS.update({
                class_module_name: humanReadableTextReg.sub(" \\1\\2", class_module_name)
            })

def printColorInfo(text, color='\033[92m'):
    CLEAR = '\033[0m'
    print(f"{color}{text}{CLEAR}")


def installNodes():
  log(f"\n-------> Translate Node Installing [DEBUG] <-------")
  printColorInfo(f"### [START] ComfyUI Translate Nodes ###", "\033[1;35m")
  
  for nodeElement in os.listdir(extension_folder):
    if not nodeElement.startswith('__') and nodeElement.endswith('Node') and os.path.isdir(os.path.join(extension_folder, nodeElement)):
      log(f"* Node <{nodeElement}> is found, installing...")
      
      # Loading node info
      printColorInfo(f"Node -> {nodeElement} [Loading]")
      addComfyUINodesToMapping(nodeElement)
          
  printColorInfo(f"### [END] ComfyUI Translate Node ###", "\033[1;35m")

installNodes()