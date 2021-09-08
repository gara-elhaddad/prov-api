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
from typing import Union


from pydantic import BaseModel
from fairgraph.openminds.computation import DataAnalysis as KGDataAnalysis, launchconfiguration
from fairgraph.openminds.controlledterms import ActionStatusType
from fairgraph.openminds.core import Person as KGPerson

from ..common.data_models import Computation, ComputationPatch

logger = logging.getLogger("ebrains-prov-api")


class DataAnalysis(Computation):
    """Record of a data analysis"""

    @classmethod
    def from_kg_objects(cls, objects):
        pass

    def to_kg_objects(self, client):
        if self.started_by:
            started_by = self.started_by.to_kg_object(client)
        else:
            started_by = KGPerson.me(client)  # todo
        inputs = [inp.to_kg_object(client) for inp in self.input]
        outputs = [outp.to_kg_object(client) for outp in self.output]
        environment = self.environment.to_kg_object(client)
        launch_configuration = self.launch_config.to_kg_object(client)
        resource_usage = [ru.to_kg_object(client) for ru in self.resource_usage]
        obj = KGDataAnalysis(
            id=self.id,
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
            tagss=self.tags
        )
        return [started_by, inputs, outputs, environment, launch_configuration, resource_usage]


class DataAnalysisPatch(ComputationPatch):
    """Correction of or update to a record of a data analysis"""

    pass
