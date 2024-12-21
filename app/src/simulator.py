import pandas as pd

from .strategies import BaseStrategy, GreedyStrategy
from .entities import Payment, Provider

from .metrics import *

from dataclasses import dataclass
from tqdm import tqdm
from typing import List


@dataclass
class Log:
    payment: Payment
    solution: List[Provider]

class Simulator:

    def __init__(self, payments: pd.DataFrame, providers: pd.DataFrame, currencies: pd.DataFrame, strategy: BaseStrategy = GreedyStrategy()):
        self.payments = payments
        self.providers = providers
        self.currencies = currencies
        self.strategy = strategy

        self._payments_for_output = self.payments.copy()

        self._initialize_dataframes()

        self.providers_constants = {
            row["ID"]: {
                "limit_min": row["LIMIT_MIN"],
                "limit_max": row["LIMIT_MAX"],
                "currency": row["CURRENCY"],
            }

            for _, row in providers[providers["TIME"] == providers.iloc[0]["TIME"]].iterrows()
        }

    def simulate(self, verbose: bool = True):        
        history = []

        for _, payment in tqdm(self.payments.iterrows(), total=len(self.payments), disable=not verbose):
            payment = Payment(
                time=payment["eventTimeRes"],
                amount=payment["amount"],
                currency=payment["cur"],
                payment=payment["payment"],
                token=payment["cardToken"]
            )

            available_providers = self._get_available_providers(payment)
            
            if len(available_providers) > 0:
                optimized_providers = self.strategy.optimize(available_providers)

                history.append({
                    "payment": payment,
                    "solution": optimized_providers
                })

            else:
                history.append({
                    "payment": payment,
                    "solution": []
                })

        return history
    
    def _get_output_dataframe(self, history) -> pd.DataFrame:
        flows: List[str] = []

        for log in history:
            flow = ""

            for k, provider in enumerate(log["solution"]):
                if k != len(log["solution"]) - 1:
                    flow += f"{provider.id}-"
                else:
                    flow += f"{provider.id}"

            flows.append(flow)

        self._payments_for_output["flow"] = flows

        return self._payments_for_output
    
    def _compute_metrics(self, history):
        penalty = 0
        processing_times = []
        
        for log in history:
            if len(log["solution"]) > 0:
                payment = log["payment"]

                expected_commision = compute_expected_commission(log["solution"])
                expected_processing_time = compute_expected_processing_time(log["solution"])

                processing_times.append(expected_processing_time)

                penalty += (expected_commision / 100) * self.currencies[payment.currency] * payment.amount

        return {
            "penalty": penalty.item(),
            "processing_time": {
                "mean": np.mean(processing_times).item(),
                "median": np.median(processing_times).item(),
                "first_quantile": np.quantile(processing_times, q=0.25).item(),
                "third_quantile": np.quantile(processing_times, q=0.75).item(),
            }
        }
            

    def _get_available_providers(self, payment: Payment) -> List[Provider]:
        available_providers = self.providers[
            (payment.time <= self.providers.TIME) &
            (payment.amount >= self.providers.MIN_SUM) &
            (payment.currency == self.providers.CURRENCY) &
            (payment.amount <= self.providers.MAX_SUM)].drop_duplicates(subset=["ID"], keep="last")

        if len(available_providers) > 0:
            assert len(available_providers) == available_providers.ID.nunique()

        available_providers = [Provider(id=provider.ID, 
                                        commission=provider.COMMISSION, 
                                        conversion=provider.CONVERSION, 
                                        processing_time=provider.AVG_TIME,
                                        limit_min=provider.LIMIT_MIN,
                                        min_sum=provider.MIN_SUM,
                                        max_sum=provider.MAX_SUM,
                                        limit_max=provider.LIMIT_MAX,
                                        currency=provider.CURRENCY)
                                         
                               for _, provider in available_providers.iterrows()]

        return available_providers
    
    def _initialize_dataframes(self):
        self.payments.eventTimeRes = pd.to_datetime(self.payments.eventTimeRes)
        self.payments = self.payments.sort_values(by="eventTimeRes")

        self.providers.TIME = pd.to_datetime(self.providers.TIME)

        self.providers = self.providers.sort_values(by="TIME")
        self.providers = self.providers.drop_duplicates(subset=["TIME", "ID"], keep="last")

        self.providers.index = range(len(self.providers))

        self.currencies = {row["destination"]: row["rate"] for _, row in self.currencies.iterrows()}