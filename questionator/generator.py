import json
import random

from leitner.models import Daroo
from questionator.conts.brand_names import names
from questionator.conts.iranian_generic import products


def which_is_brand_name_for(daroo):
    options = []
    options.extend(random.sample(names, 3))
    daroo_bns = json.loads(daroo.tradeNames)
    options.append(random.choice(daroo_bns))
    print(options)
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_bns
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a trade name for {json.loads(daroo.name)}?',
        'options': fina_options,
        'category': 'which_is_brand_name_for'
    }


def which_is_dosage_form_for(daroo):
    options = []
    options.extend(random.sample(products, 3))
    daroo_doses = json.loads(daroo.iranianGenericProducts)
    options.append(random.choice(daroo_doses))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_doses
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a iranian dosage form for {json.loads(daroo.name)}?',
        'options': fina_options,
        'category': 'which_is_dosage_form_for'
    }