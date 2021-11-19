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
from fairgraph.openminds.computation.environment import Environment


from fastapi import APIRouter, Depends, Header, Query, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError

import fairgraph.openminds.computation as omcmp

from ..auth.utils import get_kg_client_for_user_account, is_collab_admin

from .data_models import DataAnalysis, DataAnalysisPatch
from ..common.data_models import HardwareSystem, LaunchConfiguration, Status
from .. import settings


logger = logging.getLogger("ebrains-prov-api")

auth = HTTPBearer()
router = APIRouter()


@router.get("/analyses/", response_model=List[DataAnalysis])
def query_analyses(
    dataset: UUID = Query(None, description="Return analyses of this dataset"),
    simulation: UUID = Query(None, description="Return analyses of results from this simulation"),
    input_data: UUID = Query(None, description="Return analyses of a given data file or directory containing data files"),
    software: UUID = Query(None, description="Return analyses that used a specific software version"),
    platform: HardwareSystem = Query(None, description="Return analyses that ran on this hardware platform"),
    space: str = Query("myspace", description="Knowledge Graph space to search in"),
    status: Status = Query(None, description="Return analyses with this status"),
    tags: List[str] = Query(None, description="Return analyses with _all_ of these tags"),
    size: int = Query(100, description="Number of records to return"),
    from_index: int = Query(0, description="Index of the first record to return"),
    # from header
    token: HTTPAuthorizationCredentials = Depends(auth),

):
    """
    Query recorded data analyses, filtered according to various criteria.

    Where multiple filters are applied, they are combined with AND,
    e.g. software=<UUID for Elephant v0.9.0>&platform=pizdaint returns
    data analyses that used Elephant v0.9.0 and that ran on Piz Daint.

    The list may contain records of data analyses that are public, were performed by the logged-in user,
    or that are associated with a collab of which the user is a member.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    # todo: implement filters
    # todo: query different spaces: "computation", "myspace", private collab spaces for which the user is a member
    data_analysis_objects = omcmp.DataAnalysis.list(kg_client, scope="in progress", api="query",
                                                    size=size, from_index=from_index,
                                                    space=space)
    return [obj.from_kg_object(kg_client) for obj in data_analysis_objects]


@router.post("/analyses/", response_model=DataAnalysis, status_code=status.HTTP_201_CREATED)
def create_data_analysis(
    data_analysis: DataAnalysis,
    space: str = "myspace",
    token: HTTPAuthorizationCredentials = Depends(auth)
):
    """
    Store a new record of a data analysis stage in the Knowledge Graph.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    if data_analysis.id is not None:
        data_analysis_object = omcmp.Visualisation.from_uuid(str(data_analysis.id), kg_client, scope="in progress")
        if data_analysis_object is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A data analysis with id {data_analysis.id} already exists. "
                        "The POST endpoint cannot be used to modify an existing data analysis record.",
            )
    data_analysis.id == uuid4()
    data_analysis_obj = data_analysis.to_kg_object(kg_client)
    data_analysis_obj.save(kg_client, space=space, recursive=True)
    return DataAnalysis.from_kg_object(data_analysis_obj, kg_client)


@router.get("/analyses/{analysis_id}", response_model=DataAnalysis)
def get_data_analysis(analysis_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Retrieve a specific data analysis record, identified by its ID.

    You may only retrieve public records, records in your private space,
    or records associated with a collab which you can view.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    data_analysis_object = omcmp.DataAnalysis.from_uuid(str(analysis_id), kg_client, scope="in progress")
    return DataAnalysis.from_kg_object(data_analysis_object, kg_client)


@router.put("/analyses/{analysis_id}", response_model=DataAnalysis)
def replace_data_analysis(
    analysis_id: UUID,
    data_analysis: DataAnalysis,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Replace a data analysis record in its entirety.

    You may only replace records in your private space,
    or that are associated with a collab of which you are an administrator.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    data_analysis_object = omcmp.DataAnalysis.from_uuid(analysis_id, kg_client, scope="in progress")
    if not (data_analysis_object.space == "myspace" or is_collab_admin(data_analysis_object.space, token.credentials)):
        raise HTTPException(
            status_code=403,
            detail="You can only replace provenance records in your private space "
                   "or in collab spaces for which you are an administrator."
        )
    if data_analysis.id is not None and data_analysis.id != analysis_id:
        raise HTTPException(
            status_code=400,
            detail="The ID of the payload does not match the URL"
        )
    data_analysis_obj_new = data_analysis.to_kg_object(kg_client)
    data_analysis_obj_new.id = data_analysis_object.id
    data_analysis_obj_new.save(kg_client, space=data_analysis_object.space, recursive=True, replace=True)
    return DataAnalysis.from_kg_object(data_analysis_obj_new, kg_client)


@router.patch("/analyses/{analysis_id}", response_model=DataAnalysis)
def update_data_analysis(
    analysis_id: UUID,
    patch: DataAnalysisPatch,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Modify part of the metadata in a data analysis record.

    You may only update records records in your private space,
    or that are associated with a collab of which you are an administrator.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    data_analysis_object = omcmp.DataAnalysis.from_uuid(str(analysis_id), kg_client, scope="in progress")
    if not (data_analysis_object.space == "myspace" or is_collab_admin(data_analysis_object.space, token.credentials)):
        raise HTTPException(
            status_code=403,
            detail="You can only modify provenance records in your private space "
                   "or in collab spaces for which you are an administrator."
        )
    if patch.id is not None and patch.id != analysis_id:
        raise HTTPException(
            status_code=400,
            detail="Modifying the record ID is not permitted."
        )
    data_analysis_obj_updated = patch.apply_to_kg_object(data_analysis_object, kg_client)
    data_analysis_obj_updated.save(kg_client, space=data_analysis_object.space, recursive=True)
    return DataAnalysis.from_kg_object(data_analysis_obj_updated, kg_client)


@router.delete("/analyses/{analysis_id}")
def delete_data_analysis(analysis_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Delete a data analysis record.

    You may only delete records records in your private space,
    or that are associated with a collab of which you are an administrator.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    data_analysis_object = omcmp.DataAnalysis.from_uuid(analysis_id, kg_client, scope="in progress")
    if not (data_analysis_object.space == "myspace" or is_collab_admin(data_analysis_object.space)):
        raise HTTPException(
            status_code=403,
            detail="You can only delete provenance records in your private space "
                   "or in collab spaces for which you are an administrator."
        )
    data_analysis_object.delete(kg_client)
