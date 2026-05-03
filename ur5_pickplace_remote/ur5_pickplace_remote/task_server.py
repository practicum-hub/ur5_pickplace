#!/usr/bin/env python3

from threading import Thread

import rclpy
from moveit_commander import MoveGroupCommander
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from ur5_pickplace_msgs.action import Ur5PickplaceTask

class TaskServer(Node):
    def __init__(self):
        super().__init__('task_server')
        self.get_logger().info('Starting the Server')
        self.action_server = ActionServer(
            self,
            Ur5PickplaceTask,
            'task_server',
            self.goal_callback,
            self.cancel_callback,
            self.accepted_callback
        )

    def goal_callback(self, goal_handle):
        self.get_logger().info(f"Received goal request with task number {goal_handle.request.task_number}")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Received request to cancel goal")
        arm_move_group = MoveGroupCommander("arm")
        gripper_move_group = MoveGroupCommander("gripper")
        arm_move_group.stop()
        gripper_move_group.stop()

        return CancelResponse.ACCEPT

    def accepted_callback(self, goal_handle):
        Thread(target=self.execute, args=(goal_handle,)).start()

    def execute(self, goal_handle):
        self.get_logger().info('Executing goal')
        arm_move_group = MoveGroupCommander("arm")
        gripper_move_group = MoveGroupCommander("gripper")

        arm_joint_goal = []
        gripper_joint_goal = []

        if goal_handle.request.task_number == 0:
            arm_joint_goal = [0.0, 0.0, 0.0]
            gripper_joint_goal = [-0.7, 0.7]
        elif goal_handle.request.task_number == 1:
            arm_joint_goal = [-1.14, -0.6, -0.07]
            gripper_joint_goal = [0.0, 0.0]
        elif goal_handle.request.task_number == 2:
            arm_joint_goal = [-1.57, 0.0, -0.9]
            gripper_joint_goal = [0.0, 0.0]
        else:
            self.get_logger().error('Invalid Task Number')
            return

        arm_within_bounds = arm_move_group.set_joint_value_target(arm_joint_goal)
        gripper_within_bounds = gripper_move_group.set_joint_value_target(gripper_joint_goal)

        if not arm_within_bounds or not gripper_within_bounds:
            self.get_logger().warn("Target joint position(s) are outside of limits. Clamping to limits.")
            return

        arm_plan = arm_move_group.plan()
        gripper_plan = gripper_move_group.plan()

        if arm_plan and gripper_plan:
            self.get_logger().info("Planner SUCCEEDED, moving the arm and gripper")
            arm_move_group.go(wait=True)
            gripper_move_group.go(wait=True)
        else:
            self.get_logger().error("One or more planners failed!")
            return

        goal_handle.succeed()
        result = Ur5PickplaceTask.Result()
        result.success = True
        self.get_logger().info('Goal succeeded')

def main(args=None):
    rclpy.init(args=args)
    task_server = TaskServer()
    rclpy.spin(task_server)
    task_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
