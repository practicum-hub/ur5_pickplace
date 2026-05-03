# ur5_pickplace (ROS 2)

A ROS 2 workspace for a pick-and-place manipulator: robot description, controllers, MoveIt config, custom interfaces, and utility nodes.

## Packages

- `ur5_pickplace_description`  
  URDF/Xacro, meshes, RViz config, Gazebo launch files.
- `ur5_pickplace_controller`  
  `ros2_control` controller config and launch setup.
- `ur5_pickplace_moveit`  
  MoveIt configuration and launch for `move_group + RViz`.
- `ur5_pickplace_msgs`  
  Custom action and service interfaces.
- `ur5_pickplace_remote`  
  Action server for task-level manipulator commands.
- `ur5_pickplace_utils`  
  Utility nodes for angle conversion (Euler/Quaternion).
- `ur5_pickplace_py`  
  Python node examples.

## Requirements

- ROS 2 (Humble/Jazzy)
- `colcon`
- `xacro`
- `ros2_control`
- `gazebo_ros`
- MoveIt 2

## Build

```bash
cd /home/antondeulia/Projects/ROS2/NotMyPortfolio/ur5_pickplace
colcon build
source install/setup.bash
```

## Quick Start

### 1) Visualize in RViz

```bash
ros2 launch ur5_pickplace_description display.launch.py
```

### 2) Run in Gazebo

```bash
ros2 launch ur5_pickplace_description gazebo.launch.py
```

### 3) Start controllers

```bash
ros2 launch ur5_pickplace_controller controller.launch.py
```

### 4) MoveIt

```bash
ros2 launch ur5_pickplace_moveit moveit.launch.py is_sim:=True
```

## Useful Commands

Check that packages are discoverable:

```bash
colcon list
```

Inspect the action interface:

```bash
ros2 interface show ur5_pickplace_msgs/action/Ur5PickplaceTask
```

## Troubleshooting

- `Package not found`: make sure `source install/setup.bash` was executed in the current shell.
- `xacro command not found`: install the `xacro` package.
- Controllers fail to spawn: verify `controller_manager` is running and check YAML in `ur5_pickplace_controller/config`.

## Structure

```text
ur5_pickplace/
├── ur5_pickplace_controller/
├── ur5_pickplace_description/
├── ur5_pickplace_moveit/
├── ur5_pickplace_msgs/
├── ur5_pickplace_py/
├── ur5_pickplace_remote/
└── ur5_pickplace_utils/
```
