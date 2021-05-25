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
from typing import Union


from pydantic import BaseModel, HttpUrl, AnyUrl, validator, ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status

from ..common.data_models import (
    File,
    Computation,
    ComputationPatch,
    SoftwareVersion,
    ModelVersionReference,
)

logger = logging.getLogger("ebrains-prov-api")


class Simulator(str, Enum):
    nest="NEST"
    neuron="NEURON"
    brian="Brian"
    arbor="Arbor"
    spinnaker="SpiNNaker"
    brainscales="BrainScaleS"


class Simulation(Computation):
    """Record of a numerical simulation"""

    input: Union[File, ModelVersionReference, SoftwareVersion]
    # informed_by: "SimulationNew" = None


class SimulationPatch(ComputationPatch):
    """Correction of or update to a record of a numerical simulation"""

    input: Union[File, ModelVersionReference, SoftwareVersion] = None
    # informed_by: "Simulation" = None
