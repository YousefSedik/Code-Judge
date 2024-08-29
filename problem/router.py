from fastapi.routing import APIRouter


router = APIRouter()


@router.get("/problem/<problem_id>")
async def get_problem(problem_id: int):
    return {"problem_id": problem_id}


@router.post("/problem/manual")
async def create_problem():
    return {"message": "Problem created successfully"}


@router.post("/problem/CSES")
async def create_problem_cses():
    return {"message": "Problem created successfully"}
