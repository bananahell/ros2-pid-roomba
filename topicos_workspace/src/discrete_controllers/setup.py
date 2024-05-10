from setuptools import find_packages, setup

package_name = 'discrete_controllers'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Pedro Nogueira',
    maintainer_email='cmcg89034@gmail.com',
    description='A roomba that moves forward and turns whenever faced with something!',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'roomba = discrete_controllers.roomba:main',
        ],
    },
)
