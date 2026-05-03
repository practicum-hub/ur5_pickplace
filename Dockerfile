FROM osrf/ros:humble-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV ROS_WS=/root/ur5_ws

SHELL ["/bin/bash", "-c"]

# Base tooling for ROS workspace builds
RUN apt-get update && apt-get install -y \
    git \
    python3-rosdep \
    python3-colcon-common-extensions \
    python3-vcstool \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-joint-state-publisher \
    ros-humble-moveit \
    ros-humble-moveit-ros-planning-interface \
    ros-humble-moveit-configs-utils \
    && rm -rf /var/lib/apt/lists/*

# Prepare workspace and copy project packages
RUN mkdir -p ${ROS_WS}/src
WORKDIR ${ROS_WS}/src
COPY . ${ROS_WS}/src

# Install ROS dependencies from package manifests
WORKDIR ${ROS_WS}
RUN apt-get update && \
    rosdep update --rosdistro=${ROS_DISTRO} && \
    rosdep install --from-paths src --ignore-src -r -y \
      --rosdistro=${ROS_DISTRO} \
      --skip-keys=moveit_commander

# Build workspace
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --symlink-install

# Auto-source ROS + workspace in interactive shells
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "source ${ROS_WS}/install/setup.bash" >> /root/.bashrc

WORKDIR ${ROS_WS}
CMD ["bash"]
