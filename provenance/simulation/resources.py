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

from .data_models import Simulation, SimulationPatch, Simulator
from ..common.data_models import HardwareSystem, Status
from .. import settings


logger = logging.getLogger("ebrains-prov-api")

auth = HTTPBearer()
router = APIRouter()


@router.get("/simulations/", response_model=List[Simulation])
def query_simulations(
    model_version: UUID = Query(None, description="Return only simulations of this model version"),
    simulator: Simulator = Query(None, description="Return simulations using this simulator"),
    platform: HardwareSystem = Query(None, description="Return simulations that ran on this hardware platform"),
    status: Status = Query(None, description="Return simulations with this status"),
    tags: List[str] = Query(None, description="Return simulations with _all_ of these tags"),
    size: int = Query(100, description="Number of records to return"),
    from_index: int = Query(0, description="Index of the first record to return"),
    # from header
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Query recorded simulations, filtered according to various criteria.

    Where multiple filters are applied, they are combined with AND,
    e.g. simulator=nest&platform=pizdaint returns NEST simulations that ran on Piz Daint.

    The list may contain records of simulations that are public, were performed by the logged-in user,
    or that are associated with a collab of which the user is a member.
    """
    pass


@router.post("/simulations/", response_model=Simulation, status_code=status.HTTP_201_CREATED)
def create_simulation(simulation: Simulation, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Store a new record of a numerical simulation in the Knowledge Graph.
    """
    pass


@router.get("/simulations/{simulation_id}", response_model=Simulation)
def get_simulation(simulation_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Retrieve a specific simulation record, identified by its ID.

    You may only retrieve public records, records that you created, or records associated with a collab which you can view.
    """
    pass


@router.put("/simulations/{simulation_id}", response_model=Simulation)
def replace_simulation(
    simulation_id: UUID,
    simulation: Simulation,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Replace a simulation record in its entirety.

    You may only replace records that you created, or that are associated with a collab of which you are an administrator.

    DISCUSSION POINT: should this be generally allowed, restricted to administrators/service accounts, or not allowed?
    """
    pass


@router.patch("/simulations/{simulation_id}", response_model=Simulation)
def update_simulation(
    simulation_id: UUID,
    patch: SimulationPatch,
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Modify part of the metadata in a simulation record.

    You may only update records that you created, or that are associated with a collab of which you are an administrator.

    DISCUSSION POINT: should this be generally allowed, restricted to administrators/service accounts, or not allowed?
    """
    pass


@router.delete("/simulations/{simulation_id}")
def delete_simulation(simulation_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Delete a simulation record.

    You may only delete records that you created, or that are associated with a collab of which you are an administrator.
    """
    pass
