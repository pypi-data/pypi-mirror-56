from cloudshell.cli.session.session_exceptions import CommandExecutionException
from cloudshell.shell.flows.configuration.basic_flow import AbstractConfigurationFlow

from cloudshell.networking.juniper.command_actions.commit_rollback_actions import (
    CommitRollbackActions,
)
from cloudshell.networking.juniper.command_actions.save_restore_actions import (
    SaveRestoreActions,
)
from cloudshell.networking.juniper.helpers.save_restore_helper import SaveRestoreHelper


class JuniperConfigurationFlow(AbstractConfigurationFlow):
    def __init__(self, resource_config, logger, cli_configurator):
        super(JuniperConfigurationFlow, self).__init__(logger, resource_config)
        self.cli_configurator = cli_configurator

    @property
    def _file_system(self):
        return "local:"

    def _save_flow(self, folder_path, configuration_type, vrf_management_name=None):
        """Backup config.

        Backup 'startup-config' or 'running-config' from
        device to provided file_system [ftp|tftp].
        Also possible to backup config to localhost
        :param folder_path:  tftp/ftp server where file be saved
        :param configuration_type: type of configuration
        that will be saved (StartUp or Running)
        :param vrf_management_name: Virtual Routing and
        Forwarding management name
        :return: Saved configuration path
        """
        SaveRestoreHelper.validate_configuration_type(configuration_type)

        self._logger.info("Save configuration to file {0}".format(folder_path))
        with self.cli_configurator.config_mode_service() as cli_service:
            save_action = SaveRestoreActions(cli_service, self._logger)
            save_action.save_running(folder_path)
        return folder_path

    def _restore_flow(
        self, path, restore_method, configuration_type, vrf_management_name
    ):
        """Restore configuration on device from provided configuration file.

        Restore configuration from local file system or ftp/tftp
        server into 'running-config' or 'startup-config'.
        :param path: relative path to the file on the
        remote host tftp://server/sourcefile
        :param configuration_type: the configuration
        type to restore (StartUp or Running)
        :param restore_method: override current config or not
        :param vrf_management_name: Virtual Routing and
        Forwarding management name
        :return:
        """
        SaveRestoreHelper.validate_configuration_type(configuration_type)

        restore_method = restore_method or "override"
        restore_method = restore_method.lower()

        if restore_method == "append":
            restore_type = "merge"
        elif restore_method == "override":
            restore_type = restore_method
        else:
            raise Exception(
                self.__class__.__name__,
                "Restore method '{}' is wrong! Use 'Append' or 'Override'".format(
                    restore_method
                ),
            )

        if not path:
            raise Exception(self.__class__.__name__, "Config source cannot be empty")

        with self.cli_configurator.config_mode_service() as cli_service:
            restore_actions = SaveRestoreActions(cli_service, self._logger)
            commit_rollback_actions = CommitRollbackActions(cli_service, self._logger)
            try:
                restore_actions.restore_running(restore_type, path)
                commit_rollback_actions.commit()
            except CommandExecutionException:
                commit_rollback_actions.rollback()
                raise
