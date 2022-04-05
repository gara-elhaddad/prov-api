from distutils.errors import LibError
import re
from typing import List
from enum import Enum
from uuid import UUID
from pydantic import AnyHttpUrl, AnyUrl, BaseModel, Field

from fairgraph.base_v3 import as_list, IRI
import fairgraph.openminds.core as omcore
import fairgraph.openminds.controlledterms as omterms
import fairgraph.openminds.computation as omcmp
from ..common.data_models import (Person, get_repository_host, get_repository_iri,
                                  get_repository_name, get_repository_type)
from ..common.utils import invert_dict


class WorkflowRecipeType(str, Enum):
    cwl = "Common Workflow Language"
    snakemake = "Snakemake"
    unicore = "UNICORE Workflow"
    generic_python = "Python script"
    jupyter = "Jupyter notebook"


content_type_lookup = {
    "application/vnd.commonworkflowlanguage.workflowdescription+yaml": WorkflowRecipeType.cwl,
    "application/vnd.snakemake.workflowrecipe": WorkflowRecipeType.snakemake,
    "application/vnd.unicore.workflowrecipe": WorkflowRecipeType.unicore,
    "text/x-python": WorkflowRecipeType.generic_python,
    "application/x-ipynb+json": WorkflowRecipeType.jupyter
}


class WorkflowRecipe(BaseModel):
    id: UUID = None
    name: str
    alias: str = None
    custodians: List[Person] = None
    description: str = None
    developers: List[Person] = None
    type: WorkflowRecipeType = None   # temporarily allow none, until new content types added
    full_documentation: AnyHttpUrl = None
    homepage: AnyHttpUrl = None
    keywords: List[str] = None
    location: AnyUrl
    version_identifier: str
    version_innovation: str = None

    @classmethod
    def from_kg_object(cls, recipe_version, client):
        recipe = omcmp.WorkflowRecipe.list(client, scope="in progress",
                                           space=recipe_version.space,
                                           versions=recipe_version)[0]
        if recipe_version.custodians:
            custodians = [Person.from_kg_object(p, client) 
                          for p in as_list(recipe_version.custodians)]  # todo: could be Organization
        else:
            custodians = [Person.from_kg_object(p, client) 
                          for p in as_list(recipe.custodians)]
        if recipe_version.developers:
            developers = [Person.from_kg_object(p, client) 
                          for p in as_list(recipe_version.developers)]
        else:
            developers = [Person.from_kg_object(p, client) 
                          for p in as_list(recipe.developers)]
        if recipe_version.format:
            type_ = content_type_lookup.get(
                recipe_version.format.resolve(client, scope="in progress").name,
                None)
        else:
            type_ = None
        if recipe_version.homepage:
            homepage = str(recipe_version.homepage.resolve(client, scope="in progress").url)
        elif recipe.homepage:
            homepage = str(recipe.homepage.resolve(client, scope="in progress").url)
        else:
            homepage = None
        return cls(
            id=recipe_version.uuid,
            name=recipe_version.name or recipe.name,
            alias=recipe_version.alias or recipe.alias,
            custodians=custodians,
            description=recipe_version.description or recipe.description,
            developers=developers,
            type=type_,
            full_documentation=recipe_version.full_documentation,
            homepage=homepage,
            keywords=recipe_version.keywords,
            location=str(recipe_version.repository.resolve(client, scope="in progress").iri),
            version_identifier=recipe_version.version_identifier,
            version_innovation=recipe_version.version_innovation
        )

    def to_kg_object(self, client):
        content_type_name = invert_dict(content_type_lookup).get(self.type, None)
        if content_type_name:
            format = omterms.ContentType.by_name(content_type_name, client)
        else:
            format = None
        return omcmp.WorkflowRecipeVersion(
            name=self.name,
            alias=self.alias,
            #accessibility',
            #copyright',
            custodians=[p.to_kg_object(client) for p in self.custodians],
            description=self.description,
            developers=[p.to_kg_object(client) for p in self.developers],
            #digital_identifier',
            format=format,
            full_documentation=self.full_documentation,
            #funding',
            #has_components',
            homepage=omcore.URL(url=self.homepage),
            #how_to_cite',
            #is_alternative_version_of',
            #is_new_version_of',
            keywords=self.keywords,
            #licenses',
            #other_contributions',
            #related_publications',
            #release_date',
            repository=omcore.FileRepository(
                name=get_repository_name(self.location),
                iri=get_repository_iri(self.location),
                hosted_by=get_repository_host(self.location),
                repository_type=get_repository_type(self.location),
            ),
            #support_channels',
            version_identifier=self.version_identifier,
            version_innovation=self.version_innovation
        )


class WorkflowRecipePatch(BaseModel):
    name: str = None
    alias: str = None
    custodians: List[Person] = None
    description: str = None
    developers: List[Person] = None
    type: WorkflowRecipeType = None   # temporarily allow none, until new content types added
    full_documentation: AnyHttpUrl = None
    homepage: AnyHttpUrl = None
    keywords: List[str] = None
    location: AnyUrl
    version_identifier: str
    version_innovation: str = None
