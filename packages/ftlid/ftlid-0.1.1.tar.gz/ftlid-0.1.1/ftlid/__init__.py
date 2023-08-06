import fasttext
import os

__version__ = '0.1.1'
DIRNAME = os.path.dirname(os.path.abspath(__file__))


def identify_language(text, model=None, model_path=None, with_prob=False,
                      **kwargs):
    """
    Identifies language the provided text is written in using a pre-trained
    fastText model. Except for the arguments listed below, any keyword
    arguments are passed further to fastText's predict function.

    Args:
        - text: The text whose language is to be identified.
        - model (optional): Provides an instance of a fastText model used for
          prediction. Defaults to lid.176.ftz which is included in the package.
          At most one of the model and model_path arguments can be provided.
        - model_path (optional): Provides path to the fastText model used for
          prediction. Defaults to lid.176.ftz which is included in the package.
          At most one of the model and model_path arguments can be provided.
        - with_prob (optional): If True, the function returns both predicted
          languages and their probabilities. Defaults to False.
    """
    if model is None:
        if model_path is not None:
            model = load_model(model_path)
        else:
            model = DEFAULT_MODEL
    elif model_path is not None:
        raise ValueError("Unsure which model to use. At most one of the model "
                         "and model_path arguments can be provided")

    # ensure newline is escaped
    text = text.replace('\n', '\\n')

    p = model.predict(text, **kwargs)
    label = [x.replace('__label__', '') for x in p[0]]

    if with_prob:
        return label, p[1]
    return label[0] if len(label) == 1 else label


def load_model(model_path):
    """
    Loads a fastText model from disk. Use this method to get a model to be
    passed to the identify_language function. This will prevent the model from
    being loaded on every request.

    Args:
        - model_path: Provides path to the fastText model to load.
    """
    return fasttext.load_model(model_path)


DEFAULT_MODEL = load_model(os.path.join(DIRNAME, 'lid.176.ftz'))
