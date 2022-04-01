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
    statistics,
)

description = """
This is a work in progress.

Many of the endpoints work, but not all features have been implemented,
in particular filter terms for computation queries, and more testing is needed.

At present, all metadata are saved in the pre-production version of the KG,
which is reset from time-to-time, and so metadata will not be preserved long-term:
for now, please use this only for testing.

To use the API, <a href="/login" target="_blank">login here</a>, click on "Authorize" then
copy the <i>access_token</i> into the "HTTPBearer" box
(this process will be streamlined for the beta release).
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

app.include_router(workflows.router, tags=["Workflows"])
app.include_router(statistics.router, tags=["Statistics"])
app.include_router(simulation.router, tags=["Simulations"])
app.include_router(dataanalysis.router, tags=["Data analysis"])
app.include_router(visualisation.router, tags=["Visualisation"])
app.include_router(optimisation.router, tags=["Optimisation"])
app.include_router(auth.router, tags=["Authentication and authorization"])
#app.include_router(vocab.router, tags=["Controlled vocabularies"])
