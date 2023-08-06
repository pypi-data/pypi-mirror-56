import fasttext
import os

__version__ = '0.1.0'
DIRNAME = os.path.dirname(os.path.abspath(__file__))


def identify_language(text, model_path=None, with_prob=False, **kwargs):
    """
    Identifies language the provided text is written in using a pre-trained
    fastText model. Except for the arguments listed below, anky keyword
    arguments are fassed further to fastText's predict function.

    Args:
        - text: The text whose language is to be identified.
        - model_path (optional): Provides path to the fastText model used for
          prediction. Defaults to lid.176.ftz which is included in the package.
        - with_prob (optional): If True, the function returns both predicted
          languages and their probabilities. Defaults to False.
    """
    if model_path is None:
        model_path = DIRNAME + '/lid.176.ftz'
    model = fasttext.load_model(model_path)
    # ensure newline is escaped
    text = text.replace('\n', '\\n')

    p = model.predict(text, **kwargs)
    label = [x.replace('__label__', '') for x in p[0]]

    if with_prob:
        return label, p[1]
    return label[0] if len(label) == 1 else label
