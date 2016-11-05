# -*- coding: utf-8

from django.shortcuts import render
from models import Dictee, Probleme
from forms import DicteeForm

import random
import string
import datetime

# Create your views here.

def acceuil(request):
    return render(request, 'school/acceuil.html', {})

################################  DICTEES  ################################
def dictee_list(request):
    dictees = Dictee.objects.all()
    return render(request, 'school/dictee_list.html', locals())


def is_int(v):
    try:
        int(v)
        return True
    except:
        return False


def is_float(v):
    try:
        float(v)
        return True
    except:
        return False

def format_speak(txt):
    dic_replace_speak = {u'-':u'moins', u'*': u'multiplié par', u"'": u'apostrophe',u'=': u'égal'}
    for o, d in dic_replace_speak.items():
        txt = txt.replace(o,d)
    return txt


def exo_dictee(request, pk):
    dictee = Dictee.objects.get(pk=pk)
    result = None
    list_mots = dictee.text.split(';')
    step = (1000/(3*len(list_mots)))
    nb_ok_de_suite = 0

    if 'list_mots' in request.session:
        list_mots = request.session['list_mots'].split(';')
    if 'position_bipbip' in request.session:
        position_bipbip = request.session['position_bipbip']
    if 'nb_ok_de_suite' in request.session:
        nb_ok_de_suite = request.session['nb_ok_de_suite']
    if request.method == "POST":
        mot = request.session['mot']
        if 'proposition' in request.POST:
            reponse = request.POST['proposition']
            list_lettre= []
            for l in mot:
                list_lettre.append(l)

            if mot == reponse:
                result = True
                txt_a_dire = u"Bravo %s sécrit %s %s" % (mot, ' '.join(list_lettre), ' '*500)
                expected_mot = mot
                position_bipbip += step
                nb_ok_de_suite += 1
                if nb_ok_de_suite > 2:
                    position_bipbip += step


                if list_mots.count(mot) > 1:
                    list_mots.pop(list_mots.index(mot))
                while mot == expected_mot:
                    # passer a un nouveau mot
                    index_mot = random.randint(0, len(list_mots)-1)
                    mot = list_mots[index_mot]

                txt_a_dire = u"%scomment sécrit %s" % (txt_a_dire, mot)
                request.session['mot'] = mot
                request.session['list_mots'] = ';'.join(list_mots)
            else:
                result = False
                nb_ok_de_suite = 0
                txt_a_dire = u"Et non %s sécrit %s" % (mot, u' '.join(list_lettre))
                expected_mot = mot
                list_mots.append(mot)
                list_mots.append(mot)
                request.session['list_mots'] = ';'.join(list_mots)

    else:
        list_mots = dictee.text.split(';')
        index_mot = random.randint(0, len(list_mots)-1)
        mot = list_mots[index_mot]
        txt_a_dire = u"comment sécrit %s" % mot
        position_bipbip = 0
        nb_ok_de_suite = 0
        request.session['mot'] = mot
        request.session['list_mots'] = ';'.join(list_mots)

    if position_bipbip > 1000:
        nb_ok_de_suite = 1000
        position_bipbip = 1000
    request.session['nb_ok_de_suite'] = nb_ok_de_suite
    request.session['position_bipbip'] = position_bipbip

    return render(request, 'school/exo_dictee.html', locals())


def dictee_new(request):
    if request.method == "POST":
        form = DicteeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = datetime.datetime.now()
            post.save()
            dictees = Dictee.objects.all()
            return render(request, 'school/dictee_list.html', locals())
    else:
        form = DicteeForm()
    return render(request, 'school/dictee_new.html', {'form': form})

################################  ALPHABET  ################################
def alphabet_list(request):
    return render(request, 'school/alphabet_list.html', {})


def exo_alphabet(request, level):
    list_alphabet = list(string.ascii_lowercase)


    if request.method == "POST":
        index_lettre = request.session['index_lettre']
        expected_index_lettre = index_lettre
        lettre = list_alphabet[index_lettre]

        if 'Nouveau' in request.POST :
            index_lettre= random.randint(1, len(list_alphabet)-2)
            lettre = list_alphabet[index_lettre]
            result = None
            request.session['index_lettre'] = index_lettre
            return render(request, 'school/exo_alphabet.html', locals())
        if 'Verifier' in request.POST and 'proposition_avant' in request.POST and 'proposition_apres' in request.POST :
            reponse_avant = request.POST['proposition_avant']
            expected_lettre_avant = list_alphabet[expected_index_lettre-1]
            reponse_apres = request.POST['proposition_apres']
            expected_lettre_apres = list_alphabet[expected_index_lettre+1]

            if expected_lettre_avant == reponse_avant and expected_lettre_apres == reponse_apres:
                result = True
                result_avant = True
                result_apres = True
            else:
                result = False
                if expected_lettre_avant == reponse_avant:
                    result_avant = True
                else:
                    result_avant = False

                if expected_lettre_apres == reponse_apres:
                    result_apres = True
                else:
                    result_apres = False
        else:
            result = None

    else:
        index_lettre= random.randint(1, len(list_alphabet)-2)
        lettre = list_alphabet[index_lettre]
        result = None
    request.session['index_lettre'] = index_lettre
    return render(request, 'school/exo_alphabet.html', locals())


def exo_ecrire_alphabet(request, level):
    list_alphabet = list(string.ascii_lowercase)
    if level == '2':
        list_alphabet = list_alphabet[::-1]
        level_txt = u'à l envers'
        level_txt_a_dire = u'à lenvers'
    else:
        level_txt = u''
        level_txt_a_dire = u''

    if request.method == "POST":

        if 'proposition' in request.POST:
            reponse = request.POST['proposition']

            if ''.join(list_alphabet) == reponse.replace(' ', ''):
                result = True
                txt_a_dire = u"Bravo tu connais bien ton alphabet."
                txt_a_ecrire = "Bravo, tu connais bien ton alphabet !"
            else:
                result = False
                txt_a_dire = u"Et non, lalphabet %s est %s" % (level_txt_a_dire,' '.join(list_alphabet))
                txt_a_ecrire = u"Et non, l'alphabet %s est %s" % (level_txt,' '.join(list_alphabet))
    else:
        txt_a_dire = u"Ecrit lalphabet %s sil te plait." % level_txt_a_dire
        txt_a_ecrire = u"Ecrit l'alphabet %s s'il te plait." % level_txt

    return render(request, 'school/exo_ecrire_alphabet.html', locals())

################################  DICTEES  ################################
def math_acceuil(request, type):
    if type == 'calculs':
        return render(request, 'school/math_calculs.html', {})
    elif type == 'problemes':
        problemes = Probleme.objects.all()
        return render(request, 'school/math_probleme_list.html', locals())
    else:
        return render(request, 'school/math_acceuil.html', {})


def math_calcul(request, type, chiffre):

    if request.method == "POST":
        if 'Nouveau' in request.POST :
            # choisir deux nombres au hasard
            a = random.randint(0, 10** int(chiffre))
            b = random.randint(0, 10 ** int(chiffre))
            if type == 'additions':
                op = '+'
            elif type == 'soustractions':
                op = '-'
                if (a < b):
                    tmp= a
                    a = b
                    b = tmp
            elif type == 'multiplications':
                op = '*'
            elif type == 'divisions':
                op = '/'
                tmp = b
                b = a * tmp
            else:
                op ='+'

            question = '%d %s %d = '% (a, op, b)
            request.session['expected_reponse'] = str(eval('%d %s %d'% (a, op, b)))
            request.session['question'] = '%d %s %d'% (a, op, b)
            txt_a_dire = 'combien font %d %s %d' % (a, op, b)
        if 'Verifier' in request.POST:
            reponse = request.POST['proposition']
            expected = request.session['expected_reponse']
            question = request.session['question']
            if reponse == expected:
                result = True
                txt_a_dire = "Bravo, %s  = %s" % (question, expected)
                txt_a_ecrire = "Bravo, %s = %s" % (question, expected)
            else:
                result = False
                txt_a_dire = u"Et non, %s = %s" % (question, expected)
                txt_a_ecrire = u"Et non, %s = %s" % (question, expected)
    else:
        # choisir deux nombres au hasard
        a = random.randint(0, 10** int(chiffre))
        b = random.randint(0, 10** int(chiffre))
        if type == 'additions':
            op = '+'
        elif type == 'soustractions':
            op = '-'
            a = random.randint(b, 10** int(chiffre))
        elif type == 'multiplications':
            op = '*'
        elif type == 'divisions':
            op = '/'
            tmp = b
            b = a * tmp
        else:
            op ='+'

        question = '%d %s %d = '% (a, op, b)
        request.session['expected_reponse'] = str(eval('%d %s %d'% (a, op, b)))
        request.session['question'] = '%d %s %d'% (a, op, b)
        txt_a_dire = u'combien font %d %s %d' % (a, op, b)

    txt_a_dire = format_speak(txt_a_dire)
    return render(request, 'school/math_calcul.html', locals())


def math_probleme_list(request):
    problemes = Probleme.objects.all()
    return render(request, 'school/math_probleme_list.html', locals())

def extract_var(t):
    dic_var = {}
    priority_var = []
    nb_var =  t.count('{')
    for i_var in range(1,nb_var+1):
        var_desc =  t.split('{')[i_var].split('}')[0]
        l_var_desc = var_desc.split('_')
        nom = l_var_desc[0]
        type = l_var_desc[1]
        val_min = l_var_desc[2]
        val_max = l_var_desc[3]
        if is_int(val_min):
            val_min = int(val_min)
        elif is_float(val_min):
            val_min = float(val_min)
        else:
            priority_var.append(val_min)
        if is_int(val_max):
            val_max = int(val_max)
        elif is_float(val_max):
            val_max = float(val_max)
        else:
            priority_var.append(val_max)
        dic_var[nom] = {'nom':nom, 'type':type, 'val_min':val_min, 'val_max':val_max, 'desc': '{'+var_desc+'}'}
    return dic_var, priority_var

def compute_new_var(dic_var, var, txt_a_ecrire,exp_expected ):
    if not is_float(dic_var[var]['val_min']):
        dic_var[var]['val_min'] = dic_var[dic_var[var]['val_min']]['value']
    if not is_float(dic_var[var]['val_max']):
        dic_var[var]['val_max'] = dic_var[dic_var[var]['val_max']]['value']
    if type == 'int':
        var_value = random.randint(dic_var[var]['val_min'], dic_var[var]['val_max'])
    else:
        var_value = random.randrange(dic_var[var]['val_min'], dic_var[var]['val_max'])
    txt_a_ecrire = txt_a_ecrire.replace(dic_var[var]['desc'], str(var_value))
    dic_var[var]['value'] = var_value
    exp_expected = exp_expected.replace(var, str(var_value))

    return dic_var, txt_a_ecrire,exp_expected

def probleme_new_value(probleme):
    dic_var, priority_var = extract_var(probleme.text)
    txt_a_ecrire = probleme.text
    exp_expected = probleme.formule_resultat
    # d'abord les variable utilisé dans le range des autres
    for var in priority_var:
        dic_var, txt_a_ecrire, exp_expected = compute_new_var(dic_var, var, txt_a_ecrire, exp_expected)

    for var in dic_var:
        if 'value' not in dic_var[var]:
            dic_var, txt_a_ecrire, exp_expected = compute_new_var(dic_var, var, txt_a_ecrire,exp_expected)
    # faire le calcul de la valeur attendu
    expected = eval(exp_expected)
    return expected, txt_a_ecrire, exp_expected

def exo_probleme(request, pk):
    probleme = Probleme.objects.get(pk=pk)

    if request.method == "POST":
        if 'Nouveau' in request.POST :
            expected, txt_a_ecrire, exp_expected = probleme_new_value(probleme)
            request.session['expected_reponse'] = str(expected)
            request.session['exp_expected'] = str(exp_expected)
            request.session['question'] = txt_a_ecrire
            return render(request, 'school/exo_probleme.html', locals())

        if 'Verifier' in request.POST:
            reponse = request.POST['proposition']
            expected = request.session['expected_reponse']
            question = request.session['question']
            exp_expected = request.session['exp_expected']
            expected_without_unit = expected.replace(probleme.unite_resultat,'').strip()
            if reponse == expected or reponse == expected_without_unit:
                result = True
                txt_a_dire = u"Bravo, la , la réponse est %s = %s" % (exp_expected, expected)
                txt_a_dire = format_speak(txt_a_dire)
                txt_a_ecrire = u"%s\nBravo, la réponse est %s = %s" % (question, exp_expected, expected)
            else:
                result = False
                txt_a_dire = u"Et non, la bonne réponse est %s = %s" % (exp_expected, expected)
                txt_a_dire = format_speak(txt_a_dire)
                txt_a_ecrire = u"%s\nEt non, la bonne réponse est %s = %s" % (question, exp_expected, expected)
    else:
        expected,txt_a_ecrire, exp_expected = probleme_new_value(probleme)
        if probleme.unite_resultat == 'na':
            probleme.unite_resultat = ''
        request.session['expected_reponse'] = '%s %s' % (str(expected), probleme.unite_resultat)
        request.session['question'] = txt_a_ecrire
        request.session['exp_expected'] = str(exp_expected)

    return render(request, 'school/exo_probleme.html', locals())
