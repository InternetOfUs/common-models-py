from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.service_api.norm import Norm, NormOperator
from wenet.service_api.task import Task, TaskGoal, TaskAttribute


class TestTask(TestCase):

    def test_repr(self):

        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )

        to_repr = task.to_repr()
        from_repr = Task.from_repr(to_repr)

        self.assertEqual(task, from_repr)

    def test_equals(self):
        task = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task1 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task2 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id1",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task3 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id1",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task4 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal1",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task5 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833101,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task6 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id1",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )
        task7 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[

            ]
        )
        task8 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833300,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name1",
                    value="value"
                )
            ]
        )
        task9 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833301,
            deadline_ts=1577833350,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )

        task10 = Task(
            task_id="task-id",
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            start_ts=1577833100,
            end_ts=1577833301,
            deadline_ts=1577833351,
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes=[
                TaskAttribute(
                    name="name",
                    value="value"
                )
            ]
        )

        self.assertEqual(task, task1)
        self.assertNotEqual(task, task2)
        self.assertNotEqual(task, task3)
        self.assertNotEqual(task, task4)
        self.assertNotEqual(task, task5)
        self.assertNotEqual(task, task6)
        self.assertNotEqual(task, task7)
        self.assertNotEqual(task, task8)
        self.assertNotEqual(task, task9)
        self.assertNotEqual(task, task10)


class TestTaskGoal(TestCase):

    def test_repr(self):

        task_goal = TaskGoal("name", "description")

        from_repr = TaskGoal.from_repr(task_goal.to_repr())

        self.assertIsInstance(from_repr, TaskGoal)
        self.assertEqual(task_goal, from_repr)

    def test_equal(self):
        task_goal = TaskGoal("name", "description")
        task_goal1 = TaskGoal("name", "description")
        task_goal2 = TaskGoal("name1", "description")
        task_goal3 = TaskGoal("name", "description1")

        self.assertEqual(task_goal, task_goal1)
        self.assertNotEqual(task_goal, task_goal2)
        self.assertNotEqual(task_goal, task_goal3)


class TestTaskAttribute(TestCase):

    def test_repr(self):
        task_attribute = TaskAttribute("name", "description")
        from_repr = TaskAttribute.from_repr(task_attribute.to_repr())

        self.assertIsInstance(from_repr, TaskAttribute)
        self.assertEqual(task_attribute, from_repr)

    def test_equal(self):
        task_attribute = TaskAttribute("name", "description")
        task_attribute1 = TaskAttribute("name", "description")
        task_attribute2 = TaskAttribute("name1", "description")
        task_attribute3 = TaskAttribute("name", "description1")

        self.assertEqual(task_attribute, task_attribute1)
        self.assertNotEqual(task_attribute, task_attribute2)
        self.assertNotEqual(task_attribute, task_attribute3)
