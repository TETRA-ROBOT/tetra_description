from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration

def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value="true")

    return LaunchDescription([
        use_sim_time_arg,
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('tetra_description'),
                    'launch',
                    'tetra_description.launch.py'
                ])
            ]),
            launch_arguments={
                'robot_model': 's',
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }.items()
        )
    ])
