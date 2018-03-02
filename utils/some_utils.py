from uuid import uuid4


def gender_topic_sn():
    topic_sn = str(uuid4()).split("-")[0]
    return topic_sn
