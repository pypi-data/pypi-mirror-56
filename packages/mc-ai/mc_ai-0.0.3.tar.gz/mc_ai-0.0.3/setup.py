from setuptools import setup
setup(
    name='mc_ai',
    version='0.0.3',
    author='魔扣少儿编程_Hugn',
    author_email='wang1183478375@outlook.com',
    url ='https://www.coding4fun.com.cn/',
    install_requires=['urllib3>=1.25.7',
                      'requests>=2.22.0'
                      ],
    data_files=[('',['mc_ai.py'])
                ],
    include_package_data = True, 
    zip_safe=False,
    )