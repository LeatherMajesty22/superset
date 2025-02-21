# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import re

from flask_babel import gettext as __

from superset.db_engine_specs.postgres import PostgresBaseEngineSpec
from superset.errors import SupersetErrorType

# Regular expressions to catch custom errors
TEST_CONNECTION_ACCESS_DENIED_REGEX = re.compile(
    'password authentication failed for user "(?P<username>.*?)"'
)
TEST_CONNECTION_INVALID_HOSTNAME_REGEX = re.compile(
    'could not translate host name "(?P<hostname>.*?)" to address: '
    "nodename nor servname provided, or not known"
)
TEST_CONNECTION_PORT_CLOSED_REGEX = re.compile(
    r"could not connect to server: Connection refused\s+Is the server "
    r'running on host "(?P<hostname>.*?)" (\(.*?\) )?and accepting\s+TCP/IP '
    r"connections on port (?P<port>.*?)\?"
)
TEST_CONNECTION_HOST_DOWN_REGEX = re.compile(
    r"could not connect to server: (?P<reason>.*?)\s+Is the server running on "
    r'host "(?P<hostname>.*?)" (\(.*?\) )?and accepting\s+TCP/IP '
    r"connections on port (?P<port>.*?)\?"
)


class RedshiftEngineSpec(PostgresBaseEngineSpec):
    engine = "redshift"
    engine_name = "Amazon Redshift"
    max_column_name_length = 127

    custom_errors = {
        TEST_CONNECTION_ACCESS_DENIED_REGEX: (
            __('Either the username "%(username)s" or the password is incorrect.'),
            SupersetErrorType.TEST_CONNECTION_ACCESS_DENIED_ERROR,
        ),
        TEST_CONNECTION_INVALID_HOSTNAME_REGEX: (
            __('The hostname "%(hostname)s" cannot be resolved.'),
            SupersetErrorType.TEST_CONNECTION_INVALID_HOSTNAME_ERROR,
        ),
        TEST_CONNECTION_PORT_CLOSED_REGEX: (
            __('Port %(port)s on hostname "%(hostname)s" refused the connection.'),
            SupersetErrorType.TEST_CONNECTION_PORT_CLOSED_ERROR,
        ),
        TEST_CONNECTION_HOST_DOWN_REGEX: (
            __(
                'The host "%(hostname)s" might be down, and can\'t be '
                "reached on port %(port)s."
            ),
            SupersetErrorType.TEST_CONNECTION_HOST_DOWN_ERROR,
        ),
    }

    @staticmethod
    def _mutate_label(label: str) -> str:
        """
        Redshift only supports lowercase column names and aliases.

        :param label: Expected expression label
        :return: Conditionally mutated label
        """
        return label.lower()
