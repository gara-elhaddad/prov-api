from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from . import (
    settings,
    simulation,
    dataanalysis,
    visualisation,
    optimisation,
    workflows,
    auth,
    vocab,
)

description = """
This is a proposal for the EBRAINS Provenance API.

It has not yet been implemented, i.e. none of the endpoints work!
Nevertheless, the proposed endpoints and document schemas are all documented below.
"""

app = FastAPI(title="EBRAINS Provenance API", description=description, version="1.0")

app.add_middleware(SessionMiddleware, secret_key=settings.SESSIONS_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication and authorization"])
app.include_router(simulation.router, tags=["Simulations"])
app.include_router(dataanalysis.router, tags=["Data analysis"])
app.include_router(visualisation.router, tags=["Visualisation"])
app.include_router(optimisation.router, tags=["Optimisation"])
app.include_router(workflows.router, tags=["Workflows"])
app.include_router(vocab.router, tags=["Controlled vocabularies"])
