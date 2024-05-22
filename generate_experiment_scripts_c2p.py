from generate_experiment_scripts import * 

if __name__ == "__main__":
    from config_c2p import translators, tests

    generate_scripts(translators, tests, "./experiments_c2p")
