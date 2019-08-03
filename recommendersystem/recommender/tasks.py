"""
Asynchronous tasks to be executed on the backend recommender workers

Any function decorated with the @task is sent to a Queue to eventually be
executed on a Worker. This allows the function to be run as capacity is made
available without freezing the UI
"""


from recommender.queue.publish import task


@task("recommendations-exchange", "recommendations-queue", "new_recommendation")
def empty_func(num1, num2):
    return num1 + num2
