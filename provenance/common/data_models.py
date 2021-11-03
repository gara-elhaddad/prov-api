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
from os import environ
from uuid import UUID
from typing import List, Union, Optional
import re
import hashlib
import json
from fairgraph.registry import lookup_by_id
from fairgraph.utility import as_list

from pydantic.errors import DecimalIsNotFiniteError

try:
    from typing import Literal  # Python >= 3.8
except ImportError:
    from typing_extensions import Literal
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, AnyUrl, Field

from fairgraph.base_v3 import KGProxyV3 as KGProxy, IRI, as_list
#from fairgraph.openminds import controlledterms
from fairgraph.openminds.core.miscellaneous.quantitative_value import QuantitativeValue
from fairgraph.openminds.core import (
    Person as KGPerson, ORCID, File as KGFile, Organization as KGOrganization,
    FileRepository as KGFileRepository, Hash as KGHash, ContentType as KGContentType,
    SoftwareVersion as KGSoftwareVersion, ParameterSet as KGParameterSet,
    StringParameter as KGStringParameter, NumericalParameter as KGNumericalParameter
)
from fairgraph.openminds.controlledterms import FileRepositoryType, UnitOfMeasurement
from fairgraph.openminds.computation import (
    Environment as KGComputationalEnvironment,
    HardwareSystem as KGHardwareSystem,
    LaunchConfiguration as KGLaunchConfiguration
)

from .examples import EXAMPLES
from ..auth.utils import get_kg_client_for_service_account


KGFile.set_strict_mode(False, "is_part_of")
KGHardwareSystem.set_strict_mode(False, "version")
KGParameterSet.set_strict_mode(False, "relevant_for")


class Status(str, Enum):
    """Status of a computation"""

    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class CryptographicHashFunction(str, Enum):
    """Algorithm used to compute digest of file contents"""

    sha1 = "SHA-1"
    md5 = "MD5"
    todo = "list to be completed"


def get_identifier(iri):
    """Return a valid Python variable name based on a KG object UUID"""
    return "ct_" + iri.split("/")[-1].replace("-", "")


def _get_content_types():
    kg_client_service_account = get_kg_client_for_service_account()
    content_types = KGContentType.list(kg_client_service_account, scope="latest", space="controlled")
    values = [(get_identifier(ct.id), ct.name) for ct in content_types]
    values.append(("ct_python", "text/x-python"))  # temporary workaround for missing content type we need
    return values


ContentType = Enum(
    "ContentType",
    _get_content_types()
)

class Licence(str, Enum):
    """Software or document licence"""

    gpl3 = "GPL3"
    bsd = "BSD"
    ccby = "CC-BY"
    mit = "MIT"
    apache = "Apache v2"
    todo = "list to be completed"


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


# todo: look these up, don't hard code, might have different UUIDs in prod, int, dev, etc.
CSCS = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/e3f16a1a-184e-447d-aced-375c00ec4d41")
Github = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/8e16b752-a95a-41f9-acc7-7f7e7c950f1d")
Yale = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/5093d906-e058-47e9-a9eb-ac56354f79fc")  # create ModelDB as an org?
EBRAINS = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/7dfdd91f-3d05-424a-80bd-6d1d5dc11cd3")
CERN = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/dbf4d089-9be1-4420-822b-87ecb7204840")  # create Zenodo as an org?
EBI = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/30aa86d9-39b0-45d1-a8c3-a76d64bfe57a")  # create BioModels as an org?
Bitbucket = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/574d7d5c-056a-4dae-9d1c-921057451199")
CNRS = KGProxy(KGOrganization, "https://kg.ebrains.eu/api/instances/31259b06-91d0-4ad8-acfd-303fc9ed613b")


file_location_patterns = {
    "https://object.cscs.ch": EBRAINS,
    "swift://cscs.ch": EBRAINS,
    "https://ksproxy.cscs.ch": EBRAINS,
    "https://kg.humanbrainproject.org/proxy/export": EBRAINS,
    "https://github.com": Github,
    "https://senselab.med.yale.edu": Yale,
    "http://modeldb.yale.edu": Yale,
    "http://example.com": None,
    "https://collab.humanbrainproject.eu": EBRAINS,
    "collab://": EBRAINS,
    "https://drive.ebrains.eu": EBRAINS,
    "https://zenodo.org": CERN,
    "https://www.ebi.ac.uk": EBI,
    "https://CrimsonWhite@bitbucket.org": Bitbucket,
    "http://cns.iaf.cnrs-gif.fr": CNRS,
}


def get_repository_host(url):
    for fragment, org in file_location_patterns.items():
        if fragment in url:
            return org
    return None


def get_repository_iri(url):
    pattern = "https:\/\/object\.cscs\.ch\/v1\/(?P<proj>\w+)\/(?P<container_name>[\w\.]+)\/(?P<path>\S*)"
    match = re.match(pattern, url)
    if match:
        return IRI(f"https://object.cscs.ch/v1/{match[0]}/{match[1]}")

    if url.startswith("https://drive.ebrains.eu"):
        return IRI("https://drive.ebrains.eu")
    raise NotImplementedError(f"Repository IRI format not yet supported. Value was {url}")


def get_repository_name(url):
    pattern = "https:\/\/object\.cscs\.ch\/v1\/(?P<proj>\w+)\/(?P<container_name>[\w\.]+)\/(?P<path>\S*)"
    match = re.match(pattern, url)
    if match:
        return match[2]

    if url.startswith("https://drive.ebrains.eu"):
        return "EBRAINS Drive"
    raise NotImplementedError(f"Repository IRI format not yet supported. Value was {url}")


def get_repository_type(url):
    if url.startswith("https://object.cscs.ch"):
        return FileRepositoryType(name="Swift repository")
    elif url.startswith("https://drive.ebrains.eu"):
        return FileRepositoryType(name="Seafile repository")
    raise NotImplementedError(f"Repository IRI format not yet supported. Value was {url}")


class File(BaseModel):
    """Metadata about a file"""

    description: Optional[str] = Field(None, title="Description of the file contents")
    format: Optional[ContentType] = Field(None, title="Content type of the file, expressed as a media type string")
    hash: Digest = None
    location: AnyUrl
    file_name: str
    size: Optional[int] = Field(None, title="File size in bytes")
    # bundle
    # repository

    class Config:
        schema_extra = {"example": EXAMPLES["File"]}

    @classmethod
    def from_kg_object(cls, file_object, client):
        return cls(
            format=[ct for ct in ContentType if ct.value == file_object.format.resolve(client).name][0],
            hash=Digest(value=file_object.hash.digest, algorithm=CryptographicHashFunction.sha1),
            location=file_object.iri.value,
            file_name=file_object.name,
            size=int(file_object.storage_size.value),
            description=file_object.content
        )

    def to_kg_object(self, client):
        file_repository = KGFileRepository(
            hosted_by=get_repository_host(self.location),
            iri=get_repository_iri(self.location),
            name=get_repository_name(self.location),
            repository_type=get_repository_type(self.location)
        )
        if self.format:
            content_type = KGContentType(name=self.format.value)
        else:
            # todo: if self.format is empty, we should try to infer it
            content_type = None
        hash = KGHash(algorithm=self.hash.algorithm.value, digest=self.hash.value)
        if self.size is None:
            storage_size = None
        else:
            storage_size = QuantitativeValue(value=float(self.size), unit=UnitOfMeasurement(name="bytes"))
        file_obj = KGFile(
            file_repository=file_repository,
            format=content_type,
            hash=hash,
            iri=IRI(self.location),
            name=self.file_name,
            storage_size=storage_size,
            content=self.description
        )
        return file_obj


class HardwareSystem(str, Enum):
    """Computer hardware system

    "spinnaker":     the SpiNNaker 600 board machine at University of Manchester
    "spinnaker4":    a SpiNNaker 4-chip board
    "spinnaker48":   a SpiNNaker 48-chip board
    "brainscales1":  the BrainScaleS-1 system at Heidelberg University
    "pizdaint":      Piz Daint (CSCS)
    "jusuf":         JUSUF (JSC)
    "galileo"        Galileo100 (CINECA)
    "openstack_cscs" OpenStack VMs at CSCS
    "openstack_jsc"  OpenStack VMs at JSC

    """

    spinnaker = "spinnaker"  # the SpiNNaker 600 board machine at University of Manchester"
    spinnaker4 = "spinnaker4"  # a SpiNNaker 4-chip board"
    spinnaker48 = "spinnaker48"  # a SpiNNaker 48-chip board"
    brainscales1 = "brainscales1"  # the BrainScaleS-1 system at Heidelberg University"
    pizdaint = "pizdaint"  # Piz Daint (CSCS)"
    jusuf = "jusuf"  # "JUSUF (JSC)"
    galileo100 = "galileo"  # Galileo100 (CINECA)"
    openstack_cscs = "openstack_cscs"
    openstack_jsc = "openstack_jsc"


class StringParameter(BaseModel):
    """A parameter whose value is a string"""

    name: str
    value: str

    class Config:
        schema_extra = {
            "example": {
                "name": "method",
                "value": "simulated_annealing"
            }
        }

    @classmethod
    def from_kg_object(cls, param):
        return cls(
            name=param.name,
            value=param.value
        )

    def to_kg_object(self, client):
        return KGStringParameter(name=self.name, value=self.value)


class NumericalParameter(BaseModel):
    """A parameter whose value is a number or physical quantity"""

    name: str
    value: Decimal
    units: str = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Rm",
                "value": 100.3,
                "units": "MΩ"
            }
        }

    def __str__(self):
        return f"{self.name} = {self.value} {self.units}"

    @classmethod
    def from_kg_object(cls, param):
        return cls(
            name=param.name,
            value=param.values[0].value,
            units=param.values[0].units
        )

    def to_kg_object(self, client):
        return KGNumericalParameter(
            name=self.name,
            values=QuantitativeValue(value=self.value, units=UnitOfMeasurement(name=self.units))
        )


class ParameterSet(BaseModel):
    """A collection of parameters"""

    items: List[Union[StringParameter, NumericalParameter]]
    description: str = None

    @property
    def identifier(self):
        return hashlib.sha1(
            json.dumps(
                [str(item) for item in self.items]
            ).encode("utf-8")).hexdigest()

    @classmethod
    def from_kg_object(cls, ps_object, client):
        items = []
        for param in as_list(ps_object.parameters):
            if isinstance(param, KGNumericalParameter):
                items.append(NumericalParameter.from_kg_object(param))
            elif isinstance(param, KGStringParameter):
                items.append(StringParameter.from_kg_object(param))
            else:
                raise TypeError("unexpected object type in parameter set")
        return cls(
            items=items,
            description=ps_object.context
        )

    def to_kg_object(self, client):
        return KGParameterSet(
            parameters=[item.to_kg_object(client) for item in self.items],
            context=self.description
        )


class Person(BaseModel):
    """A human person responsible for launching a computation"""

    given_name: str
    family_name: str
    orcid: str = None

    class Config:
        schema_extra = {
            "example": {
                "family_name": "Destexhe",
                "given_name": "Alain",
                "orcid": "https://orcid.org/0000-0001-7405-0455"
            }
        }

    @classmethod
    def from_kg_object(cls, person, client):
        person = person.resolve(client)
        if person.digital_identifiers:
            orcid = person.digital_identifiers[0].resolve(client).identifier
        else:
            orcid = None
        return cls(given_name=person.given_name, family_name=person.family_name,
                   orcid=orcid)

    def to_kg_object(self, client):
        obj = KGPerson(family_name=self.family_name, given_name=self.given_name)
        if self.orcid:
            obj.digital_identifiers = [ORCID(identifier=self.orcid)]
        return obj


class ResourceUsage(BaseModel):
    """Measurement of the usage of some resource, such as memory, compute time"""

    value: Decimal
    units: str

    class Config:
        schema_extra = {
            "example": {
                "value": 1017.3,
                "units": "core-hours"
            }
        }

    @classmethod
    def from_kg_object(cls, resource_usage, client):
        return cls(
            value=resource_usage.value,
            units=resource_usage.unit.resolve(client).name
        )

    def to_kg_object(self, client):
        return QuantitativeValue(value=float(self.value), unit=UnitOfMeasurement(name=self.units))


class SoftwareVersion(BaseModel):
    """Minimal representation of a specific piece of software"""

    id: UUID = None
    software_name: str
    software_version: str

    class Config:
        schema_extra = {
            "example": {
                "software_name": "NEST",
                "software_version": "2.20.0"
            }
        }

    @classmethod
    def from_kg_object(cls, software_version_object, client):
        svo = software_version_object.resolve(client)
        return cls(
            id=client.uuid_from_uri(svo.id),
            software_name=svo.name,
            software_version=svo.version_identifier
        )

    def to_kg_object(self, client):
        KGSoftwareVersion.set_strict_mode(False)
        obj = KGSoftwareVersion(name=self.software_name, alias=self.software_name,
                                version_identifier=self.software_version)
        KGSoftwareVersion.set_strict_mode(True)
        return obj


class ComputationalEnvironment(BaseModel):
    """The environment within which a computation takes place"""

    id: UUID = None
    name: str =Field(..., description="A name/label for this computing environment")
    hardware: HardwareSystem = Field(..., description="The hardware system on which this environment runs")
    configuration: Optional[List[
        ParameterSet
    ]] = Field(None, description="All important hardware settings defining this environment")
    software: Optional[List[
        SoftwareVersion
    ]] = Field(None, description="All software versions available in this environment. Note that the Analysis/Simulation schemas allow storing a list of software versions actually _used_ in a computation")
    description: Optional[str] = Field(None, description="A description of this computing environment")

    class Config:
        schema_extra = {"example": EXAMPLES["ComputationalEnvironment"]}

    @classmethod
    def from_kg_object(cls, env_object, client):
        env = env_object.resolve(client)
        return cls(
            id=client.uuid_from_uri(env.id),
            name=env.name,
            hardware=getattr(HardwareSystem, env.hardware.resolve(client).name),
            configuration=[ParameterSet.from_kg_object(obj, client) for obj in as_list(env.configuration)],
            software=[SoftwareVersion.from_kg_object(obj, client) for obj in as_list(env.software)],
            description=env.description
        )

    def to_kg_object(self, client):
        return KGComputationalEnvironment(
            name=self.name,
            hardware=KGHardwareSystem(name=self.hardware.value, version="not specified"),
            configuration=[conf.to_kg_object(client) for conf in self.configuration],
            software=[sv.to_kg_object(client) for sv in self.software],
            description=self.description
        )


class LaunchConfiguration(BaseModel):
    """Metadata describing how a computation was launched"""

    description: Optional[str] = Field(None, description="Description of this launch configuration")
    name: Optional[str] = Field(None, description="Label for this launch configuration")
    executable: str = Field(..., description="Path to the command-line executable")
    arguments: Optional[List[str]] = Field(None, description="Command line arguments as a list of strings")
    environment_variables: Optional[ParameterSet] = (
        Field(None, description="Any environment variables defined by this launch configuration")
    )

    class Config:
        schema_extra = {"example": EXAMPLES["LaunchConfiguration"]}

    @property
    def identifier(self):
        return hashlib.sha1(
            json.dumps(
                {
                    "name": self.name,
                    "executable": self.executable,
                    "arguments": self.arguments,
                    "environment_variables": self.environment_variables.identifier if self.environment_variables else None
                }
            ).encode("utf-8")).hexdigest()

    @classmethod
    def from_kg_object(cls, launch_config_object, client):
        lco = launch_config_object.resolve(client)
        return cls(
            description=lco.description,
            name=lco.name,
            executable=lco.executable,
            arguments=lco.arguments,
            environment_variables=ParameterSet.from_kg_object(lco.environment_variables, client)
        )

    def to_kg_object(self, client):
        if self.environment_variables is None:
            env_vars = None
        else:
            self.environment_variables.description = self.environment_variables.description or "environment variables"
            env_vars = self.environment_variables.to_kg_object(client)
        if self.name is None:
            self.name = f"LaunchConfiguration-{self.identifier}"
        return KGLaunchConfiguration(
            name=self.name,
            description=self.description,
            executable=self.executable,
            arguments=self.arguments,
            environment_variables=env_vars
        )


class Computation(BaseModel):
    """
    Abstract base class, should not appear in documentation
    """

    id: Optional[UUID] = Field(None, description="IDs should be valid UUID v4 identifiers. If an ID is not supplied it will be generated by the Knowledge Graph")
    input: List[Union[File, SoftwareVersion]] = Field(..., description="Inputs to this computation (data files and/or code)")
    output: List[File] = Field(..., description="Files generated by this computation")
    environment: ComputationalEnvironment
    launch_config: LaunchConfiguration
    start_time: datetime
    end_time: datetime = None
    started_by: Optional[Person] = Field(None, description="If this field is left blank it is assumed that the account used to upload the provenance metadata is the same as that used to launch the computation")
    status: Status = None
    resource_usage: List[ResourceUsage] = None
    tags: List[str] = None


class ComputationPatch(Computation):
    """
    Abstract base class, should not appear in documentation
    """

    id: UUID
    input: List[Union[File, SoftwareVersion]] = None
    output: List[File] = None
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

    model_version_id: UUID = None
