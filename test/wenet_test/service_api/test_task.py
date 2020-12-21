from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.common.model.norm.norm import Norm, NormOperator
from wenet.common.model.task.task import Task, TaskGoal, TaskPage
from wenet.common.model.task.transaction import TaskTransaction


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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=98765432,
            transactions=[],
            community_id="community_id"
        )

        to_repr = task.to_repr()
        from_repr = Task.from_repr(to_repr)

        self.assertEqual(task, from_repr)

    def test_repr2(self):

        task = Task(
            task_id=None,
            creation_ts=1577833200,
            last_update_ts=1577833200,
            task_type_id="task_type_id",
            requester_id="requester_id",
            app_id="app_id",
            goal=TaskGoal(
                name="goal",
                description="description"
            ),
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
        )

        to_repr = task.to_repr()
        from_repr = Task.from_repr(to_repr)

        self.assertEqual(task, from_repr)
        self.assertIsNone(from_repr.task_id)

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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833301,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id1",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={},
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key1": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[],
            community_id="community_id_2"
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
            norms=[
                Norm(
                    norm_id="norm-id",
                    attribute="attribute",
                    operator=NormOperator.EQUALS,
                    comparison=True,
                    negation=False
                )
            ],
            attributes={
                "key": "value"
            },
            close_ts=1577833300,
            transactions=[TaskTransaction(None, "task_id", "label", 123, 123, "actioneer_id", {}, [])],
            community_id="community_id"
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


class TestTaskPage(TestCase):

    def test_repr(self):

        task_page = TaskPage(
            offset=1,
            total=100,
            tasks=[
                Task(
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
                    norms=[
                        Norm(
                            norm_id="norm-id",
                            attribute="attribute",
                            operator=NormOperator.EQUALS,
                            comparison=True,
                            negation=False
                        )
                    ],
                    attributes={
                        "key": "value"
                    },
                    close_ts=1577833300,
                    transactions=[],
                    community_id="community_id"
                ),
                Task(
                    task_id="task-id1",
                    creation_ts=1577833200,
                    last_update_ts=1577833200,
                    task_type_id="task_type_id",
                    requester_id="requester_id",
                    app_id="app_id",
                    goal=TaskGoal(
                        name="goal",
                        description="description"
                    ),
                    norms=[
                        Norm(
                            norm_id="norm-id",
                            attribute="attribute",
                            operator=NormOperator.EQUALS,
                            comparison=True,
                            negation=False
                        )
                    ],
                    attributes={
                        "key": "value"
                    },
                    close_ts=1577833300,
                    transactions=[],
                    community_id="community_id"
                )
            ]
        )

        from_repr = TaskPage.from_repr(task_page.to_repr())

        self.assertIsInstance(from_repr, TaskPage)
        self.assertEqual(from_repr, task_page)
