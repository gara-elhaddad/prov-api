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
from typing import Union, Literal


from pydantic import BaseModel

from ..common.data_models import (
    File,
    Computation,
    ComputationPatch,
    SoftwareVersion,
    ModelVersionReference,
    ComputationType
)

logger = logging.getLogger("ebrains-prov-api")


class Optimisation(Computation):
    input: Union[File, ModelVersionReference, SoftwareVersion]
    output: Union[File, ModelVersionReference]
    type: Literal["optimization"]


class OptimisationPatch(ComputationPatch):
    input: Union[File, ModelVersionReference, SoftwareVersion] = None
    output: Union[File, ModelVersionReference] = None
