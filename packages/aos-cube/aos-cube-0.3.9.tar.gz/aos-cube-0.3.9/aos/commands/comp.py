#!/usr/bin/env python

# Copyright (c) 2016 aos Limited, All Rights Reserved
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied.

import os, sys
import json
import click

from aos.util import *
from aos.managers.comp import CompManager
import configparser

@click.group(short_help="Component Manager")
@click.pass_context
def cli(ctx):
    ctx.obj = CompManager()

# List command
@cli.command("list", short_help="List installed components")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("--json-output", is_flag=True)
@click.option("-r", "--remote", is_flag=True, help="List remote components")
@click.option("-d", "--showduplicates", is_flag=True, help="show all versions of components")
@click.pass_obj
def list_component(cm, components, json_output, remote, showduplicates):
    args = []
    if showduplicates:
        args += ["--showduplicates"]

    if components:
        args += components

    # Clean cached data first
    cm.clean()
    output, err = cm.list(remote, *args)
    click.echo(output)

# Install command
@cli.command("install", short_help="Install components")
@click.argument("components", required=True, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-t", "--check-available", is_flag=True, help="Check if component available before installation")
#@click.option("-s", "--silent", is_flag=True, help="Suppress progress reporting")
#@click.option("--interactive", is_flag=True, help="Allow to make a choice for all prompts")
@click.pass_obj
def install_component(cm, components, check_available):
    cm.install(components, check_available)
    os.chdir(os.path.join(cm.project_dir, OS_NAME))
    update_config_in()

# Uninstall command
@cli.command("uninstall", short_help="Uninstall components")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-a", "--all", is_flag=True, help="Uninstall all components")
@click.option("-f", "--force", is_flag=True, help="Force to uninstall components")
@click.pass_obj
def uninstall_component(cm, components, all, force):
    if all:
        complist = []
        output, err = cm.list(remote=None)
        patten = re.compile(r"(.*\.noarch)\s*(.*)aos\s*installed")
        for line in output.splitlines():
            match = patten.match(line)
            if match:
                complist += [match.group(1)]

        if complist:
            components = complist

    opts = []
    if force:
        opts += ["--nodeps"]

    cm.uninstall(components, *opts)
    os.chdir(os.path.join(cm.project_dir, OS_NAME))
    update_config_in()

# Update command
@cli.command("update", short_help="Update installed components")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-c", "--only-check", is_flag=True, help="Do not update, only check for new version")
@click.option("--json-output", is_flag=True)
@click.pass_obj
def update_component(cm, components, only_check, json_output):
    if only_check:
        output, err = cm.update(components, True, json_output)
        if output.strip():
            click.echo(output)
    else:
        cm.update(components)
        os.chdir(os.path.join(cm.project_dir, OS_NAME))
        update_config_in()

# Search command
@cli.command("search", short_help="Search for a component")
@click.argument("keyword", required=True, nargs=-1)
@click.option("--json-output", is_flag=True)
@click.option("-n", "--name", multiple=True)
@click.option("-a", "--author", multiple=True)
@click.pass_obj
def search_component(cm, keyword, json_output, **filters):
    cm.search(keyword)

# Show command
@cli.command("show", short_help="Show detailed info about a component")
@click.argument("component", required=False, nargs=-1)
@click.option("--json-output", is_flag=True)
@click.option("-r", "--remote", is_flag=True, help="List remote components")
@click.pass_obj
def show_component(cm, json_output, remote, component):
    cm.show(json_output, remote, component)

# Clean command
@cli.command("clean", short_help="Clean cached component metadata")
@click.pass_obj
def clean_metadata(cm):
    cm.clean()
