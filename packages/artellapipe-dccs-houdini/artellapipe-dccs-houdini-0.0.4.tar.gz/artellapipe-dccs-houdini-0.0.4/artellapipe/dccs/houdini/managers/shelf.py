#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains manager that handles Artella Project Houdini Shelf
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import logging

from six import string_types

import tpDccLib as tp
from tpPyUtils import decorators

if tp.is_houdini():
    from tpHoudiniLib.core import gui

import artellapipe.register
from artellapipe.managers import shelf as core_shelf
from artellapipe.utils import resource

LOGGER = logging.getLogger()


class ArtellaHoudiniShelfManager(core_shelf.ArtellaShelfManager, object):
    def __init__(self):
        super(ArtellaHoudiniShelfManager, self).__init__()

        self._shelves = list()
        self._actions = dict()

    def create_shelf(self):
        """
        Implements create_shelf function
        """

        if not self._project:
            LOGGER.warning('Impossible to create shelf because project is not defined!')
            return False

        if tp.Dcc == tp.Dccs.Unknown or not self._parent:
            return

        self.clean_shelf()

        gui.create_shelf_set(name=self._shelf_name, dock=True)

        shelf_data = artellapipe.ToolsMgr().get_tool_shelfs() or dict()

        for tool_path, data in shelf_data.items():
            for i in iter(data):
                if isinstance(i, string_types) and i == 'separator':
                    continue
                self._shelf_creator(i)

        if self._shelves:
            shelf_set = gui.get_shelf_set(shelf_set_name=self._shelf_name)
            if shelf_set:
                self._shelves.reverse()
                shelf_set.setShelves(self._shelves)

        return True

    def clean_shelf(self):
        """
        Removes all already existing shelfs
        :return: bool
        """

        if not self._parent:
            return False

        if not self._shelf_name:
            LOGGER.warning('Impossible to clean shelf because shelf name is not defined!')
            return False

        if gui.shelf_set_exists(shelf_set_name=self._shelf_name):
            gui.remove_shelf_set(name=self._shelf_name)

        return True

    def _shelf_creator(self, data):
        category_name = data['name']
        shelf_name = '{}_{}'.format(self._shelf_name, category_name)
        if shelf_name not in self._actions:
            self._actions[shelf_name] = list()
            if gui.shelf_exists(shelf_name=shelf_name):
                gui.remove_shelf(name=shelf_name)
        if not gui.shelf_exists(shelf_name=shelf_name):
            new_shelve = gui.create_shelf(shelf_name=shelf_name, shelf_label=category_name.title())
            self._shelves.append(new_shelve)

        if 'children' not in data:
            return

        for i in iter(data['children']):
            action_type = i.get('type', 'command')
            if action_type == 'separator':
                continue
            self._add_action(i, shelf_name)

        if self._actions:
            for shelf_name, shelf_tools in self._actions.items():
                current_shelf = gui.get_shelf(shelf_name=shelf_name)
                if current_shelf:
                    current_shelf.setTools(shelf_tools)

    def _add_action(self, item_info, shelf_name):
        tool_id = item_info['id']
        tool_type = item_info.get('type', 'tool')
        tool_data = None
        if tool_type == 'command' or tool_type == 'tool':
            tool_data = artellapipe.ToolsMgr().get_tool_data_from_id(tool_id)
        if tool_data is None:
            LOGGER.warning('Shelf : Failed to find Tool: {}, type {}'.format(tool_id, tool_type))
            return

        tool_name = tool_data['config'].data.get('name', '')
        icon_name = tool_data['config'].data.get('icon', None)

        if tool_type == 'command':
            print('Adding Command ...')
        elif tool_type == 'tool':
            tool_command = "import artellapipe; artellapipe.ToolsMgr().run_tool(artellapipe.{}, " \
                           "'{}', do_reload=False, debug=False)".format(self._project.get_clean_name(), tool_id)
            tool_icon = None
            if icon_name:
                tool_icon = resource.ResourceManager().get('icons', 'shelf', '{}.png'.format(icon_name))
            new_tool = self._add_tool(label=tool_name, icon=tool_icon, command=tool_command)
            self._actions[shelf_name].append(new_tool)

    def _add_tool(self, label, icon='customIcon.png', command=None, command_type='python'):
        return gui.create_shelf_tool(
            tool_name='{}_{}'.format(self._shelf_name, label),
            tool_label=label,
            tool_type=command_type,
            tool_script=command,
            icon=icon
        )

    def _add_command(self):
        pass


@decorators.Singleton
class ArtellaHoudiniShelfManagerSingleton(ArtellaHoudiniShelfManager, object):
    def __init__(self):
        ArtellaHoudiniShelfManager.__init__(self)


artellapipe.register.register_class('ShelfMgr', ArtellaHoudiniShelfManagerSingleton)
