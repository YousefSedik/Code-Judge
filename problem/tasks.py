from worker import celery
from problem.utils.add_cses_problem_task import add_cses_problem

@celery.task
def add_cses_problem_task(cses_problem_id, problem_request_id, PHPSESSID):
    add_cses_problem(cses_problem_id, problem_request_id, PHPSESSID)
