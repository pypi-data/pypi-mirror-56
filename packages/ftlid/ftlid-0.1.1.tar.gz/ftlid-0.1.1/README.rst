ftlid
=====

A simple answer to your language identification needs, powered by `fastText
<https://fasttext.cc/>`_. It wraps the `language identification model
<https://fasttext.cc/docs/en/language-identification.html>`_ in a small
Python package for easier use.

Install
-------

.. code::

    pip install ftlid

Example
-------

.. code:: python


    from ftlid import identify_language, load_model

    # prints 'en'
    print(identify_language('Hello, how are you?'))

    # prints (['en'], array([0.99987388]))
    print(identify_language('Hello, how are you?', with_prob=True))

    # prints ['en', 'de']
    print(identify_language('And then he said "Ich liebe dich"!', k=2))

    # prints (['en', 'de'], array([0.50208992, 0.30427793]))
    print(identify_language('And then he said "Ich liebe dich"!', with_prob=True, k=2))

    # if you want to use your custom model
    print(identify_language('Hello, how are you?', model_path='model.ftz'))

    # if you would like to pass the model yourself or prevent it from being loaded on every request
    model = load_model('model.ftz')
    print(identify_language('Hello, how are you?', model=model))


License
-------

Licensed under the MIT license (see `LICENSE <./LICENSE>`_ file for more
details).
