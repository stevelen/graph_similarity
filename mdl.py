from math import floor
from scipy.optimize import newton
import autograd.numpy as np
from autograd import grad 


import math

def choose(n, k):
    if 0 < k <= n:
        p = 1
        for i in range(0, min(k, n-k)-1):
            p = floor((p * (n-i)) / (i+1))
        return p
    else:
        return 0

def log2(n):
    return math.log2(n)


def log2_zero(n):
    if n == 0:
        return 0
    else:
        return log2(n)

def log2_choose(n, k):
    if n == 0 or k == 0:
        return 0
    else:
        return log2_zero(choose(n, k))

def log2_star(n):
    if n <= 1:
        return 0
    else:
        return 1 + log2_star(log2(n))

def unviversal_integer(n):
    NORMALIZATION_CONSTANT = 2.865064
    if n <= 0:
        return 0
    c = log2(NORMALIZATION_CONSTANT)
    logstar_n = log2_star(n)
    return logstar_n + c

def update_total_description_length(model):
    model.total_description_length = sum(model.macro_stucture_desc_length) + model.edge_probability_description_length_maxent + model.structure_type_description_length

def update_variable_terms(model):
    optimize_maxent(model)
    update_description_length(model)

def optimize_maxent(model):
    n_iter = 50
    td = grad(grad(lagrange_dual_equiv))
    result = newton(td, model.lambdas, args=(model,), maxiter=n_iter, tol=1e-8)
    model.last_optimization_result = result
    model.lambdas = model.last_optimization_result.minimizer
    model.entropy = model.last_optimization_result.minimum
    if !converged(result)
        log_progress!(M, "NO CONVERGENCE AFTER $(n_iter) ITERATIONS")
    end

def lagrange_dual_equiv(lambdas, model):
    return (get_first_term(lambdas, model) - get_second_term(lambdas, model))


def get_first_term(lambdas, model):
    rest_lambda = lambdas[0]
    if model.edge_equivalence_classes == {}:
        model.maximum_m_loopy * math.log(get_normalizer(rest_lambda))
    else:
        lambda_total_contribution = 0
        lambda_total_sizes = 0
        for equivalence_class_key in model.edge_equivalence_classes:
            size = get_equiv_size(equivalence_class_key, model.edge_equivalence_classes)
            lambda_sum = get_lambda_sum_from_equiv(equivalence_class_key, lambdas)
            normalized_sum = get_normalizer(lambda_sum)
            contribution = math.log(normalized_sum)
            lambda_total_contribution += size * contribution
            lambda_total_sizes += size
        rest_class_n = model.maximum_m_loopy - lambda_total_sizes
        rest_contribution = rest_class_n * math.log(get_normalizer(rest_lambda))
        return lambda_total_contribution + rest_contribution

def get_second_term(lambdas, model):
    second_term = 0
    for lam, constraint_value in zip(lambdas, model.constraint_values):
        second_term += lam * constraint_value
    return second_term



def get_normalizer(lambda_sum):
    return (1 + math.exp(lambda_sum))

def get_equiv_size(eqv_class_key, eqv_class):
    return len(eqv_class[eqv_class_key])

def get_lambda_sum_from_equiv(equivalence_class_key, lambdas):
    lambda_sum = 0
    for idx in equivalence_class_key:
        lambda_sum += lambdas[idx]
    return lambda_sum 






