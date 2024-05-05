from qilocal.utils import PubSub


class TestPubSub:
    def test_pubsub_message(self):
        pubsub = PubSub()
        pubsub.clear()
        topic = pubsub.create_topic("test-topic")
        print("topic created")
        sub = pubsub.create_subscription("test-sub", topic)
        print("sub created")
        pubsub.list_topics()
        print("listed topics")
        for n in range(0, 10):
            topic.publish(str(n))
        response = sub.pull(10)
        for n in range(0, 10):
            assert response[n] == str(n)
