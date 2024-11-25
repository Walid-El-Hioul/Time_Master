from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name="time_master",
  version="1.0.0",
  author="Walid El-Hioul",
  author_email="walidelhioul0000@gmail.com",
  description="A comprehensive time and task management system with CLI interface",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Walid-El-Hioul/Time_Master",
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: End Users/Desktop",
      "Topic :: Office/Business :: Scheduling",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Environment :: Console",
  ],
  python_requires=">=3.7",
  install_requires=[
      # None
  ],
  entry_points={
      "console_scripts": [
          "time_master=time_master:main",
      ],
  },
  package_data={
      "time_master": ["schedule/*.json", "tasks/*.json"],
  },
  include_package_data=True,
  keywords="time management, task management, scheduling, CLI, productivity",
  project_urls={
      "Bug Reports": "https://github.com/Walid-El-Hioul/Time_Master/issues",
      "Source": "https://github.com/Walid-El-Hioul/Time_Master",
  },
)