from worker import celery
from submit.utils.code_evaluate import test
import asyncio

@celery.task
async def task_code_task(submission_id, problem_id):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # No active event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Await the test function to completion and get the result
    result = loop.run_until_complete(test(submission_id, problem_id))

    # Ensure result is JSON serializable (e.g., str, int, dict)
    return result if result is not None else "Completed"


