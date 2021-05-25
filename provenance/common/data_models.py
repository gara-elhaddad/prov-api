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

from enum import Enum
from uuid import UUID
from typing import List, Union
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, AnyUrl


class Status(str, Enum):
    """Status of a computation"""

    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class CryptographicHashFunction(str, Enum):
    """Algorithm used to compute digest of file contents"""

    sha1 = "sha1"
    md5 = "md5"


class ContentType(str, Enum):
    """The content/media type of a file"""

    pdf = "application/pdf"
    png = "image/png"


class Licence(str, Enum):
    """Software or document licence"""

    gpl3 = "GPL3"
    bsd = "BSD"
    ccby = "CC-BY"
    mit = "MIT"
    apache = "Apache v2"


class Species(str, Enum):
    mouse = "Mus musculus"
    rat = "Rattus norvegicus"
    human = "Homo sapiens"
    macaque = "Macaca mulatta"
    marmoset = "Callithrix jacchus"
    rodent = "Rodentia"  # yes, not a species
    opossum = "Monodelphis domestica"
    platypus = "Ornithorhynchus anatinus"


BrainRegion = Enum(
    "BrainRegion",
    [(name.replace(" ", "_"), name) for name in ["cortex", "hippocampus", "list to be completed"]],
)


ModelScope = Enum(
    "ModelScope",
    [
        (name.replace(" ", "_").replace(":", "__"), name)
        for name in ["single cell", "network", "list to be completed"]
    ],
)


AbstractionLevel = Enum(
    "AbstractionLevel",
    [
        (name.replace(" ", "_").replace(":", "__"), name)
        for name in ["spiking neurons", "neural field", "list to be completed"]
    ],
)


CellType = Enum(
    "CellType",
    [
        (name.replace(" ", "_"), name)
        for name in ["pyramidal cell", "interneuron", "list to be completed"]
    ],
)


class Digest(BaseModel):
    """Hash value of the content of a file, used as a simple way to check if the contents have changed"""

    value: str
    algorithm: CryptographicHashFunction


class File(BaseModel):
    """Metadata about a file"""

    description: str = None
    format: ContentType = None
    hash: Digest = None
    location: AnyUrl
    name: str
    size: int = None
    # bundle
    # repository


class HardwareSystem(str, Enum):
    """Computer hardware system"""

    spinnaker = "the SpiNNaker 600 board machine at University of Manchester"
    spinnaker4 = "a SpiNNaker 4-chip board"
    spinnaker48 = "a SpiNNaker 48-chip board"
    brainscales1 = "the BrainScaleS-1 system at Heidelberg University"
    pizdaint = "Piz Daint (CSCS)"
    jusuf = "JUSUF (JSC)"
    galileo100 = "Galileo100 (CINECA)"


class StringParameter(BaseModel):
    """A parameter whose value is a string"""

    name: str
    value: str


class NumericalParameter(BaseModel):
    """A parameter whose value is a number or physical quantity"""

    name: str
    value: Decimal
    units: str = None


class ParameterSet(BaseModel):
    """A collection of parameters"""

    items: Union[StringParameter, NumericalParameter]
    description: str


class Person(BaseModel):
    """A human person responsible for launching a computation"""

    given_name: str
    family_name: str
    orcid: str = None


class ResourceUsage(BaseModel):
    """Measurement of the usage of some resource, such as memory, compute time"""

    value: Decimal
    units: str


class SoftwareVersion(BaseModel):
    """Minimal representation of a specific piece of software"""

    id: UUID = None
    name: str
    version: str


class ComputationalEnvironment(BaseModel):
    """The environment within which a computation takes place"""

    id: UUID = None
    name: str  # a name/label for this computing environment
    hardware: HardwareSystem  # the hardware system on which this environment runs
    configuration: List[
        ParameterSet
    ] = None  # all important hardware settings defining this environment.
    software: List[
        SoftwareVersion
    ] = None  # all software versions available in this environment. [Note: this is optional. The Analysis/Simulation schemas allow storing a list of software versions actually _used_ in a computation
    description: str  # a description of this computing environment


class LaunchConfiguration(BaseModel):
    """Metadata describing how a computation was launched"""

    description: str = None  # description of this launch configuration
    name: str = None  # label for this launch configuration.
    executable: str  # path to the command-line executable
    arguments: List[str] = None  # command line arguments as a list of strings
    environment_variables: ParameterSet = (
        None  # any environment variables defined by this launch configuration
    )


class Computation(BaseModel):
    """
    Abstract base class, should not appear in documentation
    """

    id: UUID = None
    input: Union[File, SoftwareVersion]
    output: File
    environment: ComputationalEnvironment
    launch_config: LaunchConfiguration
    start_time: datetime
    end_time: datetime = None
    started_by: Person = None
    status: Status = None
    resource_usage: List[ResourceUsage] = None
    tags: List[str] = None


class ComputationPatch(Computation):
    """
    Abstract base class, should not appear in documentation
    """

    id: UUID
    input: Union[File, SoftwareVersion] = None
    output: File = None
    environment: ComputationalEnvironment = None
    launch_config: LaunchConfiguration = None
    start_time: datetime = None
    end_time: datetime = None
    started_by: Person = None
    status: Status = None
    resource_usage: List[ResourceUsage] = None
    tags: List[str] = None


class ModelVersionReference(BaseModel):
    """
    Reference to a model version.

    The Model Validation API or one of the KG APIs may be used to obtain further
    information about the model version using its ID.
    """

    id: UUID = None
