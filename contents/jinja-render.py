#!/usr/bin/env python3
# Render a jinja template
# Chris Gadd
# 2021-03-03

import json
import sys
from os import environ
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, exceptions

template_vars={}
template_vars['job'] = {key[7:].lower():value for key,value in environ.items() if key.startswith('RD_JOB_')}
template_vars['node'] = {key[8:].lower():value for key,value in environ.items() if key.startswith('RD_NODE_')}
template_vars['option'] = {key[10:].lower():value for key,value in environ.items() if key.startswith('RD_OPTION_')}
template = environ['RD_CONFIG_TEMPLATE']
output = environ['RD_CONFIG_OUTPUT']
data = environ.get('RD_CONFIG_DATA')
debug = environ['RD_JOB_LOGLEVEL'] == "DEBUG"

if data:
  try:
    template_vars['data'] = json.loads(data)
  except:
    sys.exit("Failed to read additional data (is it valid JSON?): " + data)
else:
  template_vars['data'] = None


def renderTemplate(templateFile, outputFile, template_vars):
  print(f"Rendering {templateFile} as {outputFile}")
  env = Environment(
    loader=FileSystemLoader(Path(templateFile).parent),
    trim_blocks=True,
    lstrip_blocks=True
  )

  try:
    template = env.get_template(Path(templateFile).name)
  except exceptions.TemplateNotFound:
    sys.exit(f"Template not found: {templateFile}")
  rendered_output = template.render(job=template_vars['job'], node=template_vars['node'], option=template_vars['option'], data=template_vars['data'])
  with open(outputFile, "w") as fh:
    fh.write(rendered_output)

if debug:
  print("job context:")
  print(template_vars['job'])
  print("node context:")
  print(template_vars['node'])
  print("option context:")
  print(template_vars['option'])
  print("data context:")
  print(template_vars['data'])

if Path(template).is_dir():
  templateFiles = Path(template).glob("*")
else:
  # filename may have wildcards
  templateFiles = Path(template).parent.glob(Path(template).name)

for templateFile in templateFiles:
  if Path(output).is_dir():
    outputFile = Path(output).joinpath(Path(templateFile).name)
  else:
    outputFile = output
  renderTemplate(templateFile, outputFile, template_vars)
