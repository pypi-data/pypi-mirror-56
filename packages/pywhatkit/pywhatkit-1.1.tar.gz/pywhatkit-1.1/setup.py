from distutils.core import setup
import setuptools

def readme():
    with open(r'C:\Users\pc\Desktop\pywhatkit\README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'pywhatkit',
    packages = setuptools.find_packages(),
    version = '1.1',
    license='MIT',
    description = 'pywhatkit is a Python library for Sending whatsapp message at certain time and some other stuffs.',   # Give a short description about your library
    author = 'Ankit Raj Mahapatra',                   # Type in your name
    author_email = 'ankitrajjitendra816@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/Ankit404butfound/awesomepy',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/Ankit404butfound/awesomepy/archive/1.0.tar.gz',    # I explain this later on
    keywords = ['sendwhatmsg', 'info', 'playonyt', 'search'],   # Keywords that define your package best
    install_requires=[           
          'pyautogui',
          'beautifulsoup4',
          'wikipedia',
          'requests',
          'pyttsx3',
      ],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)
