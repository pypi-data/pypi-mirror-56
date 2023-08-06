import sys
import time
import numpy as np

sys.path.append('../')

from rlclient import client


def test_random_requests(rlclient):
    run_id = 0

    cumulative_reward = 0
    n = 10000
    _time = time.time()
    for request_number in range(n):
        context = rlclient.get_context(run_id, request_number)
        # print(context['context'].values())
        if request_number % 1000 == 0:
            print(time.time() - _time)
            _time = time.time()
            print(request_number)
        offer = {
            'header': [5, 15, 35],
            'language': ['NL', 'EN', 'GE'],
            'adtype': ['skyscraper', 'square', 'banner'],
            'color': ['green', 'blue', 'red', 'black', 'white'],
            'price': list(map(lambda x: 1 + float(x) / 10., range(490)))
        }
        # Random choice
        offer = {key: np.random.choice(val) for key, val in offer.items()}

        result = rlclient.serve_page(run_id, request_number,
                                     header=offer['header'],
                                     language=offer['language'],
                                     adtype=offer['adtype'],
                                     color=offer['color'],
                                     price=offer['price'])

        # print(result, offer['price'] * result['success'])
        cumulative_reward += offer['price'] * result['success']

    mean_reward = cumulative_reward / n
    print("Mean reward: %.2f euro" % mean_reward)


if __name__ == "__main__":
    rlclient = client.RLClient("steven", "password")
    test_random_requests(rlclient)
