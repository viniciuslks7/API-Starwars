"""API v1 router aggregating all resource routers."""

from fastapi import APIRouter

from src.api.v1.comparison import router as comparison_router
from src.api.v1.films import router as films_router
from src.api.v1.people import router as people_router
from src.api.v1.planets import router as planets_router
from src.api.v1.species import router as species_router
from src.api.v1.starships import router as starships_router
from src.api.v1.statistics import router as statistics_router
from src.api.v1.vehicles import router as vehicles_router

router = APIRouter()

# Include all resource routers
router.include_router(people_router, prefix="/people", tags=["People"])
router.include_router(films_router, prefix="/films", tags=["Films"])
router.include_router(starships_router, prefix="/starships", tags=["Starships"])
router.include_router(planets_router, prefix="/planets", tags=["Planets"])
router.include_router(vehicles_router, prefix="/vehicles", tags=["Vehicles"])
router.include_router(species_router, prefix="/species", tags=["Species"])
router.include_router(statistics_router, prefix="/statistics", tags=["Statistics"])
router.include_router(comparison_router, prefix="/compare", tags=["Comparison"])
