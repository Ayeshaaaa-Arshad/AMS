from celery import shared_task


@shared_task
def my_task():
    result = "Task executed!"
    print("Task executed!")
    return result
