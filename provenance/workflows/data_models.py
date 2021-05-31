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

from typing import List, Union
from uuid import UUID

from pydantic import BaseModel, Field
from ..common.data_models import Person
from ..simulation.data_models import Simulation
from ..dataanalysis.data_models import DataAnalysis
from ..visualisation.data_models import Visualisation
from ..optimisation.data_models import Optimisation


class Workflow(BaseModel):
    id: UUID = None
    stages: List[Union[Simulation, DataAnalysis, Visualisation, Optimisation]] = Field(
        ...,
        description="A workflow record is specified by the list of computations that were carried out. "
                    "The sequence of computations is inferred from the inputs, outputs and start times of each stage."
    )
    started_by: Person = None
