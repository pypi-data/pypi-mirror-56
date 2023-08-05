# -*- coding: utf-8 -*-

"""Main module."""

from datetime import datetime

from pynamodb.attributes import (
    UTCDateTimeAttribute,
)

class PynamodbRestMixin:

    createdAt = UTCDateTimeAttribute(null=False, default=datetime.utcnow)
    updatedAt = UTCDateTimeAttribute(null=False)

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.utcnow()
        super(PynamodbRestMixin, self).save()

    def add_items(self, data):
        for name in self.get_attributes().keys():
            value = data.get(name)
            if value:
                setattr(self, name, value)
        return self

    @classmethod
    def update_actions(cls, obj, data, operation="set", exclude=None):
        actions = []
        exclude_set = set(["updatedAt", "createdAt"])
        if exclude:
            exclude_set = exclude_set.union(set(exclude))

        for name in obj.get_attributes().keys():
            if name in exclude_set:
                continue
            value = data.get(name)
            if value and value is not None:
                model_attr = getattr(cls, name)

                update_op = getattr(model_attr, operation)
                action_op = update_op(value)
                actions.append(action_op)

        return actions

    def update_save(self, actions):
        self.update(actions=actions)
        self.save()
        return self