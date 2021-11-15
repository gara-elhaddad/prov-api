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
    ComputationalEnvironment, File, SoftwareVersion
)

logger = logging.getLogger("ebrains-prov-api")


class DataAnalysis(Computation):
    """Record of a data analysis"""
    kg_cls = KGDataAnalysis

    @classmethod
    def from_kg_object(cls, data_analysis_object, client):
        dao = data_analysis_object.resolve(client)
        inputs = []
        for obj in as_list(dao.inputs):
            if isinstance(obj, KGFile):
                inputs.append(File.from_kg_object(obj, client))
            elif isinstance(obj, KGSoftwareVersion):
                inputs.append(SoftwareVersion.from_kg_object(obj, client))
            else:
                raise TypeError(f"unexpected object type in inputs: {type(obj)}")
        return cls(
            id=client.uuid_from_uri(dao.id),
            input=inputs,
            output=[File.from_kg_object(obj, client) for obj in as_list(dao.outputs)],
            environment=ComputationalEnvironment.from_kg_object(dao.environment, client),
            launch_config=LaunchConfiguration.from_kg_object(dao.launch_configuration, client),
            start_time=dao.started_at_time,
            end_time=dao.ended_at_time,
            started_by=Person.from_kg_object(dao.started_by, client),
            status=getattr(Status, dao.status.resolve(client).name),
            resource_usage=[ResourceUsage.from_kg_object(obj, client) for obj in as_list(dao.resource_usages)],
            tags=dao.tags
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
            status=ActionStatusType(name=self.status.value),
            resource_usages=resource_usage,
            tags=self.tags
        )
        return obj


class DataAnalysisPatch(ComputationPatch):
    """Correction of or update to a record of a data analysis"""

    pass
