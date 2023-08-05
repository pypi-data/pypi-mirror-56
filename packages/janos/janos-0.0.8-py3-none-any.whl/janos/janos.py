# -*- coding: utf-8 -*-
"""
@authors:
David Bergman
Teng Huang
Phil Brooks
Andrea Lodi
Arvind U Raghunathan

Some rights reserved.
"""

import time
import numpy as np
import math
import sys
import numbers
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from gurobipy import *
import matplotlib.pyplot as plt


class JANOS:
    """
    Attributes | Parameters
    """
    MIN_DOUBLE_VAL = -10000000.0
    MAX_DOUBLE_VAL = 10000000.0
    EPSILON = 0.00000001
    BIG_M = 5000.0

    def get_min_double_val(self):
        return self.MIN_DOUBLE_VAL

    def get_max_double_val(self):
        return self.MAX_DOUBLE_VAL

    def get_epsilon(self):
        return self.EPSILON

    def get_big_m(self):
        return self.BIG_M

    def set_min_double_val(self, new_val):
        if isinstance(new_val, numbers.Number):
            self.MIN_DOUBLE_VAL = new_val
        else:
            print("Error: MIN_DOUBLE_VAL must be numbers.")
            sys.exit(1)

    def set_max_double_val(self, new_val):
        if isinstance(new_val, numbers.Number):
            self.MAX_DOUBLE_VAL = new_val
        else:
            print("Error: MAX_DOUBLE_VAL must be numbers.")
            sys.exit(1)

    def set_epsilon(self, new_val):
        if isinstance(new_val, numbers.Number):
            self.EPSILON = new_val
        else:
            print("Error: EPSILON must be numbers.")
            sys.exit(1)

    def set_big_m(self, new_val):
        if isinstance(new_val, numbers.Number):
            self.BIG_M = new_val
        else:
            print("Error: BIG_M must be numbers.")
            sys.exit(1)


def is_binary(series, allow_na=False):
    if allow_na:
        series.dropna(inplace=True)
    return sorted(series.unique()) == [0, 1]


def calc_average_sigmoid_value(a, b):
    """
    reference: https://math.stackexchange.com/questions/2365763/integrating-logistic-functions
    """
    if a > b:
        # print("a must be less than or equal to b when calculating average sigmoid value ..." )
        sys.exit(1)
    if a == b:
        # print("WARNING: calculating the average values of a sigmoid function on an interval of size 0 ... " )
        return math.exp(a) / (1 + math.exp(a))
    return 1/(b-a) * (np.log(1+math.exp(b)) - np.log(1+math.exp(a)))


def calc_sigmoid_value(a):
    return math.exp(a) / (1 + math.exp(a))


def calc_inverse_sigmoid(a):
    if not isinstance(a, numbers.Number):
        max_val = max(list(a))
        min_val = min(list(a))
    else:
        max_val = a
        min_val = a

    if max_val >= 1:
        # print("Cannot do inverse of sigmoid for value above 1 ... " )
        sys.exit(1)
    if min_val <= 0:
        # print("Cannot do inverse of sigmoid for value below 0 ... " )
        sys.exit(1)
    return np.log(a/(1-a))


class JModel:
    """
    MEMBER FUNCTIONS
    """
    def solve(self):

        # print("Solving the model ... ")

        self.start_learning_time = time.time()
        self.learn_models()
        self.end_learning_time = time.time()

        self.start_optimization_time = time.time()
        self.optimize()
        self.end_optimization_time = time.time()

        self.end_time = time.time()

    def learn_models(self):

        # print("Learning predictive models ... ")

        for i in range(len(self.optimization_pms)):
            self.optimization_pms[i].train_opt_pm()

    def optimize(self):
        # print("Optimizing ... " )
        try:
            model = Model(self.model_name)

            for rv_index in range(len(self.__regularVariablesLong)):

                if self.__regularVariablesLong[rv_index].variable_type == "discrete":
                    for domain_index in range(len(self.__regularVariablesLong[rv_index].discrete_domain)):
                        self.__w[rv_index, domain_index] = model.addVar(vtype=GRB.BINARY, name=self.__regularVariablesLong[rv_index].name + "_w[[" + str(domain_index) + "]]")
                    self.__x[rv_index] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=self.__regularVariablesLong[rv_index].name)
                else:
                    self.__x[rv_index] = model.addVar(vtype=GRB.CONTINUOUS, lb=self.__regularVariablesLong[rv_index].lower_bound, ub=self.__regularVariablesLong[rv_index].upper_bound, name=self.__regularVariablesLong[rv_index].name)
            for pv_index in range(len(self.__predictedVariablesLong)):
                self.__y[pv_index] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=self.__predictedVariablesLong[pv_index].name)

            model.update()

            """
            Associate binary w with continuous x
            only needed for discrete variables
            """

            for rv_index in range(len(self.__regularVariablesLong)):
                if self.__regularVariablesLong[rv_index].variable_type == "discrete":
                    projection_expr = LinExpr(0.0)

                    one_w_expr = LinExpr(0.0)
                    for domain_index in range(len(self.__regularVariablesLong[rv_index].discrete_domain)):
                        projection_expr += self.__regularVariablesLong[rv_index].discrete_domain[domain_index] * self.__w[rv_index, domain_index]
                        one_w_expr += self.__w[rv_index, domain_index]
                    model.addConstr(self.__x[rv_index] == projection_expr)
                    model.addConstr(one_w_expr == 1)

            """
            Put constraints
            """
            for con_index in range(len(self.__constraints)):

                con_expr = LinExpr(0.0)

                for term_index in range(len(self.__constraints[con_index].con_expr.expression_terms)):
                    var_vector_index = self.__regularVariablesLong.index(self.__constraints[con_index].con_expr.expression_terms[term_index].regular_var)
                    value_in_coeff = self.__constraints[con_index].con_expr.expression_terms[term_index].value
                    con_expr += value_in_coeff * self.__x[var_vector_index]

                if self.__constraints[con_index].sense == 'less_equal':
                    model.addConstr(con_expr <= self.__constraints[con_index].rhs)
                elif self.__constraints[con_index].sense == 'equal':
                    model.addConstr(con_expr == self.__constraints[con_index].rhs)
                else:
                    model.addConstr(con_expr >= self.__constraints[con_index].rhs)

            """
            Connect regular variables with predictive variables
            """
            for pv_index in range(len(self.__predictedVariablesLong)):

                """
                Neural Network
                """
                if isinstance(self.__predictedVariablesLong[pv_index].opm.optimization_pm, MLPRegressor):
                    this_pm = self.__predictedVariablesLong[pv_index].opm
                    for node in range(this_pm.n_nodes):
                        self.__pre_relu_value[pv_index, node] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=self.__predictedVariablesLong[pv_index].name + "_pre[[" + str(node) + "]]")
                        self.__post_relu_value[pv_index, node] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=self.__predictedVariablesLong[pv_index].name + "_post[[" + str(node) + "]]")
                        self.__need_activation_func[pv_index, node] = model.addVar(vtype=GRB.BINARY, name=self.__predictedVariablesLong[pv_index].name + "_actFun[[" + str(node) + "]]")
                    model.update()

                    """
                    obtain the detail of the predictive model
                    """
                    predicted_model_for_var = self.__predictedVariablesLong[pv_index].opm.optimization_pm
                    opt_pm_for_var = self.__predictedVariablesLong[pv_index].opm
                    nn_coefs = predicted_model_for_var.coefs_
                    nn_intercepts = predicted_model_for_var.intercepts_

                    """
                    generate matrices W and B and A
                    """

                    """
                    initialize the matrices W and A
                    """
                    W = np.zeros((this_pm.n_nodes, this_pm.n_nodes), dtype=float)
                    A = np.zeros((this_pm.n_nodes, this_pm.n_nodes), dtype=int)

                    for layer in range(this_pm.n_layers - 1):
                        for i in range(this_pm.layers_sizes[layer]):
                            for j in range(this_pm.layers_sizes[layer + 1]):
                                A[i + this_pm.offset[layer], j + this_pm.offset[layer + 1]] = 1
                                W[i + this_pm.offset[layer], j + this_pm.offset[layer + 1]] = nn_coefs[layer][i][j]

                    """
                    initialize vector B
                    """
                    B = np.zeros(this_pm.n_inputs, dtype=float).tolist()
                    for layer in range(this_pm.n_layers - 1):
                        B += nn_intercepts[layer].tolist()

                    W = np.around(W, decimals=6)
                    B = np.around(B, decimals=6)

                    """
                    Constructing matrices W, B and A
                    """

                    for node in range(this_pm.n_nodes):

                        if this_pm.nodes_locations[node] == 0:
                            """
                            input layer
                            """
                            model.addConstr(self.__pre_relu_value[pv_index, node] == self.__post_relu_value[pv_index, node])

                            feature_index = node

                            # print("feature_index : ", feature_index)
                            # print("opt_pm_for_var.feature_names[feature_index] = ", opt_pm_for_var.feature_names[feature_index])
                            # print("pv_index : ", pv_index)
                            # print("variable_mapping[opt_pm_for_var.feature_names : ", self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])
                            if isinstance(self.__predictedVariablesLong[pv_index].variable_mapping[
                                              opt_pm_for_var.feature_names[feature_index]], RegularVariable):
                                rv_index = self.__regularVariablesLong.index(self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])
                                model.addConstr(self.__pre_relu_value[pv_index, node] == self.__x[rv_index])
                            else:
                                model.addConstr(self.__pre_relu_value[pv_index, node] == self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])

                        elif this_pm.nodes_locations[node] == this_pm.n_layers - 1:
                            """
                            output layer
                            """
                            model.addConstr(self.__pre_relu_value[pv_index, node] == self.__post_relu_value[pv_index, node])

                            incoming_arcs = LinExpr(0.0)
                            for j in range(node):
                                if A[j][node] == 1:
                                    incoming_arcs += W[j][node] * self.__post_relu_value[pv_index, j]
                            model.addConstr(self.__pre_relu_value[pv_index, node] == incoming_arcs + B[node])

                        else:
                            """
                            hidden layers
                            """

                            incoming_arcs = LinExpr(0.0)
                            for j in range(node):
                                if A[j][node] == 1:
                                    incoming_arcs += W[j][node] * self.__post_relu_value[pv_index, j]
                            model.addConstr(self.__pre_relu_value[pv_index, node] == incoming_arcs + B[node])

                            model.addConstr(self.__post_relu_value[pv_index, node] <= JANOS.BIG_M * self.__need_activation_func[pv_index, node] + JANOS.EPSILON)
                            model.addConstr(self.__post_relu_value[pv_index, node] >= 0.0)

                            model.addConstr(self.__pre_relu_value[pv_index, node] <= JANOS.BIG_M * self.__need_activation_func[pv_index, node])
                            model.addConstr(self.__pre_relu_value[pv_index, node] >= -1.0 * JANOS.BIG_M * (1 - self.__need_activation_func[pv_index, node]) + JANOS.EPSILON)

                            model.addConstr(self.__post_relu_value[pv_index, node] <= self.__pre_relu_value[pv_index, node] + JANOS.BIG_M * (1 - self.__need_activation_func[pv_index, node]) + JANOS.EPSILON)
                            model.addConstr(self.__post_relu_value[pv_index, node] >= self.__pre_relu_value[pv_index, node] - JANOS.BIG_M * (1 - self.__need_activation_func[pv_index, node]) - JANOS.EPSILON)

                    model.addConstr(self.__y[pv_index] == self.__post_relu_value[pv_index, this_pm.n_nodes-1])


                """
                Linear regression
                """
                if isinstance(self.__predictedVariablesLong[pv_index].opm.optimization_pm, LinearRegression):

                    predictive_model_for_var = self.__predictedVariablesLong[pv_index].opm.optimization_pm
                    opt_pm_for_var = self.__predictedVariablesLong[pv_index].opm

                    lin_regr_expr = LinExpr(0.0)
                    for feature_index in range(len(opt_pm_for_var.feature_names)):
                        # print("feature_index : ", feature_index)
                        # print("feature_name : ", opt_pm_for_var.feature_names[feature_index])
                        # print("predictive_model_for_var.coef_ : ", predictive_model_for_var.coef_)
                        # print("predictive_model_for_var.coef_[feature_index] : ",
                        #       predictive_model_for_var.coef_[0][feature_index])
                        if isinstance(self.__predictedVariablesLong[pv_index].variable_mapping[
                                          opt_pm_for_var.feature_names[feature_index]], RegularVariable):
                            rv_index = self.__regularVariablesLong.index(self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])
                            lin_regr_expr += predictive_model_for_var.coef_[0][feature_index] * self.__x[rv_index]
                        else:

                            # print("input : ", self.__predictedVariablesLong[pv_index].variable_mapping[
                            #               opt_pm_for_var.feature_names[feature_index]])
                            # print("multiplication : ", predictive_model_for_var.coef_[0][feature_index] * self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])
                            lin_regr_expr += predictive_model_for_var.coef_[0][feature_index] * self.__predictedVariablesLong[pv_index].variable_mapping[
                                          opt_pm_for_var.feature_names[feature_index]]

                    lin_regr_expr += predictive_model_for_var.intercept_
                    model.addConstr(lin_regr_expr == self.__y[pv_index])


                """
                Logistic regression
                """
                if isinstance(self.__predictedVariablesLong[pv_index].opm.optimization_pm, LogisticRegression):

                    n_intervals_discretization = self.__predictedVariablesLong[pv_index].opm.n_breakpoints  # TODO: Make this dynamic

                    predictive_model_for_var = self.__predictedVariablesLong[pv_index].opm.optimization_pm
                    opt_pm_for_var = self.__predictedVariablesLong[pv_index].opm

                    max_value_lin_expr = 0.0
                    min_value_lin_expr = 0.0

                    for feature_index in range(len(opt_pm_for_var.feature_names)):
                        if isinstance(self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]], RegularVariable):
                            rv_index = self.__regularVariablesLong.index(self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])
                            if predictive_model_for_var.coef_[0][feature_index] > 0:
                                max_value_lin_expr += predictive_model_for_var.coef_[0][feature_index] * self.__regularVariablesLong[rv_index].upper_bound
                                min_value_lin_expr += predictive_model_for_var.coef_[0][feature_index] * self.__regularVariablesLong[rv_index].lower_bound
                            else:
                                max_value_lin_expr += predictive_model_for_var.coef_[0][feature_index] * self.__regularVariablesLong[rv_index].lower_bound
                                min_value_lin_expr += predictive_model_for_var.coef_[0][feature_index] * self.__regularVariablesLong[rv_index].upper_bound
                        else:
                            max_value_lin_expr += predictive_model_for_var.coef_[0][feature_index] * self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]]
                            min_value_lin_expr += predictive_model_for_var.coef_[0][feature_index] * self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]]

                    b = max_value_lin_expr + predictive_model_for_var.intercept_
                    a = min_value_lin_expr + predictive_model_for_var.intercept_

                    breakpoints_for_probs = np.linspace(calc_sigmoid_value(a), calc_sigmoid_value(b), n_intervals_discretization)
                    breakpoints_for_lin_expr = np.apply_along_axis(calc_inverse_sigmoid, 0, breakpoints_for_probs)

                    self.__z[pv_index] = model.addVars(n_intervals_discretization-1, vtype=GRB.BINARY, name="z[" + str(pv_index) + "]")

                    model.update()

                    """
                    Pick at most one z
                    """
                    one_z_expr = LinExpr(0.0)
                    for interval_index in range(n_intervals_discretization-1):
                        one_z_expr += self.__z[pv_index][interval_index]
                    model.addConstr(one_z_expr == 1)

                    exp_argument_expr = LinExpr(0.0)
                    for feature_index in range(len(opt_pm_for_var.feature_names)):
                        if isinstance(self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]], RegularVariable):
                            rv_index = self.__regularVariablesLong.index(self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]])
                            exp_argument_expr += predictive_model_for_var.coef_[0][feature_index] * self.__x[rv_index]
                        else:
                            exp_argument_expr += predictive_model_for_var.coef_[0][feature_index] * self.__predictedVariablesLong[pv_index].variable_mapping[opt_pm_for_var.feature_names[feature_index]]

                    exp_argument_expr += predictive_model_for_var.intercept_

                    """
                    link linear expression with binaries
                    """
                    for interval_index in range(n_intervals_discretization-1):
                        model.addConstr((breakpoints_for_lin_expr[interval_index] - a[0]) * self.__z[pv_index][interval_index] + a[0] <= exp_argument_expr)
                        model.addConstr((breakpoints_for_lin_expr[interval_index+1] - b[0]) * self.__z[pv_index][interval_index] + b[0] >= exp_argument_expr)

                    """
                    link breakpoints with probs
                    """
                    model.addConstr(0 <= self.__y[pv_index])
                    model.addConstr(1 >= self.__y[pv_index])

                    min_prob = calc_sigmoid_value(a)
                    max_prob = calc_sigmoid_value(b)
                    model.addConstr(min_prob <= self.__y[pv_index])
                    model.addConstr(max_prob >= self.__y[pv_index])

                    for interval_index in range(n_intervals_discretization-1):
                        prob_val = calc_average_sigmoid_value(breakpoints_for_lin_expr[interval_index], breakpoints_for_lin_expr[interval_index+1])
                        model.addConstr(min_prob + (prob_val - min_prob - JANOS.EPSILON) * self.__z[pv_index][interval_index] <= self.__y[pv_index])
                        model.addConstr(max_prob + (prob_val - max_prob + JANOS.EPSILON) * self.__z[pv_index][interval_index] >= self.__y[pv_index])

            model.update()

            """
            Setting objective
            """

            obj_expr = LinExpr(0.0)

            for rv_index in range(len(self.__regularVariablesLong)):
                obj_expr += self.__regularVariablesLong[rv_index].objective_coefficient * self.__x[rv_index]
            for pv_index in range(len(self.__predictedVariablesLong)):
                obj_expr += self.__predictedVariablesLong[pv_index].objective_coefficient * self.__y[pv_index]

            model.setObjective(obj_expr, GRB.MAXIMIZE)

            """
            Associate
            """

            if self.write_lp_model:
                if self.get_lp_model_filename() != "":
                    model.write(self.get_lp_model_filename())
                else:
                    model.write("ipmodel.lp")
            model.setParam("TimeLimit", self.get_time_limit())  # OR: model.setParam.TimeLimit = self.get_time_limit()
            model.setParam("OutputFlag", self.get_output_flag())
            for key, value in self.gurobi_param_settings.items():
                model.setParam(key, value)

            model.optimize()
            self.gurobi_model = model

        except GurobiError as e:
            print('Gurobi error ' + str(e.errno) + ": " + str(e.message))

    def get_simulated_objVal(self):
        return self.simulations

    def gen_simulated_objVal(self):
        produce_interval = False
        for pv_index in range(len(self.__predictedVariablesLong)):
            # print(pv_index, self.__predictedVariablesLong[pv_index].opm.SE)
            if self.__predictedVariablesLong[pv_index].opm.SE < 0:
                """
                get out
                """
                produce_interval = False
                break
            else:
                if pv_index == len(self.__predictedVariablesLong) - 1:
                    produce_interval = True
                else:
                    continue

        if produce_interval:

            simulate_objVals = []

            for i in range(self.get_simulation_times()):
                simulate_objVal = 0.0

                for rv_index in range(len(self.__regularVariablesLong)):
                    simulate_objVal += self.__regularVariablesLong[rv_index].objective_coefficient * self.__x[rv_index].X

                for pv_index in range(len(self.__predictedVariablesLong)):
                    if isinstance(self.__predictedVariablesLong[pv_index].opm.optimization_pm, LogisticRegression):
                        pred_prob = self.__y[pv_index].X
                        Xb = math.log(pred_prob) - math.log(1 - pred_prob) + np.random.normal(loc=0.0, scale=
                        self.__predictedVariablesLong[pv_index].opm.SE)
                        simu_prob = math.exp(Xb) / (1 + math.exp(Xb))
                        simulate_objVal += self.__predictedVariablesLong[pv_index].objective_coefficient * simu_prob
                    else:
                        y_value = self.__y[pv_index].X + np.random.normal(loc=0, scale=self.__predictedVariablesLong[pv_index].opm.SE)
                        simulate_objVal += self.__predictedVariablesLong[pv_index].objective_coefficient * y_value

                simulate_objVals.append(simulate_objVal)
            self.simulations = simulate_objVals

            print("==> The {0}% and {1}% percentiles are : ({2}, {3})".format(self.get_left_percentile_for_output(),
                                                                          self.get_right_percentile_for_output(), round(
                    np.percentile(simulate_objVals, self.get_left_percentile_for_output()), self.decimals), round(
                    np.percentile(simulate_objVals, self.get_right_percentile_for_output()), self.decimals)))

            array_simulated_objVals = np.asarray(simulate_objVals)
            select_for_plot = array_simulated_objVals[
                (array_simulated_objVals >= np.percentile(simulate_objVals, self.get_left_percentile_for_plot())) & (
                            array_simulated_objVals <= np.percentile(simulate_objVals,
                                                                     self.get_right_percentile_for_plot()))]
            plt.figure(figsize=(8, 6))
            plt.hist(select_for_plot)
            plt.xlabel("Simulated Objective Values")
            plt.ylabel("Frequency")
            plt.title("The simulated objective values from {0}% to {1}% percentiles".format(self.get_left_percentile_for_plot(),
                                                                                    self.get_right_percentile_for_plot()))

            """
            (Teng) Here, write to file is recommended to be in front of show().
            Otherwise, some warning and a blank file.
            """
            if self.get_plot_in_file():
                if self.get_plot_filename() == "":
                    plt.savefig("simulated_objVal.png")
                else:
                    plt.savefig(self.get_plot_filename())
            if self.get_plot_on_screen():
                plt.show()
        else:
            print("==> JANOS is unable to generate the {0}% and {1}% percentiles without sample data.".format(
                self.get_left_percentile_for_output(), self.get_right_percentile_for_output()))

    def get_output_flag(self):
        return self.output_flag

    def set_output_flag(self, flag):
        if flag != 0 & flag != 1:
            print("OutputFlag must be 1 or 0.")
            sys.exit(1)
        self.output_flag = flag

    def get_best_solution(self):
        # print("Getting best solution ... ")
        reg_var = []
        for rv_index in range(len(self.__regularVariablesLong)):
            reg_var.append(round(self.__x[rv_index].X, self.decimals))
        pred_var = []
        for pv_index in range(len(self.__predictedVariablesLong)):
            pred_var.append(round(self.__y[pv_index].X, self.decimals))

        return {"regular": reg_var,
                "predicted": pred_var}  # TODO: change the text into variable names

    def get_value(self):
        # print("Getting best value ... ")
        return round(self.gurobi_model.objVal, self.decimals)

    def get_time(self):
        # print("Getting total solution time ... ")
        # print("Total time: ", self.end_time - self.start_time)
        return self.end_time - self.start_time

    def get_time_limit(self):
        # print("Getting time limit ... ")
        # print("Time limit: ", self.optimization_time_limit)
        return self.optimization_time_limit

    def get_time_learn(self):
        # print("Getting learning time ... ")
        # print("Learning time: ", self.end_learning_time - self.start_learning_time)
        return self.end_learning_time - self.start_learning_time

    def get_time_solve(self):
        # print("Getting optimization time ... ")
        # print("Learning time: ", self.end_optimization_time - self.start_optimization_time)
        return self.end_optimization_time - self.start_optimization_time

    def get_predictive_models(self):
        # print("Printing details about predicive models ... ")
        pred_models = []
        for pv_index in range(len(self.__predictedVariablesLong)):
            pred_models.append(self.__predictedVariablesLong[pv_index].opm.optimization_pm)
        return pred_models

    def get_optimization_details(self):
        """
        Teng on Sep 13, 2019: What's this?
        :return:
        """
        print("Getting details about the optimization run ... ")
        print("TO DO ... ")

    def set_optimization_model(self):
        """
        Teng on Sep 13, 2019: What's this?
        :return:
        """
        print("Setting optimization model ... ")
        print("TO DO ... ")

    def set_optimization_time_limit(self, new_val):
        # print("Setting optimization time limit ... ")
        if not isinstance(new_val, numbers.Number):
            print("Setting a non-numeric time limit ... ")
            sys.exit(1)
        if new_val < 5.0:
            print("Setting time limit lower than 5 seconds which is not allowed ... ")
            sys.exit(1)
        self.optimization_time_limit = new_val

    def get_number_of_regular_variables(self):
        # print("Getting number of regular variables ... ")
        return len(self.__regularVariablesLong)

    def get_number_of_predicted_variables(self):
        # print("Getting number of predicted variables ... ")
        return len(self.__predictedVariablesLong)

    def get_regular_variables(self):
        return self.__x

    def get_predicted_variables(self):
        return self.__y

    """
    MODELING ELEMENT FUNCTIONS
    """

    def add_predicted_variables(self, dimensions, name):
        # print("Adding predicted variables ... ")

        if name in self.names_assigned_to_variables:
            print("Cannot add two variables with the same name ... ")
            sys.exit(1)

        """
        Check all conditions
        """
        if not isinstance(dimensions, list):
            print("Adding predictive variables where the dimensions are not a list ... ")
            sys.exit(1)
        for i in range(len(dimensions)):
            if not isinstance(dimensions[i], int):
                print("A dimension is not an integer ... " )
                sys.exit(1)
            if dimensions[i] < 1:
                print("A dimension is less than 1 ... " )
                sys.exit(1)
        if not isinstance(name, str):
            print("Variable name not a string ... " )
            sys.exit(1)
        if len(dimensions) >= 5:
            print("Trying to add a variable with 5 or more dimensions which is currently not allowed ... ")
            sys.exit(1)

        """
        All conditions satisfied so adding variables to the model
        """

        new_variables = list()
        if len(dimensions) == 1:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = PredictedVariable(self, name, [d1])
                self.__predictedVariablesLong.append(new_variables[d1])
        if len(dimensions) == 2:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = [None]*dimensions[1]
                for d2 in range(dimensions[1]):
                    new_variables[d1][d2] = PredictedVariable(self, name, [d1, d2])
                    self.__predictedVariablesLong.append(new_variables[d1][d2])
        if len(dimensions) == 3:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = [None]*dimensions[1]
                for d2 in range(dimensions[1]):
                    new_variables[d1][d2] = [None]*dimensions[2]
                    for d3 in range(dimensions[2]):
                        new_variables[d1][d2][d3] = PredictedVariable(self, name, [d1, d2, d3])
                        self.__predictedVariablesLong.append(new_variables[d1][d2][d3])
        if len(dimensions) == 4:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = [None]*dimensions[1]
                for d2 in range(dimensions[1]):
                    new_variables[d1][d2] = [None]*dimensions[2]
                    for d3 in range(dimensions[2]):
                        new_variables[d1][d2][d3] = [None]*dimensions[3]
                        for d4 in range(dimensions[3]):
                            new_variables[d1][d2][d3][d4] = PredictedVariable(self, name, [d1, d2, d3, d4])
                            self.__predictedVariablesLong.append(new_variables[d1][d2][d3][d4])

        self.__predictedVariables.append(new_variables)
        self.names_assigned_to_variables.append(name)
        return new_variables

    def add_regular_variables(self, dimensions, name):
        # print("Adding regular variables ... ")

        if name in self.names_assigned_to_variables:
            print("Cannot add two variables with the same name ... ")
            sys.exit(1)

        """
        Check all conditions
        """
        if not isinstance(dimensions, list):
            print("Adding regular variables where the dimensions are not a list ... ")
            sys.exit(1)
        for i in range(len(dimensions)):
            if not isinstance(dimensions[i], int):
                print("A dimension is not an integer ... " )
                sys.exit(1)
            if dimensions[i] < 1:
                print("A dimension is less than 1 ... " )
                sys.exit(1)
        if not isinstance(name, str):
            print("Variable name not a string ... " )
            sys.exit(1)
        if len(dimensions) >= 5:
            print("Trying to add a variable with 5 or more dimensions which is currently not allowed ... ")
            sys.exit(1)

        """
        All conditions satisfied so adding variables to the model
        """

        new_variables = list()
        if len(dimensions) == 1:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = RegularVariable(name, [d1], self)
                self.__regularVariablesLong.append(new_variables[d1])
        if len(dimensions) == 2:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = [None]*dimensions[1]
                for d2 in range(dimensions[1]):
                    new_variables[d1][d2] = RegularVariable(name, [d1, d2], self)
                    self.__regularVariablesLong.append(new_variables[d1][d2])
        if len(dimensions) == 3:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = [None]*dimensions[1]
                for d2 in range(dimensions[1]):
                    new_variables[d1][d2] = [None]*dimensions[2]
                    for d3 in range(dimensions[2]):
                        new_variables[d1][d2][d3] = RegularVariable(name, [d1, d2, d3], self)
                        self.__regularVariablesLong.append(new_variables[d1][d2][d3])
        if len(dimensions) == 4:
            new_variables = [None]*dimensions[0]
            for d1 in range(dimensions[0]):
                new_variables[d1] = [None]*dimensions[1]
                for d2 in range(dimensions[1]):
                    new_variables[d1][d2] = [None]*dimensions[2]
                    for d3 in range(dimensions[2]):
                        new_variables[d1][d2][d3] = [None]*dimensions[3]
                        for d4 in range(dimensions[3]):
                            new_variables[d1][d2][d3][d4] = RegularVariable(name, [d1, d2, d3, d4], self)
                            self.__regularVariablesLong.append(new_variables[d1][d2][d3][d4])

        self.__regularVariables.append(new_variables)
        self.names_assigned_to_variables.append(name)
        return new_variables

    def add_constraint(self, con_expr, sense, rhs):
        if not isinstance(con_expr, Expression):
             print("First argument in add constraint must be an expression ... ")
             sys.exit(1)
        if sense not in ['less_equal', 'equal', 'greater_equal']:
             print("Second argument in add constraint must be less_equal, equal, or greater_equal ... ")
             sys.exit(1)
        if not isinstance(rhs, numbers.Number):
             print("Third argument in add constraint must be a value ... ")
             sys.exit(1)
        new_expr = Expression()
        # print(len(new_expr.expression_terms))
        for i in range(len(con_expr.expression_terms)):
            new_expr.add_term(con_expr.expression_terms[i].regular_var, con_expr.expression_terms[i].value)

        self.__constraints.append(Constraint(new_expr, sense, rhs))

    def add_pretrained_pm(self, pretrained_model):
        self.optimization_pms.append(pretrained_model)

    def add_optimization_pm(self, input_df, dependent_var):

        if dependent_var not in list(input_df.columns):
            print("Dependent variable of optimization predicted variable is not a column in input data ... ")
            sys.exit(1)

        new_opt_pm = OptimizationPredictiveModel(input_df, dependent_var)
        self.optimization_pms.append(new_opt_pm.optimization_pm)

    def set_model_name(self, new_model_name):
        if isinstance(new_model_name, str):
            self.model_name = new_model_name
        else:
            print("model name must be string")
            sys.exit(1)

    def get_model_name(self):
        return self.model_name

    def set_left_percentile_for_output(self, percentile):
        if isinstance(percentile, numbers.Number):
            self.left_percentile_for_output = percentile
        else:
            print("percentile must be an integer.")
            sys.exit(1)

    def get_left_percentile_for_output(self):
        return self.left_percentile_for_output

    def set_right_percentile_for_out(self, percentile):
        if isinstance(percentile, numbers.Number):
            self.right_percentile_for_output = percentile
        else:
            print("percentile must be an integer.")
            sys.exit(1)

    def get_right_percentile_for_output(self):
        return self.right_percentile_for_output

    def set_left_percentile_for_plot(self, percentile):
        if isinstance(percentile, numbers.Number):
            self.left_percentile_for_plot = percentile
        else:
            print("percentile must be an integer.")
            sys.exit(1)

    def get_left_percentile_for_plot(self):
        return self.left_percentile_for_plot

    def set_right_percentile_for_plot(self, percentile):
        if isinstance(percentile, numbers.Number):
            self.right_percentile_for_plot = percentile
        else:
            print("percentile must be an integer.")
            sys.exit(1)

    def get_right_percentile_for_plot(self):
        return self.right_percentile_for_plot

    def set_plot_on_screen(self, decision):
        if isinstance(decision, bool):
            self.make_plot_on_screen = decision
        else:
            print("Decision needs to be True or False.")
            sys.exit(1)

    def get_plot_on_screen(self):
        return self.make_plot_on_screen

    def set_plot_in_file(self, decision):
        if isinstance(decision, bool):
            self.output_plot_in_file = decision
        else:
            print("Decision must be True or False.")
            sys.exit(1)

    def get_plot_in_file(self):
        return self.output_plot_in_file

    def set_plot_filename(self, filename):
        if isinstance(filename, str):
            self.plot_filename = filename
        else:
            print("Filename must be string.")
            sys.exit(1)

    def get_plot_filename(self):
        return self.plot_filename

    def set_simulation_times(self, n):
        if isinstance(n, numbers.Number):
            self.n_simulations = n
        else:
            print("n should be numbers.")
            sys.exit(1)

    def get_simulation_times(self):
        return self.n_simulations


    def set_decimals(self, decimal):
        if isinstance(decimal, numbers.Number):
            self.decimals = decimal
        else:
            print("Decimal must be integer.")
            sys.exit(1)

    def get_decimals(self):
        return self.decimals

    """
    CONSTRUCTORS
    """

    def __init__(self, opt_model_name=None):
        # print("Creating a model ... " )
        if opt_model_name is None:
            self.model_name = "my_first_janos_model"
        else:
            self.model_name = opt_model_name
        self.__regularVariables =               list()  # protected variable list
        self.__regularVariablesLong =           list()  # protected long version
        self.__predictedVariables =             list()
        self.__predictedVariablesLong =         list()
        self.__constraints =                    list()
        self.__objectiveFunction =              list()
        self.solution_pool =                    list()
        self.best_known_solution =              list()

        self.optimization_time_limit =          3600.0

        self.start_time =                       time.time()
        self.end_time =                         time.time()
        self.start_learning_time =              time.time()
        self.end_learning_time =                time.time()
        self.start_optimization_time =          time.time()
        self.end_optimization_time =            time.time()

        self.names_assigned_to_variables =      []

        self.start_time =                       time.time()
        self.PMs =                              []

        self.optimization_pms =                 []

        self.left_percentile_for_output = 25
        self.right_percentile_for_output = 75
        self.left_percentile_for_plot = 25
        self.right_percentile_for_plot = 75
        self.make_plot_on_screen = True
        self.output_plot_in_file = True
        self.plot_filename = ""

        self.n_simulations = 1000  # for prediction intervals

        self.decimals = 2  # for all output numbers
        self.write_lp_model = False
        self.lp_model_filename = ""

        self.gurobi_param_settings = {}
        self.output_flag = 1

        self.gurobi_model = None
        self.simulations = []

        """
        variables for regular variables (needed for all)
        """
        self.__w = {}  # binaries for each regular variable
        self.__x = {}  # continuous projection for x

        """
        variables for logistic regression
        """
        self.__y = {}  # predicted variables
        self.__z = {}  # binary discretized variables

        """
        variables for neural network
        """
        self.__pre_relu_value = {}  # continuous
        self.__post_relu_value = {}  # continuous
        self.__need_activation_func = {}  # binary

    def add_gurobi_param_settings(self, key, value):
        if not isinstance(key, str):
            print("parameters are strings.")
            sys.exit(1)
        self.gurobi_param_settings[key] = value
#        print(self.gurobi_param_settings)
#        sys.exit(1)

    def set_write_lp_model(self, write_lp_model):
        self.write_lp_model = write_lp_model

    def get_write_lp_model(self):
        return self.write_lp_model

    def set_lp_model_filename(self, filename):
        self.lp_model_filename = filename

    def get_lp_model_filename(self):
        return self.lp_model_filename


class OptimizationPredictiveModel:
    """
    Teng on Sep 12, 2019:
        the NN parameters maybe could be set and get here.
    """
    def train_opt_pm(self):
        """
        Teng on Sep 12, 2019:
        add checking PM names;
        :return:
        """
        if self.optimization_pm is None:
            """
            PM is not specified
            """
            if self.model_type is None:
                """
                User didn't specify the model they want to use.
                """
                if is_binary(self.input_df[self.dependent_var]):
                    # print("Learning a logistic regression model .. " )
                    predictive_model = LogisticRegression(solver='lbfgs')
                    predictive_model.fit(self.input_df.drop(self.dependent_var, axis=1), self.input_df[self.dependent_var])

                    """
                    add for estimating standard error (SE)
                    """
                    log_prob = predictive_model.predict_log_proba(self.input_df.drop(self.dependent_var, axis=1))
                    n_records = len(log_prob)
                    X_beta = []
                    for i in range(n_records):
                        X_beta.append(log_prob[i][0]-log_prob[i][1])
                    self.SE = np.std(X_beta)
                else:
                    # print("Learning a linear regression model .. " )
                    predictive_model = LinearRegression()
                    predictive_model.fit(self.input_df.drop(self.dependent_var, axis=1),
                                         self.input_df[self.dependent_var])

                    # add for estimating standard error (SE)
                    predicted_y = predictive_model.predict(self.input_df.drop(self.dependent_var, axis=1))
                    self.SE = np.std(self.input_df[self.dependent_var] - predicted_y)
            else:
                """
                User specified the PM they want to use.
                """
                if self.model_type == "LinearRegression":
                    # print("Learning a linear regression model .. " )
                    predictive_model = LinearRegression()
                    predictive_model.fit(self.input_df.drop(self.dependent_var, axis=1), self.input_df[self.dependent_var])

                    # add for estimating standard error (SE)
                    predicted_y = predictive_model.predict(self.input_df.drop(self.dependent_var, axis=1))
                    self.SE = np.std(self.input_df[self.dependent_var] - predicted_y)

                if self.model_type == "LogisticRegression":
                    # print("Learning a logistic regression model .. " )
                    predictive_model = LogisticRegression(solver='lbfgs')
                    predictive_model.fit(self.input_df.drop(self.dependent_var, axis=1), self.input_df[self.dependent_var])

                    """
                    add for estimating standard error (SE)
                    """
                    log_prob = predictive_model.predict_log_proba(self.input_df.drop(self.dependent_var, axis=1))
                    n_records = len(log_prob)
                    X_beta = []
                    for i in range(n_records):
                        X_beta.append(log_prob[i][0] - log_prob[i][1])
                    self.SE = np.std(X_beta)

                if self.model_type == "MLPRegressor":
                    # print("Learning a Neural Network .. " )
                    predictive_model = MLPRegressor(
                        hidden_layer_sizes=self.hidden_layers)  ### TODO: how to link training and optimization!
                    predictive_model.fit(self.input_df.drop(self.dependent_var, axis=1),
                                         self.input_df[self.dependent_var])

                    """
                    add for estimating standard error (SE)
                    """
                    predicted_y = predictive_model.predict(self.input_df.drop(self.dependent_var, axis=1))
                    self.SE = np.std(self.input_df[self.dependent_var] - predicted_y)

            self.optimization_pm = predictive_model

    def set_breakpoints(self, number_of_breakpoints):
        """
        set the number of breakpoints.
        """
        if isinstance(number_of_breakpoints, numbers.Number):
            self.n_breakpoints = number_of_breakpoints
        else:
            print("The number of breakpoints should be an integer.")
            sys.exit(1)
    
    def get_breakpoints(self):
        return self.n_breakpoints

    def set_pm_type(self, pm_name):
        if isinstance(pm_name, str):
            if pm_name not in {"LinearRegression", "LogisticRegression", "MLPRegressor"}:
                print("Predictive models must be one of : 'LinearRegression', 'LogisticRegression', or 'MLPRegressor'.")
                sys.exit(1)
            self.model_type = pm_name

        else:
            print("pm_name should be a string.")
            sys.exit(1)

    def get_pm_type(self):
        return self.model_type

    def update_nn_parameters(self):
        """
        If hidden_layers is changed, we need to update the rest.
        :return: no return.

        It's recommended to run update_nn_parameters() before training NN.
        When optimize, retrieve information from the trained model to make sure the trained model (structure) is used in the optimization.
        """
        self.n_hidden_layers = len(self.hidden_layers)
        self.n_layers = self.n_hidden_layers + 2
        self.layers_sizes = [self.n_inputs] + self.hidden_layers + [self.n_outputs]
        self.offset = [0]
        for i in range(len(self.layers_sizes) - 1):
            self.offset += [self.offset[i] + self.layers_sizes[i]]

        self.n_nodes = self.n_inputs + 1
        for i in self.hidden_layers:
            self.n_nodes += i

        self.nodes_locations = []
        for layer in range(self.n_layers):
            for iter in range(self.layers_sizes[layer]):
                self.nodes_locations.append(layer)

        # print("n_hidden_layers : ", self.n_hidden_layers)
        # print("n_layers : ", self.n_layers)
        # print("layers_sizes : ", self.layers_sizes)
        # print("offset : ", self.offset)

    def set_hidden_layers(self, new_hidden_layers):
        if isinstance(new_hidden_layers, list):
            self.hidden_layers = new_hidden_layers
            self.update_nn_parameters()
        else:
            print("hidden_layers must be a list.")
            sys.exit(1)

    def get_hidden_layers(self):
        return self.hidden_layers

    def __init__(self, parent_dimodel, input_df=None, dependent_var=None, pretrained_model=None, feature_names=None):
        """
        input_df is a dataframe that includes both features and dependent_var;
        dependent_var is the name of the column in input_df;
        """
        # print("Creating an optimization predictive model ... ")
        self.SE = -1.0  # for generating prediction intervals
        self.n_breakpoints = 20  # for logistic regression models

        """
        Initialize for NN, assign them value later.
        """
        self.hidden_layers = []
        self.n_inputs = 0
        self.n_outputs = 1  ## TODO: for now, assume single output for each PM.

        """
        calculated
        """
        self.n_hidden_layers = len(self.hidden_layers)
        self.n_layers = 0
        self.layers_sizes = []
        self.offset = [0]
        self.n_nodes = 0
        self.nodes_locations = []

        if pretrained_model is None:
            if (input_df is None) or (dependent_var is None) or (feature_names is not None):
                print("Need to specify data frame and dependent variable if no pretrained model is specified ... ")
                sys.exit(1)

            self.JModel = parent_dimodel
            parent_dimodel.optimization_pms.append(self)
            self.optimization_pm = None  ## This is updated in train_opt_pm.
            self.input_df = input_df
            self.dependent_var = dependent_var
            self.feature_names = input_df.drop(dependent_var, axis=1).columns
            self.model_type = None

            """
            The following are for neural networks
            The following three are determined by user or the data.
            """
            self.hidden_layers = [3]
            self.n_inputs = input_df.shape[1] - 1
            self.n_outputs = 1  ## TODO: for now, assume single output for each PM.

            """
            calculated
            """
            self.n_hidden_layers = len(self.hidden_layers)
            self.n_layers = self.n_hidden_layers + 2
            self.layers_sizes = [self.n_inputs] + self.hidden_layers + [self.n_outputs]
            self.offset = [0]
            for i in range(len(self.layers_sizes) - 1):
                self.offset += [self.offset[i] + self.layers_sizes[i]]

            self.n_nodes = self.n_inputs + 1
            for i in self.hidden_layers:
                self.n_nodes += i

            self.nodes_locations = []
            for layer in range(self.n_layers):
                for iter in range(self.layers_sizes[layer]):
                    self.nodes_locations.append(layer)
        else:
            if (input_df is not None) or (dependent_var is not None) or (feature_names is None):
                ## TODO: the following later.
                """
                Teng on Sep 12, 2019: [Implement later maybe]
                    Users can specify both pretrained_model and input_df, so that they could have a prediction interval of their objective value.
                """
                print("Do not supply input_df or dependent_var if pretrained model is specified ... ")
                sys.exit(1)

            self.JModel = parent_dimodel
            parent_dimodel.optimization_pms.append(self)
            self.optimization_pm = pretrained_model
            self.input_df = None
            self.dependent_var = None
            self.feature_names = feature_names
            self.model_type = type(pretrained_model).__name__

            if isinstance(pretrained_model, MLPRegressor):
                self.hidden_layers = pretrained_model.hidden_layer_sizes
                self.n_inputs = len(pretrained_model.coefs_[0])
                self.n_outputs = pretrained_model.n_outputs_
                self.update_nn_parameters()
                # print("hidden_layers : ", self.hidden_layers)
                # print("n_inputs : ", self.n_inputs)
                # print("n_outputs : ", self.n_outputs)


class ExpressionTerm:

    def __init__(self, input_regular_var, input_value):
        self.regular_var = input_regular_var
        self.value = input_value

    def __str__(self):
        return "Variable is " + self.regular_var.name + " and value is " + str(self.value)


class Expression:

    def add_term(self, input_regular_var, input_value):
        if not isinstance(input_value, numbers.Number):
            print("Setting a non-numeric value for a term ... ")
            sys.exit(1)
        if not isinstance(input_regular_var, RegularVariable):
            print("Setting a non-regular variable in a term ... ")
            sys.exit(1)
        self.expression_terms.append(ExpressionTerm(input_regular_var, input_value))

    def __init__(self):
        # print("Declared an expression ... " )
        self.expression_terms = list()


class Constraint:

    def __init__(self, con_expr, sense, rhs):
        self.con_expr = con_expr
        self.sense = sense
        self.rhs = rhs


class RegularVariable:

    def getVariableDetails(self):
        return {"var_name": self.name,
                # "domain": self.domain,
                "obj_coeff": self.objective_coefficient,
                "value_in_sol": self.value_in_sol}

    def setDiscreteDomain(self, new_domain):
        if not isinstance(new_domain, list):
            print("Setting domain where the dimension argument is not a list ... ")
            sys.exit(1)
        if len(new_domain) < 1:
            print("Setting a domain with dimension less than 1 ... ")
            sys.exit(1)
        for i in range(len(new_domain)):
            if not isinstance(new_domain[i], numbers.Number):
                print("Setting a domain element that is not a number ... " )
                sys.exit(1)
        self.discrete_domain = np.sort(np.array(new_domain))
        self.upper_bound = max(np.array(new_domain))
        self.lower_bound = min(np.array(new_domain))
        self.variable_type = "discrete"

    def setContinuousDomain(self, lower_bound=None, upper_bound=None):
        """
        Teng on Sep 12, 2019: don't know what to do yet.
        :param new_domain:
        :return:
        """

        if lower_bound is not None:
            if not isinstance(lower_bound, numbers.Number):
                print("lower_bound must be a number.")
        if upper_bound is not None:
            if not isinstance(upper_bound, numbers.Number):
                print("upper_bound must be a number.")

        self.continuous_domain = [lower_bound, upper_bound]
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.variable_type = "continuous"

    def setObjectiveCoefficient(self, new_coeff):
        if not isinstance(new_coeff, numbers.Number):
            print("Setting a non-numeric objective coefficient ... ")
            sys.exit(1)
        self.objective_coefficient = new_coeff

#    def # printVariableDetails(self):
#        # print("variable name: " , self.name)
#        # print("variable domain: ", self.domain)
#        # print("objective coefficient: ", self.objective_coefficient)

    def __init__(self, variable_set_name, indices, parent_dimodel):
        # print("Declared a variable ... " )
        self.name = variable_set_name + "["
        for i in range(len(indices)):
            if i == len(indices) - 1:
                self.name = self.name + str(indices[i]) + "]"
            else:
                self.name = self.name + str(indices[i]) + ","
        self.parent_dimodel = parent_dimodel
        self.discrete_domain = [JANOS.MIN_DOUBLE_VAL, JANOS.MAX_DOUBLE_VAL]
        self.continuous_domain = [JANOS.MIN_DOUBLE_VAL, JANOS.MAX_DOUBLE_VAL]
        self.objective_coefficient = 0.0
        self.value_in_sol = 0
        self.upper_bound = JANOS.MAX_DOUBLE_VAL
        self.lower_bound = JANOS.MIN_DOUBLE_VAL
        self.variable_type = "continuous"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (self.name) == (other.name)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


class PredictedVariable:

    def getVariableDetails(self):
        """
        Teng on Sep 13, 2019: not in the manual yet. Later...
        :return:
        """
        return({"var_name": self.name,
                "predictive_model": self.opm,
                "obj_coeff": self.objective_coefficient,
                "value_in_sol": self.value_in_sol,
                "mapping_of_columns": self.mapping_of_columns,
                "lower_bound": self.lower_bound,
                "upper_bound": self.upper_bound,
                "penalty": self.penalty})

    def setPM(self, opm, variable_mapping):
        # print(self.parentDImodel)
        if not isinstance(variable_mapping, dict):
            print("Not a dictionary in the definition of the variable ... ")
            sys.exit(1)
#        if not all( x in self.parentDImodel__regularVariablesLong or isinstance(numbers.Number) for x in list(variable_mapping.values()) ):
#            # print("Not all values in dictionary are regular variables or constants... " )
#            sys.exit(1)
        # print("\n")
        # print("TO DO: Ensure input to setPM is an optimization predictive model and the second argument is a dictionary containing only regular variables and constants ... " )
        # print("\n")
        self.opm = opm
        self.variable_mapping = variable_mapping

    def __init__(self, parentDImodel, variable_set_name, indices):
        # print("Declared a variable ... " )
        self.name = variable_set_name + "["
        for i in range(len(indices)):
            if i == len(indices) - 1:
                self.name = self.name + str(indices[i]) + "]"
            else:
                self.name = self.name + str(indices[i]) + ","
        self.parentDImodel = parentDImodel

        self.opm = None
        self.variable_mapping = None
        self.objective_coefficient = 0.0
        self.values_in_sol = 0
        self.lower_bound = JANOS.MIN_DOUBLE_VAL
        self.upper_bound = JANOS.MAX_DOUBLE_VAL
        self.penalty = 1

    def setPenalty(self, new_val):
        if not isinstance(new_val, numbers.Number):
            print("Setting a non-numeric penalty ... ")
            sys.exit(1)
        if new_val < (-1)*JANOS.EPSILON:
            print("Setting negative penalty which is not allowed ... ")
            sys.exit(1)
        self.penalty = new_val

    def setLowerBound(self, new_val):
        if not isinstance(new_val, numbers.Number):
            print("Setting a non-numeric bound ... ")
            sys.exit(1)
        if new_val > self.upper_bound:
            print("Setting a lower bound which is higher than the current upper bound ... ")
            sys.exit(1)
        self.lower_bound = new_val

    def setUpperBound(self, new_val):
        if not isinstance(new_val, numbers.Number):
            print("Setting a non-numeric bound ... ")
            sys.exit(1)
        if new_val < self.lower_bound:
            print("Setting a upper bound which is lower than the current lower bound ... ")
            sys.exit(1)
        self.upper_bound = new_val

    def setObjectiveCoefficient(self, new_coeff):
        if not isinstance(new_coeff, numbers.Number):
            print("Setting a non-numeric objective coefficient ... ")
            sys.exit(1)
        self.objective_coefficient = new_coeff

