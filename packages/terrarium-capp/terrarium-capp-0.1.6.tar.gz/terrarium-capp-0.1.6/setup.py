# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': '.'}

packages = \
['terrarium', 'terrarium.utils']

package_data = \
{'': ['*'], 'terrarium': ['summary/*']}

install_requires = \
['arrow>=0.15.4,<0.16.0',
 'colorama>=0.4.1,<0.5.0',
 'dill>=0.2.9,<0.3.0',
 'fire==0.1.3',
 'pandas>=0.24.2,<0.25.0',
 'pydent==0.1.5a8',
 'uvloop>=0.12.2,<0.13.0',
 'validator.py>=1.3,<2.0',
 'webcolors>=1.9,<2.0']

entry_points = \
{'console_scripts': ['terrarium = terrarium.cli:main']}

setup_kwargs = {
    'name': 'terrarium-capp',
    'version': '0.1.6',
    'description': 'Adaptive Computer Aided Process Planner',
    'long_description': '# Terrarium\n\n[![PyPI version](https://badge.fury.io/py/terrarium-capp.svg)](https://badge.fury.io/py/terrarium-capp)\n\nTerrarium is a [dynamic computer-aided process planner (CAPP)](https://en.wikipedia.org/wiki/Computer-aided_process_planning) for biology designed for agile manufacturing of biological products, such as E Coli & Yeast strains, or Mammalian cell lines.\n\nThis piece of software automatically plans scientific experiments in Aquarium using historical\nplanning data and current laboratory inventory. Data can be pulled from specific researchers\nto emulate how that particular researcher would plan experiments.\n\n## Requirements\n\n* development version of **trident (v0.1.0)**\n* Python >= 3.6\n* Aquarium login credentials\n\n## Usage\n\nInstalling a specific version\n\n```python\npip install terrarium-capp==0.1.5\n```\n\nNew models can be built as in the following:\n\n```python\nfrom pydent import AqSession\nfrom terrarium import AutoPlannerModel\nproduction = AqSession("login", "pass", "url")\n\n# pull last 300 experimental to build model\nmodel = AutoPlannerModel(production, depth=300)\nmodel.build()\nmodels.save(\'terrarium.pkl\')\n```\n\nSaved models can be open later:\n\n```python\nmodel = AutoPlannerModel.load(\'terrarium.pkl\')\n```\n\nWhat protocols the model uses can be adjusted using filters:\n\n```python\nignore_ots = production.OperationType.where({"category": ["Control Blocks", "Library Cloning"], "deployed": True})\nignore_ots += production.OperationType.where({"name": "Yeast Mating"})\nignore_ots += production.OperationType.where({"name": "Yeast Auxotrophic Plate Mating"})\nignore = [ot.id for ot in ignore_ots]\nmodel.add_model_filter("AllowableFieldType", lambda m: m.field_type.parent_id in ignore)\n```\n\nSample composition:\n\n```python\nsample_composition = nx.DiGraph()\n\n# build a new yeast strain from a plasmid, which is comprised of several fragments\nedges = [\n     (\'DTBA_backboneA_splitAMP\', \'pyMOD-URA-URA3.A.1-pGPD-yeVenus-tCYC1\'),\n     (\'T1MC_NatMX-Cassette_MCT2 (JV)\', \'pyMOD-URA-URA3.A.1-pGPD-yeVenus-tCYC1\'),\n     (\'BBUT_URA3.A.0_homology1_UTP1 (from genome)\', \'pyMOD-URA-URA3.A.1-pGPD-yeVenus-tCYC1\'),\n     (\'DH5alpha\', \'pyMOD-URA-URA3.A.1-pGPD-yeVenus-tCYC1\'),\n     (\'TP-IRES-EGFP-TS\', \'pyMOD-URA-URA3.A.1-pGPD-yeVenus-tCYC1\' ),\n     (\'pyMOD-URA-URA3.A.1-pGPD-yeVenus-tCYC1\', \'CEN.PK2 - MAT alpha | his-pGRR-W5-W8-RGR-W36\'),\n]\n\nfor n1, n2 in edges:\n    s1 = browser.find_by_name(n1)\n    s2 = browser.find_by_name(n2)\n    sample_composition.add_node(s1.id, sample=s1)\n    sample_composition.add_node(s2.id, sample=s2)\n    sample_composition.add_edge(s1.id, s2.id)\n```\n\n```python\nignore_items = []  # optional to not include certain items in the search.\ndesired_object_type = production.ObjectType.find_by_name(\'Fragment Stock\')\ncost, paths, graph = network.run(desired_object_type, ignore=ignore_items)\n```\n\n```python\n# make a new plan\ncanvas = Planner(production)\n\n# add protocols from optimized network to plan\nnetwork.plan(paths, graph, canvas)\n\n# submit to Aquarium\ncanvas.create()\n```\n\n**Example of Planning Yeast Construction**\n\n![plan_example](assets/images/plan_example0.png)\n\n**Probability Matrix of Connecting Aquarium Protocols**\n\nThe autoplanner uses this type of data, in concert with the `sample_composition` network,\nto build an optimal experiment.\n\n![all_connections](assets/images/all_op_types.png)\n\n**Top 50 Connections**\n\n![top_50_connections](assets/images/top_50_optypes.png)\n\n## Model Factory\n\n```python\nfactory = ModelFactory(session)\n\n# make a model from a single user\nmodel1 = factory.emulate(\'user1\').build()\n\n# make a model from a group of users\nuser_group = [\'user2\', \'user3\']\nmodel2 = factory.emulate(user_group).build()\n\n# make a model from the last 100 plans\nmodel3 = factory.new(100).build()\n\n# compose a weighted model\nmodel = model1 + model2 * 3\n```\n\n## Future Version\n\n* estimate convidence for certain inventory items or operations based on\npast success rate\n* better api for\n* using \'ghost\' plans to build model\n* emulating specific users / user groups\n** faster execution (currently ~45-60 seconds)\n\n## License\n\nFeb. 4, 2019 - This software is not currently licensed. The author (Justin D. Vrana of University of Washington) does not grant permission to copy or modify code base.\n',
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'url': 'https://www.github.com/jvrana/Terrarium',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
