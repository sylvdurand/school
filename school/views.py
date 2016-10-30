# -*- coding: utf-8

from django.shortcuts import render
from models import Dictee, Probleme

import random
import string

# Create your views here.

def acceuil(request):
    return render(request, 'school/acceuil.html', {})

################################  DICTEES  ################################
def dictee_list(request):
    dictees = Dictee.objects.all()
    return render(request, 'school/dictee_list.html', locals())


def exo_dictee(request, pk):
    dictee = Dictee.objects.get(pk=pk)
    result = None
    list_mots = dictee.text.split(';')
    if 'list_mots' in request.session:
        list_mots = request.session['list_mots'].split(';')
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
        request.session['mot'] = mot
        request.session['list_mots'] = ';'.join(list_mots)
    return render(request, 'school/exo_dictee.html', locals())


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
    txt_a_dire = txt_a_dire.replace(u'*', u'multiplié par')
    txt_a_dire = txt_a_dire.replace(u'-', u'moins')
    return render(request, 'school/math_calcul.html', locals())


def math_probleme_list(request):
    problemes = Probleme.objects.all()
    return render(request, 'school/math_probleme_list.html', locals())

def extract_var(t):
    dic_var = {}
    nb_var =  t.count('{')
    for i_var in range(1,nb_var+1):
        var_desc =  t.split('{')[i_var].split('}')[0]
        l_var_desc = var_desc.split('_')
        type = l_var_desc[0]
        nom = l_var_desc[1]
        nb_decimal = l_var_desc[2].count('X')
        dic_var[nom] = {'nom':nom, 'type':type, 'nb_decimal':nb_decimal, 'desc': '{'+var_desc+'}'}
    return dic_var

def exo_probleme(request, pk):
    probleme = Probleme.objects.get(pk=pk)

    if request.method == "POST":
        if 'Nouveau' in request.POST :
            dic_var = extract_var(probleme.text)
            txt_a_ecrire = probleme.text
            exp_expected = probleme.formule_resultat
            for var in dic_var:
                var_value = random.randint(0, 10**dic_var[var]['nb_decimal'])
                txt_a_ecrire = txt_a_ecrire.replace(dic_var[var]['desc'],str(var_value))
                dic_var[var]['value'] = var_value
                exp_expected = exp_expected.replace(var,str(var_value))
            expected = eval(exp_expected)
            request.session['expected_reponse'] = str(expected)
            request.session['question'] = txt_a_ecrire
            return render(request, 'school/exo_probleme.html', locals())

        if 'Verifier' in request.POST:
            reponse = request.POST['proposition']
            expected = request.session['expected_reponse']
            question = request.session['question']
            expected_without_unit = expected.replace(probleme.unite_resultat,'').strip()
            if reponse == expected or reponse == expected_without_unit:
                result = True
                txt_a_dire = u"Bravo, %s la réponse est %s" % (question, expected)
                txt_a_ecrire = u"Bravo, %s la réponse est %s" % (question, expected)
            else:
                result = False
                txt_a_dire = u"Et non, %s la bonne réponse est %s" % (question, expected)
                txt_a_ecrire = u"Et non, %s la bonne réponse est %s" % (question, expected)
    else:
        dic_var = extract_var(probleme.text)
        txt_a_ecrire = probleme.text
        exp_expected = probleme.formule_resultat
        for var in dic_var:
            var_value = random.randint(0, 10**dic_var[var]['nb_decimal'])
            txt_a_ecrire = txt_a_ecrire.replace(dic_var[var]['desc'],str(var_value))
            dic_var[var]['value'] = var_value
            exp_expected = exp_expected.replace(var,str(var_value))
        expected = eval(exp_expected)
        request.session['expected_reponse'] = '%s %s' % (str(expected), probleme.unite_resultat)
        request.session['question'] = txt_a_ecrire
    return render(request, 'school/exo_probleme.html', locals())
