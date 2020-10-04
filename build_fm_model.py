from grave import FactorizationMachine


if __name__ == '__main__':

    name = "all_stable_bandgap_dim20.fm.ctx10_or_1"
    dim = 20
    context_window_size = 10

    X, Y, dictionary = FactorizationMachine.load_training_data("%s.training.data" % name, sparse=True)

    fm = FactorizationMachine(dim=dim, y_max=100, alpha=0.75, context_window_size=context_window_size, dictionary=dictionary)

    fm.fit(X, Y, batch_size=1, num_epochs=50, learning_rate=0.002, use_autograd=False)

    fm.save("%s.model" % name)