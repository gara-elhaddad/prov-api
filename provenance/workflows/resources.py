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

from .data_models import Workflow
from .. import settings


logger = logging.getLogger("ebrains-prov-api")

auth = HTTPBearer()
router = APIRouter()


@router.get("/workflows/", response_model=List[Workflow])
def query_workflows(
    tags: List[str] = Query(None, description="Return workflows with _all_ of these tags"),
    size: int = Query(100, description="Number of records to return"),
    from_index: int = Query(0, description="Index of the first record to return"),
    # from header
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Query recorded workflows, filtered according to various criteria.

    The list may contain records of workflows that are public, were launched by the logged-in user,
    or that are associated with a collab of which the user is a member.
    """
    pass


@router.post("/workflows/", response_model=Workflow, status_code=status.HTTP_201_CREATED)
def store_recorded_workflow(workflow: Workflow, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Store a new record of a workflow execution in the Knowledge Graph.
    """
    pass


@router.get("/workflows/{workflow_id}", response_model=Workflow)
def get_recorded_workflow(workflow_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Retrieve a specific record of a workflow execution from the Knowledge Graph, identified by its ID.

    You may only retrieve public records, records that you created, or records associated with a collab which you can view.
    """
    pass


@router.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Delete a record of a computational workflow execution.

    You may only delete records that you created, or that are associated with a collab of which you are an administrator.
    """
    pass