from setuptools import setup
setup(
        name="APIGtool",
        version='0.1.0',
        packages=['apigtool'],
        description='Collection of APIG Utilities',
        author='Cloud Engineering',
        author_email='chuck.muckamuck@gmail.com',
        install_requires=[
                    "boto3>=1.9",
                    "Click>=7.0",
                    "pymongo>=3.6",
                    "tabulate>=0.8"
                ],
        entry_points="""
            [console_scripts]
            apigtool=apigtool.command:cli
        """
)
