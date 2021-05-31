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

from typing import List
from uuid import UUID
from datetime import datetime
import logging


from fastapi import APIRouter, Depends, Header, Query, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError

from .data_models import DataAnalysis, DataAnalysisPatch
from ..common.data_models import HardwareSystem, Status
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
    pass


@router.post("/analyses/", response_model=DataAnalysis, status_code=status.HTTP_201_CREATED)
def create_data_analysis(data_analysis: DataAnalysis, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Store a new record of a data analysis stage in the Knowledge Graph.
    """
    pass


@router.get("/analyses/{analysis_id}", response_model=DataAnalysis)
def get_data_analysis(analysis_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Retrieve a specific data analysis record, identified by its ID.

    You may only retrieve public records, records that you created, or records associated with a collab which you can view.
    """
    pass


@router.put("/analyses/{analysis_id}", response_model=DataAnalysis)
def replace_data_analysis(
    analysis_id: UUID,
    data_analysis: DataAnalysis,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Replace a data analysis record in its entirety.

    You may only replace records that you created, or that are associated with a collab of which you are an administrator.

    DISCUSSION POINT: should this be generally allowed, restricted to administrators/service accounts, or not allowed?
    """
    pass


@router.patch("/analyses/{analysis_id}", response_model=DataAnalysis)
def update_data_analysis(
    analysis_id: UUID,
    patch: DataAnalysisPatch,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Modify part of the metadata in a data analysis record.

    You may only update records that you created, or that are associated with a collab of which you are an administrator.

    DISCUSSION POINT: should this be generally allowed, restricted to administrators/service accounts, or not allowed?
    """
    pass


@router.delete("/analyses/{analysis_id}", response_model=DataAnalysis)
def delete_data_analysis(analysis_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Delete a data analysis record.

    You may only delete records that you created, or that are associated with a collab of which you are an administrator.
    """
    pass
