import pandas as pd
import metrics

from .strategies import BaseStrategy, GreedyStrategy
from .entities import Payment, Provider

from tqdm import tqdm
from typing import List


class Simulator:

    def __init__(self, payments: pd.DataFrame, providers: pd.DataFrame, strategy: BaseStrategy = GreedyStrategy()):
        self.payments = payments
        self.providers = providers

        self.strategy = strategy

    def simulate(self, verbose: bool = True):        
        history = []

        for _, payment in tqdm(self.payments.iterrows(), total=len(self.payments), disable=not verbose):
            payment = Payment(*payment)

            available_providers = self._get_available_providers(payment)
            
            if len(available_providers) > 0:
                optimized_providers = self.strategy.optimize(available_providers)

                expected_commission = metrics.compute_expected_commission(optimized_providers)
                expected_conversion = metrics.compute_expected_conversion(optimized_providers)

                expected_processing_time = metrics.compute_expected_processing_time(optimized_providers)

            else:
                optimized_providers = []
                
                expected_commission = 0
                expected_conversion = 0
                expected_processing_time = 0
            
            history.append({
                "payment": payment,
                "providers": optimized_providers,
                "metrics": {
                    "expected_commission": expected_commission,
                    "expected_conversion": expected_conversion,
                    "expected_processing_time": expected_processing_time
                }
            })

        return history

    def _get_available_providers(self, payment: Payment) -> List[Provider]:
        available_providers = self.providers[
            (payment.time >= self.providers.TIME) &
            (payment.time <= (self.providers.TIME + timedelta(hours=1))) &
            (payment.amount >= self.providers.MIN_SUM) &
            (payment.currency == self.providers.CURRENCY) &
            (payment.amount <= self.providers.MAX_SUM)
        ].drop_duplicates("ID")

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