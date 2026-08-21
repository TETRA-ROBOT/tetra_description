import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value="true", description="Use simulation clock if true")
    robot_model_arg = DeclareLaunchArgument('robot_model', default_value="m", description="TETRA robot model (m, h, edu, mh, s, sm)")

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': Command([
                'xacro ',
                PathJoinSubstitution([
                    FindPackageShare('tetra_description'),
                    'urdf',
                    'tetra_robot.urdf.xacro',
                ]),
                ' robot_model:=',
                LaunchConfiguration('robot_model'),
            ]),
        }]
    )

    ld.add_action(use_sim_time_arg)
    ld.add_action(robot_model_arg)
    ld.add_action(rsp_node)

    return ld
