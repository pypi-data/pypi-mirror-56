# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['maru',
 'maru.factory',
 'maru.feature',
 'maru.feature.extractor',
 'maru.grammeme',
 'maru.lemmatizer',
 'maru.pymorphy',
 'maru.pymorphy.grammeme',
 'maru.resource',
 'maru.resource.crf',
 'maru.resource.linear',
 'maru.resource.rnn',
 'maru.tagger',
 'maru.utils',
 'maru.vectorizer',
 'maru.vectorizer.sparse']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.2.2,<3.0.0',
 'lru-dict>=1.1.6,<2.0.0',
 'numpy>=1.15.0,<2.0.0',
 'pymorphy2[fast]>=0.8,<0.9',
 'python-crfsuite>=0.9.5,<0.10.0',
 'scikit-learn>=0.19.0,<0.20.0',
 'scipy>=1.1.0,<2.0.0',
 'tensorflow>=1.9.0,<1.15.0']

extras_require = \
{'gpu': ['tensorflow-gpu>=1.9.0,<1.15.0']}

setup_kwargs = {
    'name': 'maru',
    'version': '0.1.2',
    'description': 'Morphological Analyzer for Russian 💬',
    'long_description': "MARu: Morphological Analyzer for Russian\n========================================\n\n\n.. image:: https://img.shields.io/pypi/v/maru.svg\n    :target: https://pypi.python.org/pypi/maru\n    :alt: Package version\n\n.. image:: https://img.shields.io/pypi/l/maru.svg\n    :target: https://pypi.python.org/pypi/maru\n    :alt: Package license\n\n.. image:: https://img.shields.io/pypi/pyversions/maru.svg\n    :target: https://pypi.python.org/pypi/maru\n    :alt: Python versions\n\n.. image:: https://travis-ci.org/chomechome/maru.svg?branch=master\n    :target: https://travis-ci.org/chomechome/maru\n    :alt: TravisCI status\n\n.. image:: https://codecov.io/github/chomechome/maru/coverage.svg?branch=master\n    :target: https://codecov.io/github/chomechome/maru\n    :alt: Code coverage\n\n.. image:: https://codeclimate.com/github/chomechome/maru/badges/gpa.svg?branch=master\n    :target: https://codeclimate.com/github/chomechome/maru\n    :alt: Code quality\n\n\n---------------\n\n**MARu** is a morphological analyzer for Russian, written in Python, powered by machine learning and neural networks.\n\nInstallation\n------------\n\n::\n\n    $ pipenv install maru\n\nor\n\n::\n\n    $ pipenv install maru[gpu]\n\nfor installation with Tensorflow GPU support.\n\nYou can also just use `pip` (though you should definitely take a look at `pipenv <https://pipenv.readthedocs.io/en/latest/>`_).\n\n\nWhat's in the Box?\n------------------\n\n.. image:: https://sociorocketnewsen.files.wordpress.com/2013/10/maru-top.jpg?w=580&h=305&crop=1\n\n- ✨ Morphological analysis with contextual disambiguation using `Universal Dependencies <http://universaldependencies.org/u/feat/index.html>`_ tags.\n- 🌈 Trained via various machine learning methods: linear model, CRF, deep neural network.\n- 🔮 Speed/accuracy trade-off between different methods.\n- 🍰 Vocabulary-based lemmatization, built on top of `pymorphy2 <https://github.com/kmike/pymorphy2>`_.\n\n\nUsage\n-----\n\nFirst, create a `maru.analyzer.Analyzer <https://github.com/chomechome/maru/blob/master/maru/analyzer.py#L13-L36>`_ object using the factory method:\n\n.. code-block:: python\n\n    >> import maru\n    >> analyzer = maru.get_analyzer(tagger='crf', lemmatizer='pymorphy')\n\nThen, analyze some text:\n\n.. code-block:: python\n\n    >> analyzed = analyzer.analyze(['мама', 'мыла', 'раму'])  # note that this returns an iterator\n    >> for morph in analyzed:\n    ...     print(morph)\n    ...\n    Morph(word='мама', lemma='мама', tag=Tag(pos=NOUN,animacy=Anim,case=Nom,gender=Fem,number=Sing))\n    Morph(word='мыла', lemma='мыть', tag=Tag(pos=VERB,aspect=Imp,gender=Fem,mood=Ind,number=Sing,tense=Past,verbform=Fin,voice=Act))\n    Morph(word='раму', lemma='рама', tag=Tag(pos=NOUN,animacy=Inan,case=Acc,gender=Fem,number=Sing))\n\nOther available taggers that you can pass to ``maru.get_analyzer`` are ``'linear'``, ``'rnn'``, and ``'pymorphy'``.\nAnother available lemmatizer is ``'dummy'`` (no actual lemmatization, slightly improves inference speed).\n\nYou can refer to the following table when choosing an algorithm to use:\n\n+-----------------------------------------------------------------------------------------------------+\n|                    Full tag accuracy (per token, per sentence) and inference speed                  |\n+----------+--------+--------+--------+--------+--------+--------+--------+--------+------------------+\n| Tagger   |   News (Lenta)  |   Social (VK)   | Literature (JZ) |       All       | Inference speed  |\n+==========+========+========+========+========+========+========+========+========+==================+\n| Pymorphy | 77.24% | 12.85% | 72.71% | 18.84% | 73.16% | 10.91% | 74.43% | 14.85% | 49000 tokens/sec |\n+----------+--------+--------+--------+--------+--------+--------+--------+--------+------------------+\n| Linear   | 95.00% | 61.73% | 91.64% | 59.51% | 93.00% | 57.87% | 93.26% | 59.62% | 26500 tokens/sec |\n+----------+--------+--------+--------+--------+--------+--------+--------+--------+------------------+\n| CRF      | 95.55% | 64.53% | 91.82% | 61.27% | 93.59% | 63.96% | 93.70% | 62.95% |  5500 tokens/sec |\n+----------+--------+--------+--------+--------+--------+--------+--------+--------+------------------+\n| RNN      | 97.65% | 79.33% | 95.43% | 75.88% | 95.84% | 73.60% | 96.34% | 76.14% |  1000 tokens/sec |\n+----------+--------+--------+--------+--------+--------+--------+--------+--------+------------------+\n\nAccuracy was measured on the `MorphoRuEval-2017 <https://github.com/dialogue-evaluation/morphoRuEval-2017>`_ test set.\nInference speed was estimated on a system with 32 GB RAM, Intel i7 6700K as CPU and GeForce GTX 1060 as GPU.\nRNN performance is given for single sentence inference on GPU. An addition of batch inference in the future can greatly improve it.\n",
    'author': 'Vladislav Blinov',
    'author_email': 'cunningplan@yandex.ru',
    'url': 'https://github.com/chomechome/maru',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
