#!/usr/bin/env python3
#
#  IRIS VT Module Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from iris_interface.IrisModuleInterface import IrisPipelineTypes, IrisModuleInterface, IrisModuleTypes
import iris_interface.IrisInterfaceStatus as InterfaceStatus

import iris_check_module.IrisCheckConfig as interface_conf

from app.datamgmt.iris_engine.modules_db import module_list_available_hooks


class IrisCheckModule(IrisModuleInterface):
    """
    Main class of IrisCheck Module
    """
    _module_name = interface_conf.module_name
    _module_description = interface_conf.module_description
    _interface_version = interface_conf.interface_version
    _module_version = interface_conf.module_version
    _pipeline_support = interface_conf.pipeline_support
    _pipeline_info = interface_conf.pipeline_info
    _module_configuration = interface_conf.module_configuration
    _module_type = IrisModuleTypes.module_processor

    def register_hooks(self, module_id: int):
        """
        Registers all the hooks

        :param module_id: Module ID provided by IRIS
        :return: Nothing
        """
        hooks = [hook.hook_name for hook in module_list_available_hooks()]

        for hook in hooks:
            status = self.register_to_hook(module_id, iris_hook_name=hook)
            if status.is_failure():
                self.log.error(status.get_message())
                self.log.error(status.get_data())

            else:
                self.log.info(f"Successfully subscribed to {hook} hook")

    def hooks_handler(self, hook_name: str, data):
        """
        Hooks handler table. Simply log the call if the setting tells us to do so.

        :param hook_name: Name of the hook which triggered
        :param data: Data associated with the trigger.
        :return: IIStatus
        """

        if self._dict_conf.get('check_log_received_hook') is True:
            self.log.info(f'Received {hook_name}')
            self.log.info(f'Received data of type {type(data)}')

        return InterfaceStatus.I2Success(data=data, logs=list(self.message_queue))
