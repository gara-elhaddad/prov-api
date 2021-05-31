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
from enum import Enum
from uuid import UUID
from typing import List, Union


from pydantic import Field


from ..common.data_models import (
    File,
    Computation,
    ComputationPatch,
    SoftwareVersion,
    ModelVersionReference,
)

from .examples import EXAMPLES

logger = logging.getLogger("ebrains-prov-api")


class Simulator(str, Enum):
    """docstring for Simulator goes here"""
    nest="NEST"
    neuron="NEURON"
    brian="Brian"
    arbor="Arbor"
    spinnaker="SpiNNaker"
    brainscales="BrainScaleS"


class Simulation(Computation):
    """Record of a numerical simulation"""

    input: List[Union[File, ModelVersionReference, SoftwareVersion]] = Field(..., description="Inputs to this simulation (models, data files, configuration files and/or code)")
    # informed_by: "SimulationNew" = None

    class Config:
        schema_extra = EXAMPLES["Simulation"]


class SimulationPatch(ComputationPatch):
    """Correction of or update to a record of a numerical simulation"""

    input: List[Union[File, ModelVersionReference, SoftwareVersion]] = None
    # informed_by: "Simulation" = None

    class Config:
        schema_extra = {
            "example": {
                "end_time": "2021-05-28T16:32:58.597Z",
                "status": "failed",
                "resource_usage": [
                    {
                        "value": 1017.3,
                        "units": "core-hours"
                    }
                ],
                "tags": [
                    "core-dump"
                ]
            }
        }
