import pandas as pd


from src.simulator import Simulator


providers = pd.read_csv("dev/data/providers_1.csv")
payments = pd.read_csv("dev/data/payments_1.csv")
currencies = pd.read_csv("dev/data/ex_rates.csv")


simulator = Simulator(payments=payments, providers=providers, currencies=currencies)


history = simulator.simulate()

outputs = simulator._get_output_dataframe(history)

metrics = simulator._compute_metrics(history)


print(metrics)