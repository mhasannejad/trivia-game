import json
import random
from itertools import islice

from leitner.models import Daroo
from questionator.conts.brand_names import names
from questionator.conts.clinical_attentions import prescriptions
from questionator.conts.dnames import daroo_names
from questionator.conts.categories import pharma_categories, treatment_categories
from questionator.conts.indications import indications
from questionator.conts.intractions import attentions
from questionator.conts.iranian_generic import products
from questionator.conts.pregnency import preg_categories
from questionator.conts.training import training_points


def which_is_brand_name_for(daroo):
    options = []
    options.extend(random.sample(names, 3))
    daroo_bns = json.loads(daroo.tradeNames)
    options.append(random.choice(daroo_bns))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_bns
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a trade name for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
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
        'question': f'which is a iranian dosage form for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'category': 'which_is_dosage_form_for',
        'daroo_id': daroo.id,
    }


def which_is_daroo_for_brand_name(daroo):
    options = []
    options.extend(random.sample(daroo_names, 3))
    daroo_trade_names = json.loads(daroo.tradeNames)
    options.append(json.loads(daroo.name))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in json.loads(daroo.name) or json.loads(daroo.name) in i
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is generic name for {random.choice(daroo_trade_names)}?',
        'options': fina_options,
        'category': 'which_is_dosage_form_for',
        'daroo_id': daroo.id,
    }


def which_is_correct_pregnancy_category_for(daroo):
    options = []
    options.extend(random.sample(preg_categories, 3))
    options.append(json.loads(daroo.pregnancyCategory))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i == json.loads(daroo.pregnancyCategory)
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is pregnancy category for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'category': 'which_is_daroo_for_brand_name',
        'daroo_id': daroo.id,
    }


def which_is_correct_pharmacologic_category_for(daroo):
    options = []
    options.extend(random.sample(pharma_categories, 3))
    daroo_category = json.loads(daroo.pharmacologyCategory)
    options.append(json.loads(daroo.pharmacologyCategory))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in json.loads(daroo.pharmacologyCategory) or json.loads(daroo.pharmacologyCategory) in i
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is correct pharmacologic category for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'category': 'which_is_correct_pregnancy_category_for',
        'daroo_id': daroo.id,
    }


def which_is_a_treatment_category_for_daroo(daroo):
    options = []
    options.extend(random.sample(treatment_categories, 3))
    daroo_bns = json.loads(daroo.treatmentCategory)
    options.append(random.choice(daroo_bns))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_bns
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a treatment category for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_treatment_category_for_daroo'
    }


def which_is_a_indication_for_daroo(daroo):
    options = []
    options.extend(random.sample(indications, 3))
    daroo_inds = json.loads(daroo.indications)
    options.append(random.choice(list(daroo_inds.keys())))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_inds
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is an indication for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_indication_for_daroo'
    }


def which_is_a_mechanism_for_daroo(daroo):
    options = []
    options.extend(random.sample(indications, 3))
    daroo_mechs = list(json.loads(daroo.pharmacoDynamics)['mechanism'].items())
    chosen_mech = random.choice(daroo_mechs)
    options.append(f'{chosen_mech[0]} => {chosen_mech[1]}')
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in f'{chosen_mech[0]} => {chosen_mech[1]}' or f'{chosen_mech[0]} => {chosen_mech[1]}' in i
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a correct mechanism for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_mechanism_for_daroo'
    }


def which_is_a_attention_case_for_daroo(daroo):
    options = []
    options.extend(random.sample(attentions, 3))
    daroo_attns = json.loads(daroo.sideEffects)
    options.append(random.choice(daroo_attns['attention']))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_attns['attention']
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a attention case for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_treatment_category_for_daroo'
    }


def which_is_a_prescription_attention_case_for_daroo(daroo):
    options = []
    options.extend(random.sample(prescriptions, 3))
    daroo_attns = json.loads(daroo.clinicalAttentions)
    options.append(random.choice(daroo_attns['prescription']))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_attns['prescription']
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a prescription attention case for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_prescription_attention_case_for_daroo'
    }


def which_is_a_prescription_tracking_point_case_for_daroo(daroo):
    options = []
    options.extend(random.sample(prescriptions, 3))
    daroo_attns = json.loads(daroo.clinicalAttentions)
    options.append(random.choice(daroo_attns['tracking']))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_attns['tracking']
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a a correct tracking point for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_prescription_tracking_point_case_for_daroo'
    }


def random_refer_to_daroo(daroo):
    name = ''
    rand = random.choice(range(1))
    if rand == 0:
        name = json.loads(daroo.name)
    elif rand == 1:
        name = random.choice(json.loads(daroo.tradeNames))

    return name


def which_is_a_correct_training_point_for(daroo):
    options = []
    options.extend(random.sample(training_points, 3))
    daroo_bns = json.loads(daroo.trainings)
    options.append(random.choice(daroo_bns))
    fina_options = []
    for i in options:
        fina_options.append({
            'option': i,
            'is_right': i in daroo_bns
        })
    random.shuffle(fina_options)
    return {
        'question': f'which is a correct training point for {random_refer_to_daroo(daroo)}?',
        'options': fina_options,
        'daroo_id': daroo.id,
        'category': 'which_is_a_correct_training_point_for'
    }
