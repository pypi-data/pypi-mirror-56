# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the configuration merger. Understand by that the fact that we are mergin
the upstream configuration file locally.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""


from os import sep as directory_separator

from colorama import Fore, Style

import PyFunceble


class Merge:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Merge the old into the new configuration file.
    :param str configuration_path: The path to the configuration file to update.
    """

    def __init__(self, configuration_path):
        config_link = PyFunceble.converter.InternalUrl(
            "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.PyFunceble_production.yaml"  # pylint: disable=line-too-long
        ).get_converted()

        self.path_to_config = configuration_path

        if not self.path_to_config.endswith(directory_separator):
            self.path_to_config += directory_separator

        self.path_to_config += (
            PyFunceble.abstracts.Infrastructure.CONFIGURATION_FILENAME
        )

        dict_instance = PyFunceble.helpers.Dict()

        self.local_config = dict_instance.from_yaml_file(self.path_to_config)
        self.upstream_config = dict_instance.from_yaml(
            PyFunceble.helpers.Download(config_link).text()
        )

        if self.upstream_config["links"]["config"] != config_link:
            self.upstream_config = dict_instance.from_yaml(
                PyFunceble.helpers.Download(
                    self.upstream_config["links"]["config"]
                ).text()
            )

        self.new_config = {}

        if self._is_local_version_different_from_upstream():
            self._load()

    def _is_local_version_different_from_upstream(self):
        """
        Checks if we have to merge.
        """

        # We check if all upstream keys are into the local keys map.
        result = not PyFunceble.helpers.Dict(self.local_config).has_same_keys_as(
            self.upstream_config
        )

        PyFunceble.LOGGER.debug(f"Local version is different from upstream: {result}")
        return result

    def _merge_values(self):
        """
        Simply merge the older into the new one.
        """

        to_remove = []

        self.new_config = PyFunceble.helpers.Dict(
            PyFunceble.helpers.Merge(self.local_config).into(self.upstream_config)
        ).remove_key(to_remove)

        if "seconds_before_http_timeout" in self.new_config:
            self.new_config["timout"] = self.new_config["seconds_before_http_timeout"]
            del self.new_config["seconds_before_http_timeout"]

    def _save(self):
        """
        Save the new configuration inside the configuration file.
        """

        PyFunceble.helpers.Dict(self.new_config).to_yaml_file(self.path_to_config)

        if "config_loaded" in PyFunceble.INTERN:
            del PyFunceble.INTERN["config_loaded"]

            if "custom_config_loaded" in PyFunceble.INTERN:
                custom = PyFunceble.INTERN["custom_config_loaded"]
            else:
                custom = None

            PyFunceble.load_config(custom=custom)

    def _load(self):
        """
        Execute the logic behind the merging.
        """

        if not PyFunceble.helpers.EnvironmentVariable(
            "PYFUNCEBLE_AUTO_CONFIGURATION"
        ).exists():
            # The auto configuration environment variable is not set.

            while True:
                # We infinitly loop until we get a reponse which is `y|Y` or `n|N`.

                # We ask the user if we should install and load the default configuration.
                response = input(
                    Style.BRIGHT
                    + Fore.RED
                    + "A configuration key is missing.\n"
                    + Fore.RESET
                    + "Try to merge upstream configuration file into %s ? [y/n] "
                    % (Style.BRIGHT + self.path_to_config + Style.RESET_ALL)
                )

                if isinstance(response, str):
                    # The response is a string

                    if response.lower() == "y":
                        # The response is a `y` or `Y`.

                        # We merge the old values inside the new one.
                        self._merge_values()

                        # And we save.
                        self._save()

                        print(
                            Style.BRIGHT + Fore.GREEN + "Done!\n"
                            "If it happens again, please fill a new issue."
                        )

                        # And we break the loop as we got a satisfied response.
                        break

                    if response.lower() == "n":
                        # The response is a `n` or `N`.

                        # We inform the user that something went wrong.
                        raise PyFunceble.exceptions.ConfigurationFileNotFound()
        else:
            # The auto configuration environment variable is set.

            # We merge the old values inside the new one.
            self._merge_values()

            # And we save.
            self._save()
