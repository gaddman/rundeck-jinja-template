Rundeck plugin to parse a Jinja template and insert Rundeck variables.

## Description
Reads a Jinja template and outputs to a new file with the Rundeck variables rendered. Supports the `job`, `node`, and `option` contexts, plus any provided directly.

Tested in RHEL7.

## Requirements
- Python jinja2 module - install with `pip3 install jinja2`

## Installation
Copy `rundeck-jinja-template.zip` to /var/lib/rundeck/libext, or install via the Rundeck web interface.