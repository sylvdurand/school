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
    if 'mot' in request.session:
        expected_mot = request.session['mot']
    result = None
    list_mots = dictee.text.split()
    index_mot = random.randint(0, len(list_mots)-1)
    mot = list_mots[index_mot]

    if request.method == "POST":
        expected_mot = request.session['mot']
        if 'proposition' in request.POST:
            reponse = request.POST['proposition']
            expected_mot = request.session['mot']
            if expected_mot == reponse:
                result = True
            else:
                result = False
                mot = expected_mot

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