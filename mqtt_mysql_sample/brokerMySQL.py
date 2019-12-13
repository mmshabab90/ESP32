import logging
import asyncio
import pymysql.cursors

from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1

logger = logging.getLogger(__name__)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:5252'
        }
    },
    'sys_interval': 10,
    'topic-check': {
        'enabled': False
    }
}

broker = Broker(config)


@asyncio.coroutine
def startBroker():
    yield from broker.start()


@asyncio.coroutine
def brokerGetMessage():
    C = MQTTClient()
    yield from C.connect('mqtt://localhost:5252/')
    yield from C.subscribe([
        ('TESTtopic/test', QOS_1)
    ])
    logger.info('Subscribed!')
    try:
        for item in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print(packet.payload.data.decode('utf-8'))

            # Connect to the database
            connection = pymysql.connect(host='localhost',
                                         user='su',
                                         password='sa1234567',
                                         db='mqttpy',
                                         cursorclass=pymysql.cursors.DictCursor)

            with connection.cursor() as cursor:
                        # Create a new record
                sql = "INSERT INTO `mqttpy` (`message`) VALUES (%s)"
                value = str(packet.payload.data.decode('utf-8'))
                cursor.execute(sql, value)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            print(cursor.rowcount, 'Data saved!')

    except ClientException as client_exception:
        logger.error('Client exception: %s' % client_exception)


if __name__ == '__main__':
    formatter = '[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(startBroker())
    asyncio.get_event_loop().run_until_complete(brokerGetMessage())
    asyncio.get_event_loop().run_forever()
