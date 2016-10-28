# -*- coding: utf-8

from django.shortcuts import render
from models import Dictee

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
    list_mots = dictee.text.split()

    if request.method == "POST":
        mot = request.session['mot']
        if 'proposition' in request.POST:
            reponse = request.POST['proposition']
            list_lettre= []
            for l in mot:
                list_lettre.append(l)

            if mot == reponse:
                result = True
                txt_a_dire = u"Bravo %s sécrit %s %s" % (mot,' '.join(list_lettre),' '*500)
                expected_mot = mot
                # passer a un nouveau mot
                index_mot = random.randint(0, len(list_mots)-1)
                mot = list_mots[index_mot]
                txt_a_dire = u"%scomment sécrit %s" % (txt_a_dire,mot)
                request.session['mot'] = mot
            else:
                result = False
                txt_a_dire = u"Et non %s sécrit %s" % (mot,u' '.join(list_lettre))
                expected_mot = mot

    else:
        index_mot = random.randint(0, len(list_mots)-1)
        mot = list_mots[index_mot]
        txt_a_dire = u"comment sécrit %s" % mot
        request.session['mot'] = mot
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
        return render(request, 'school/math_problemes.html', {})
    else:
        return render(request, 'school/math_acceuil.html', {})


def math_calcul(request, type, chiffre):


    if request.method == "POST":
        if 'Nouveau' in request.POST :
            if type == 'additions':
                op = '+'
            elif type == 'soustractions':
                op = '-'
            elif type == 'multiplications':
                op = '*'
            elif type == 'divisions':
                op = '/'
            else:
                op ='+'
            # choisir deux nombres au hasard
            a = random.randint(0, 10** int(chiffre))
            b = random.randint(0, 10 ** int(chiffre))
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
        if type == 'additions':
            op = '+'
        elif type == 'soustractions':
            op = '-'
        elif type == 'multiplications':
            op = '*'
        elif type == 'divisions':
            op = '/'
        else:
            op ='+'
        # choisir deux nombres au hasard
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        question = '%d %s %d = '% (a, op, b)
        request.session['expected_reponse'] = str(eval('%d %s %d'% (a, op, b)))
        request.session['question'] = '%d %s %d'% (a, op, b)
        txt_a_dire = u'combien font %d %s %d' % (a, op, b)
    txt_a_dire = txt_a_dire.replace(u'*', u'multiplié par')
    return render(request, 'school/math_calcul.html', locals())

