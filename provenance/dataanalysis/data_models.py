"""
docstring goes here
"""

"""
   Copyright 2021 CNRS

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import logging
from uuid import UUID
from fairgraph.base_v3 import KGProxy
from fairgraph.utility import as_list

from fairgraph.openminds.computation import DataAnalysis as KGDataAnalysis
from fairgraph.openminds.controlledterms import ActionStatusType
from fairgraph.openminds.core import (
    Person as KGPerson,
    File as KGFile,
    SoftwareVersion as KGSoftwareVersion
)

from ..common.data_models import (
    Computation, ComputationPatch, Status, Person, ResourceUsage, LaunchConfiguration,
    ComputationalEnvironment, File, SoftwareVersion, ACTION_STATUS_TYPES, status_name_map
)

logger = logging.getLogger("ebrains-prov-api")


class DataAnalysis(Computation):
    """Record of a data analysis"""
    kg_cls = KGDataAnalysis

    @classmethod
    def from_kg_object(cls, data_analysis_object, client):
        obj = data_analysis_object.resolve(client)
        inputs = []
        for input in as_list(obj.inputs):
            if isinstance(input, KGProxy):
                input = input.resolve(client, scope="in progress")
            if isinstance(input, KGFile):
                inputs.append(File.from_kg_object(input, client))
            elif isinstance(input, KGSoftwareVersion):
                inputs.append(SoftwareVersion.from_kg_object(input, client))
            else:
                raise TypeError(f"unexpected object type in inputs: {type(input)}")
        return cls(
            id=client.uuid_from_uri(obj.id),
            input=inputs,
            output=[File.from_kg_object(outp, client) for outp in as_list(obj.outputs)],
            environment=ComputationalEnvironment.from_kg_object(obj.environment, client),
            launch_config=LaunchConfiguration.from_kg_object(obj.launch_configuration, client),
            start_time=obj.started_at_time,
            end_time=obj.ended_at_time,
            started_by=Person.from_kg_object(obj.started_by, client),
            status=getattr(Status, status_name_map[obj.status.resolve(client).name]),
            resource_usage=[ResourceUsage.from_kg_object(ru, client) for ru in as_list(obj.resource_usages)],
            tags=as_list(obj.tags)
        )

    def to_kg_object(self, client):
        if self.started_by:
            started_by = self.started_by.to_kg_object(client)
        else:
            started_by = KGPerson.me(client)  # todo
        inputs = [inp.to_kg_object(client) for inp in self.input]
        outputs = [outp.to_kg_object(client) for outp in self.output]
        environment = self.environment.to_kg_object(client)
        launch_configuration = self.launch_config.to_kg_object(client)
        resource_usage = [ru.to_kg_object(client) for ru in self.resource_usage]
        obj = self.__class__.kg_cls(
            id=client.uri_from_uuid(self.id),
            lookup_label=f"Data analysis by {started_by.full_name} on {self.start_time.isoformat()} [{self.id.hex[:7]}]",
            inputs=inputs,
            outputs=outputs,
            environment=environment,
            launch_configuration=launch_configuration,
            started_at_time=self.start_time,
            ended_at_time=self.end_time,
            started_by=started_by,
            #was_informed_by= # todo
            status=ACTION_STATUS_TYPES[self.status.value],
            resource_usages=resource_usage,
            tags=self.tags
        )
        return obj


class DataAnalysisPatch(ComputationPatch):
    """Correction of or update to a record of a data analysis"""

    def apply_to_kg_object(self, data_analysis_object, client):
        obj = data_analysis_object
        update_label = False
        if self.input:
            obj.inputs = [inp.to_kg_object(client) for inp in self.input]
        if self.output:
            obj.outputs = [outp.to_kg_object(client) for outp in self.output]
        if self.environment:
            obj.environment = self.environment.to_kg_object(client)
        if self.launch_config:
            obj.launch_configuration = self.launch_config.to_kg_object(client)
        if self.start_time:
            obj.started_at_time = self.start_time
            update_label = True
        if self.end_time:
            obj.ended_at_time = self.end_time
        if self.started_by:
            obj.started_by = self.started_by.to_kg_object(client)
            update_label = True
        if self.status:
            obj.status = ACTION_STATUS_TYPES[self.status.value]
        if self.resource_usage:
            obj.resource_usages = [ru.to_kg_object(client) for ru in self.resource_usage]
        if self.tags:
            obj.tags = as_list(self.tags)
        if update_label:
            obj.lookup_label = f"Data analysis by {obj.started_by.full_name} on {obj.started_at_time.isoformat()} [{obj.id.hex[:7]}]"
        return obj