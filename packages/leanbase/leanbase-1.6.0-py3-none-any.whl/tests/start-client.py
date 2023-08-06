import logging

import leanbase

logging.basicConfig(level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

leanbase.configure(
    api_key="7dc96185-bc8e-4c30-9a22-7d672b884452",
    user_token_secret="1562c73185c28387d52079e6540a6398",
    team_id="5qgZJg1",
    convey_host="http://localhost:9000/",
)

leanbase.await_initialisation(1.0)
logging.info("ZZ")
logging.info(leanbase.user({'user.email': 'funda@gmail.com'}).can_access('4VLJOnp'))
logging.info("OO")
logging.info(leanbase.user({'user.email': 'funda@puls.com'}).can_access('4VLJOnp'))
logging.info(leanbase.user({'user.email': 'funda@puls.com'}).get_user_token())

