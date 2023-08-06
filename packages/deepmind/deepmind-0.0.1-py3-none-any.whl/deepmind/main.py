import machine_learning
import parameters as p
import preprocessing
import pandas as pd
import os
import platypus
import numpy as np
from matplotlib import pyplot as plt


def ga_objective_func(params):


    number_of_classes, svm_gamma, svm_c = params


    def train_autoencoder(fusion):

        def autoencoder(name, file_address, fusion):
            d = preprocessing.Data()
            d.address = file_address
            d.fusion = fusion
            fusion_data = d.import_fluent_fusion()
            ae = machine_learning.Autoencoder()
            ae.data = fusion_data
            ae.name = name
            ae.train()
            reconstructed, latent = ae.predict()
            error = ae.error()
            return reconstructed, latent, error

        cfd_files = os.listdir(p.cfd_content)

        counter = 0
        for f in cfd_files:
            if 'contents' in f:
                print('{} % completed'.format(round((counter/len(cfd_files)) * 100, 2)))
                name = f.split('/')[-1]
                if ('weight_' + name) not in os.listdir(p.output_dir + 'training_weights/'):
                    file_address = p.cfd_content + name
                    autoencoder(name, file_address, fusion)
                    counter += 1


    def exp_classification(number_of_classes):
        exp = pd.read_csv(p.files_dir + 'experiment_info.csv')
        measured_classes = preprocessing.classification()
        measured_classes.data = exp
        measured_classes.num_of_classes = number_of_classes
        exp_classified = measured_classes.assign_classes()
        return exp_classified

    def predict(name, file_address, element):
        d = preprocessing.Data()
        d.address = file_address
        d.fusion = fusion
        fusion_data = d.import_fluent_fusion()
        ae = machine_learning.Autoencoder()
        ae.data = fusion_data
        ae.name = name
        ae.element = element
        reconstructed, latent = ae.predict()
        error = ae.error()
        return reconstructed, latent, error


    def generate_svm_data(number_of_classes):
        exp_classified = exp_classification(number_of_classes)
        dp_list = exp_classified['dp'].values
        dp_list = np.unique(dp_list)
        reconstructed_list, latent_list, error_list = [], [], []
        counter = 0
        for dp in dp_list:
            elements = list(exp_classified[exp_classified['dp'] == int(dp)]['element'].values)
            tot = len(dp_list) * len(elements)
            for element in elements:
                print('{} % completed'.format(round((counter / tot) * 100, 2)))
                name = 'contents_{}_freezing.pkl'.format(int(dp))
                weight_file_address = p.output_dir + 'training_weights/weight_' + name
                cfd_file_address = p.cfd_content + name
                reconstructed, latent, error = predict(name, cfd_file_address, element)
                reconstructed_list.append(reconstructed)
                latent_list.append(latent)
                error_list.append(error)
                counter += 1
        np.save('latent_list.np', np.array(latent_list))
        np.save('autoencoder_error.np', np.array(error_list))


    def load_exp_data():
        exp_classified = exp_classification(number_of_classes)
        latent_list = np.load('latent_list.np.npy')
        autoencoder_error = np.load('autoencoder_error.np.npy')
        latent_np = np.array(latent_list)
        input_data = latent_np.reshape((80, 22))
        exp_data = input_data
        exp_labels = exp_classified['size classes'].values
        return exp_data, exp_labels, autoencoder_error

    def classification():
        exp_data, exp_labels, autoencoder_error = load_exp_data()

        def predict_labels(i):
            svm = machine_learning.Svm(gamma=svm_gamma, c=svm_c, data=exp_data[10:70], labels=exp_labels[10:70], new_inputs=[exp_data[i, :]])
            predicted_labels = svm.classify()

            return predicted_labels[0]

        predicted_labels = []
        for i in range(80):
            predicted_labels.append(predict_labels(i)[0])



        def mse(a, b):
            return (np.square(a - b)).mean(axis=0)

        svm_error = mse(np.array(exp_labels[:10]), np.array(predicted_labels[:10]))


        return predicted_labels, svm_error


    exp_labels = exp_classification(number_of_classes)
    predicted_labels, svm_error = classification()


    if (svm_error < p.acceptable_error):
        with open(p.output_dir + 'ga_params.txt', 'a+') as f:
            f.writelines('{}\t{}\n'.format(params, svm_error))


    # train_autoencoder(fusion)
    # generate_svm_data(number_of_classes)


    x = range(len(predicted_labels))

    exp_labels = exp_labels['size classes'].values


    plt.plot(x, exp_labels, label='Experiment')
    plt.plot(x, predicted_labels, '--', label='Predicted')
    plt.legend()
    # plt.show()


    print(svm_error)
    return [svm_error]


def run_ga(cpu_number):
    #   remove old log file
    if os.path.isfile(p.output_dir + 'ga_params.txt'):
        os.remove(p.output_dir + 'ga_params.txt')

    problem = platypus.Problem(3, 1, 0)  # where Problem(variables, objective_funcs, constraints)

    problem.types[:] = [platypus.Integer(5, 5000), platypus.Real(0.0001, 10), platypus.Real(0.0001, 10)]

    # problem.constraints[0] = ">0"
    problem.function =  ga_objective_func
    if __name__ == "__main__":
        algorithms = [platypus.NSGAII]
        problems = [problem]
        with platypus.ProcessPoolEvaluator(cpu_number) as evaluator:
            results = platypus.experiment(algorithms, problems, nfe=900000, evaluator=evaluator)



# run_ga(1)


params = [8, 2.9039858639398903, 7.680102206149233]
ga_objective_func(params)