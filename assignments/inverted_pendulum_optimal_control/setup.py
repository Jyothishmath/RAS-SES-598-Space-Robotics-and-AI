from setuptools import setup
import os
from glob import glob

package_name = 'inverted_pendulum_optimal_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
        (os.path.join('share', package_name, 'models/inverted_pendulum'), 
         glob('models/inverted_pendulum/*.urdf')),
        (os.path.join('share', package_name, 'models/inverted_pendulum/meshes'), 
         glob('models/inverted_pendulum/meshes/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Instructor',
    maintainer_email='instructor@university.edu',
    description='ROS2 package for inverted pendulum control using LQR',
    license='Creative Commons Attribution 4.0',
    entry_points={
        'console_scripts': [
            'lqr_controller = inverted_pendulum_optimal_control.lqr_controller:main',
            'earthquake_force_generator = inverted_pendulum_optimal_control.earthquake_force_generator:main',
            'force_visualizer = inverted_pendulum_optimal_control.force_visualizer:main',
            'state_republisher = inverted_pendulum_optimal_control.state_republisher:main',
        ],
    },
)
