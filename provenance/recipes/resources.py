"""
docstring goes here
"""

"""
   Copyright 2022 CNRS

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

import fairgraph.openminds.computation as omcmp

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError

from ..auth.utils import get_kg_client_for_user_account
from ..common.utils import create_computation, delete_computation
from .data_models import WorkflowRecipe


logger = logging.getLogger("ebrains-prov-api")

auth = HTTPBearer()
router = APIRouter()


@router.get("/recipes/", response_model=List[WorkflowRecipe])
def query_workflow_recipes(
    space: str = Query("myspace", description="Knowledge Graph space to search in"),
    size: int = Query(100, description="Number of records to return"),
    from_index: int = Query(0, description="Index of the first record to return"),
    # from header
    token: HTTPAuthorizationCredentials = Depends(auth),
):
    """
    Query workflow recipes.

    The list may contain records of recipes that are public
    or that are associated with a collab of which the user is a member.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    recipes = omcmp.WorkflowRecipeVersion.list(
        kg_client, scope="in progress", space=space,
        from_index=from_index, size=size)
    return [WorkflowRecipe.from_kg_object(rcp, kg_client) for rcp in recipes]


@router.get("/recipes/{recipe_id}", response_model=WorkflowRecipe)
def get_workflow_recipe(recipe_id: UUID, token: HTTPAuthorizationCredentials = Depends(auth)):
    """
    Retrieve a workflow recipe (aka workflow description) from the Knowledge Graph, identified by its ID.

    You may only retrieve public recipes, recipes that you created, or recipes associated with a collab which you can view.
    """
    kg_client = get_kg_client_for_user_account(token.credentials)
    recipe_object = omcmp.WorkflowRecipeVersion.from_uuid(str(recipe_id), kg_client, scope="in progress")
    return WorkflowRecipe.from_kg_object(recipe_object, kg_client)
