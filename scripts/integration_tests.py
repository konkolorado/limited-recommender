"""
Runs integration tests to check if similarities in preloaded data are correct
"""
import requests
import urllib
import json
import time


def wait_for_url():
    while True:
        try:
            status = requests.get("http://localhost:8000").status_code
        except requests.exceptions.ConnectionError:
            print("Waiting for localhost:8000")
            time.sleep(5)
        else:
            if status == 200:
                break
            else:
                print("Waiting for localhost:8000")
                time.sleep(1)


def make_request_get_dict(url, args):
    """
    url: string url for the api endpoint to hit
    args: a list of tuples where the 0 indexed item is the key, 1 is the value
    """
    query = urllib.parse.urlencode(args)
    response = requests.get(url + "?" + query)
    assert response.status_code == 200
    return json.loads(response.text)


def test_similarities_counts():
    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0451408373")])
    assert result["count"] == 2

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0671745077")])
    assert result["count"] == 2

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0849953537")])
    assert result["count"] == 2


def test_similarities_scores():
    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0451408373"),
                                       ("target", "0671745077")])
    assert result["results"][0]["score"] == 1.0

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0451408373"),
                                       ("target", "0849953537")])
    assert result["results"][0]["score"] == 1.0

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0671745077"),
                                       ("target", "0451408373")])
    assert result["results"][0]["score"] == 0.70710678118655

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0671745077"),
                                       ("target", "0849953537")])
    assert result["results"][0]["score"] == 1.0

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0849953537"),
                                       ("target", "0451408373")])
    assert result["results"][0]["score"] == 0.57735026918963

    result = make_request_get_dict("http://localhost:8000/api/similarities/",
                                   [("source", "0849953537"),
                                       ("target", "0671745077")])
    assert result["results"][0]["score"] == 0.81649658092773


def main():
    wait_for_url()
    test_similarities_counts()
    test_similarities_scores()


if __name__ == "__main__":
    main()
