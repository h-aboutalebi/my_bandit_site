from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .bandit.MainDiscreteSetting import *


# This is for non-continous environment urls
def sim_ncontinous_env(request):
    context = {'range': range(1, 15)}
    return render(request, 'bandit_simulator/sim_ncontinous_env.html', context)

# This is for about page
def about(request):
    return render(request, 'bandit_simulator/about.html', {})


# This function handles the request sent by sim_ncontinous_env ajax
def handle_sim_ncontinous_env_ajax(request):
    print("Hooora")
    data = request.POST
    response = call_bandit_main(data)
    return JsonResponse(response)


# This function calls the bandit main class to gerate corresponding simulation figures for a given request
def call_bandit_main(data):
    form_data_dictionary = {
        "number_of_experiment": int(data['number_of_experiment']),
        "patient_number": int(data['patient_number']),
        "epsilon_value": float(data['epsilon_value']),
        "mean_value_range": [float(item) for item in data.getlist('range')],
        "reward_tensor": data['reward_tensor'],
        "initial_value": float(data['initial_value']),
        "tau_value": float(data['tau_value']),
        "c_value": float(data['c_value']),
        "alpha_value":float(data['alpha_value']),
        "beta_value": float(data['beta_value'])

    }
    response = main(form_data_dictionary)
    return response
