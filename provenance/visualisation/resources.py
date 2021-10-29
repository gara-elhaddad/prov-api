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

from os import environ, stat_result
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
import logging
from itertools import chain


from fastapi import APIRouter, Depends, Header, Query, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError

import fairgraph.openminds.computation as omcmp

from ..auth.utils import get_kg_client_for_user_account

from .data_models import Visualisation, VisualisationPatch
from ..common.data_models import HardwareSystem, Status
from .. import settings


logger = logging.getLogger("ebrains-prov-api")

auth = HTTPBearer()
router = APIRouter()


@router.get("/visualisations/", response_model=List[Visualisation])
def query_visualisations(
    dataset: UUID = Query(None, description="Return visualisations of this dataset"),
    simulation: UUID = Query(None, description="Return visualisations of results from this simulation"),
    input_data: UUID = Query(None, description="Return visualisations of a given data file or directory containing data files"),
    software: UUID = Query(None, description="Return visualisations that used a specific software version"),
    platform: HardwareSystem = Query(None, description="Return visualisations that ran on this hardware platform"),
    space: str = Query("myspace", description="Knowledge Graph space to search in"),
    status: Status = Query(None, description="Return visualisations with this status"),
    tags: List[str] = Query(None, description="Return visualisations with _all_ of these tags"),
    size: int = Query(100, description="Number of records to return"),
    from_index: int = Query(0, description="Index of the first record to return"),
    # from header
    token: HTTPAuthorizationCredentials = Depends(auth),

):
    """
    Query recorded data visualisations, filtered according to various criteria.

    Where multiple filters are applied, they are combined with AND,
    e.g. software=<UUID for Elephant v0.9.0>&platform=pizdaint returns
    data visualisations that used Elephant v0.9.0 and that ran on Piz Daint.

    The list may contain records of data visualisations that are public, were performed by the logged-in user,
    or that are associated with a collab of which the user is a member.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    # todo: implement filters
    visualisation_objects = omcmp.Visualisation.list(kg_client, scope="in progress", api="query",
                                                    size=size, from_index=from_index,
                                                    space=space)
    return [obj.from_kg_object(kg_client) for obj in visualisation_objects]


@router.post("/visualisations/", response_model=Visualisation, status_code=status.HTTP_201_CREATED)
def create_visualisation(
    visualisation: Visualisation,
    space: str = "myspace",
    token: HTTPAuthorizationCredentials = Depends(auth)
):
    """
    Store a new record of a visualisation stage in the Knowledge Graph.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    #(visualisation_obj, started_by, inputs, outputs, environment,
    # launch_configuration) = visualisation.to_kg_object(kg_client)
    #for item in (launch_configuration, environment, *outputs, *inputs, started_by, visualisation_obj):
    #    item.save(kg_client, space="myspace")  # todo: support collab spaces. Save people to common?
    if visualisation.id is not None:
        visualisation_object = omcmp.Visualisation.from_uuid(visualisation.id, kg_client, scope="in progress")
        if visualisation_object is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A visualisation with id {visualisation.id} already exists. The POST endpoint cannot be used to modify an existing visualisation record.",
            )

    visualisation_obj = visualisation.to_kg_object(kg_client)
    visualisation_obj.save(kg_client, space=space, recursive=True)
    return visualisation_obj.from_kg_object(kg_client)


@router.get("/visualisations/{visualisation_id}", response_model=Visualisation)
def get_visualisation(visualisation_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Retrieve a specific visualisation record, identified by its ID.

    You may only retrieve public records, records that you created, or records associated with a collab which you can view.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    visualisation_object = omcmp.Visualisation.from_uuid(visualisation_id, kg_client, scope="in progress")
    return Visualisation.from_kg_object(visualisation_object, kg_client)


@router.put("/visualisations/{visualisation_id}", response_model=Visualisation)
def replace_visualisation(
    visualisation_id: UUID,
    visualisation: Visualisation,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Replace a visualisation record in its entirety.

    You may only replace records that you created, or that are associated with a collab of which you are an administrator.

    DISCUSSION POINT: should this be generally allowed, restricted to administrators/service accounts, or not allowed?
    """
    pass


@router.patch("/visualisations/{visualisation_id}", response_model=Visualisation)
def update_visualisation(
    visualisation_id: UUID,
    patch: VisualisationPatch,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Modify part of the metadata in a visualisation record.

    You may only update records that you created, or that are associated with a collab of which you are an administrator.

    DISCUSSION POINT: should this be generally allowed, restricted to administrators/service accounts, or not allowed?
    """
    pass


@router.delete("/analyses/{visualisation_id}", response_model=Visualisation)
def delete_visualisation(visualisation_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Delete a visualisation record.

    You may only delete records that you created, or that are associated with a collab of which you are an administrator.
    """
    pass
