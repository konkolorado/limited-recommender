"""
Asynchronous tasks to be executed on the backend recommender workers

Any function decorated with the @task is sent to a Queue to eventually be
executed on a Worker. This allows the function to be run as capacity is made
available without freezing the UI
"""
from collections import defaultdict

import numpy

from recommender.queue.publish import task

from bookcrossing.models import User, Book, Rating
from recommender.models import Similarity


@task("recommendations-exchange", "recommendations-queue", "new_recommendation")
def empty_func(num1, num2):
    return num1 + num2


@task("recommendations-exchange", "recommendations-queue", "new_recommendation")
def compute_similarities():
    """
    Creates or updates the item-similarity matrix

    For each item in product catalog, I1
        For each customer C who purchased I1
            For each item I2 purchased by customer C
                Record that a customer purchased I1 and I2
        For each item I2 Compute the similarity between I1 and I2
    """
    new_similarties = 0
    n_users = User.objects.all().count()

    # For each item in catalog
    for book in Book.objects.all():

        item_to_item = defaultdict(lambda: ddict_callable(n_users))

        # For each customer c who purchased item
        for rating in Rating.objects.filter(isbn__id=book.id):
            # Record c rated book and other_rated_book, part 1
            item_to_item[book.isbn][rating.user_id.id-1] = 1

            # For every other item purchased by customer c
            for rated_book in Rating.objects.filter(
                    user_id__id=rating.user_id.id).exclude(
                    isbn__id=book.id):

                # Record c rated book and other_rated_book, part 2
                item_to_item[rated_book.isbn.isbn][rating.user_id.id-1] = 1

        # For each item bought along with item, compute similarity
        sims = compute_similarity_scores(book.isbn, item_to_item)

        # Store item to item similarities
        newly_created = commit_similarities(book.isbn, sims)
        new_similarties += newly_created
    return new_similarties


def ddict_callable(n_users):
    """
    A callable that can be supplied to defaultdicts to initialize keys
    with a list of zeroes of length # of Users
    """
    return list([0]) * n_users


def compute_similarity_scores(source, item_to_item, precision=14):
    """
    Computes cosine similarity scores between item and all other items
    in co_rated_items dictionary
    """
    similarities = dict()
    for other_item in item_to_item:
        if other_item == source:
            continue
        score = calc_cosine_similarity(item_to_item[source],
                                       item_to_item[other_item])
        similarities[other_item] = round(score, precision)
    return similarities


def calc_cosine_similarity(a, b):
    """ Computes the cosine similarity between two 1-dimensional lists """
    return numpy.dot(a, b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b))


def commit_similarities(item, similarities):
    """
    Takes an object identifier "item" and a dict of similarities where each
    key is another object identifier and the value is the similarity
    between the two items
    """
    newly_created = 0
    for similar_item_isbn in similarities:
        _, created = Similarity.objects.update_or_create(
            source=Book.objects.get(isbn=item),
            target=Book.objects.get(isbn=similar_item_isbn),
            defaults={'score': similarities[similar_item_isbn]})
        if created:
            newly_created += 1
    return newly_created
