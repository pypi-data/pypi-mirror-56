import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(name='chatWrapper',
      version='0.1',
      description='Wrapper for Chat API: https://os-chat-api.herokuapp.com/',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/duggalrd/chat_api_wrapper',
      author='Rahul Duggal',
      author_email='duggalr42@gmail.com',
      license='MIT',
      packages=['chatWrapper'],
      zip_safe=False)
