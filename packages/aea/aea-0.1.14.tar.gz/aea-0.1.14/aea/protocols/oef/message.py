# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the default message definition."""
from enum import Enum
from typing import Optional, List, cast

from aea.protocols.base import Message
from aea.protocols.oef.models import Description, Query


class OEFMessage(Message):
    """The OEF message class."""

    protocol_id = "oef"

    class Type(Enum):
        """OEF Message types."""

        REGISTER_SERVICE = "register_service"
        REGISTER_AGENT = "register_agent"
        UNREGISTER_SERVICE = "unregister_service"
        UNREGISTER_AGENT = "unregister_agent"
        SEARCH_SERVICES = "search_services"
        SEARCH_AGENTS = "search_agents"
        OEF_ERROR = "oef_error"
        DIALOGUE_ERROR = "dialogue_error"
        SEARCH_RESULT = "search_result"

        def __str__(self):
            """Get string representation."""
            return self.value

    class OEFErrorOperation(Enum):
        """Operation code for the OEF. It is returned in the OEF Error messages."""

        REGISTER_SERVICE = 0
        UNREGISTER_SERVICE = 1
        SEARCH_SERVICES = 2
        SEARCH_SERVICES_WIDE = 3
        SEARCH_AGENTS = 4
        SEND_MESSAGE = 5
        REGISTER_AGENT = 6
        UNREGISTER_AGENT = 7

        OTHER = 10000

        def __str__(self):
            """Get string representation."""
            return str(self.value)

    def __init__(self, oef_type: Optional[Type] = None,
                 **kwargs):
        """
        Initialize.

        :param oef_type: the type of OEF message.
        """
        super().__init__(type=oef_type, **kwargs)
        assert self.check_consistency(), "OEFMessage initialization inconsistent."

    def check_consistency(self) -> bool:
        """Check that the data is consistent."""
        try:
            assert self.is_set("type")
            oef_type = OEFMessage.Type(self.get("type"))
            if oef_type == OEFMessage.Type.REGISTER_SERVICE:
                assert self.is_set("id")
                assert self.is_set("service_description")
                assert self.is_set("service_id")
                service_description = self.get("service_description")
                service_id = self.get("service_id")
                assert isinstance(service_description, Description)
                assert isinstance(service_id, str)
            elif oef_type == OEFMessage.Type.REGISTER_AGENT:
                assert self.is_set("id")
                assert self.is_set("agent_description")
                assert self.is_set("agent_id")
                agent_description = self.get("agent_description")
                agent_id = self.get("agent_id")
                assert isinstance(agent_description, Description)
                assert isinstance(agent_id, str)
            elif oef_type == OEFMessage.Type.UNREGISTER_SERVICE:
                assert self.is_set("id")
                assert self.is_set("service_description")
                assert self.is_set("service_id")
                service_description = self.get("service_description")
                service_id = self.get("service_id")
                assert isinstance(service_description, Description)
                assert isinstance(service_id, str)
            elif oef_type == OEFMessage.Type.UNREGISTER_AGENT:
                assert self.is_set("id")
                assert self.is_set("agent_description")
                assert self.is_set("agent_id")
                agent_description = self.get("agent_description")
                agent_id = self.get("agent_id")
                assert isinstance(agent_description, Description)
                assert isinstance(agent_id, str)
            elif oef_type == OEFMessage.Type.SEARCH_SERVICES:
                assert self.is_set("id")
                assert self.is_set("query")
                query = self.get("query")
                assert isinstance(query, Query)
            elif oef_type == OEFMessage.Type.SEARCH_AGENTS:
                assert self.is_set("id")
                assert self.is_set("query")
                query = self.get("query")
                assert isinstance(query, Query)
            elif oef_type == OEFMessage.Type.SEARCH_RESULT:
                assert self.is_set("id")
                assert self.is_set("agents")
                agents = cast(List[str], self.get("agents"))
                assert type(agents) == list and all(type(a) == str for a in agents)
            elif oef_type == OEFMessage.Type.OEF_ERROR:
                assert self.is_set("id")
                assert self.is_set("operation")
                operation = self.get("operation")
                assert operation in set(OEFMessage.OEFErrorOperation)
            elif oef_type == OEFMessage.Type.DIALOGUE_ERROR:
                assert self.is_set("id")
                assert self.is_set("dialogue_id")
                assert self.is_set("origin")
            else:
                raise ValueError("Type not recognized.")
        except (AssertionError, ValueError):
            return False

        return True
