
import requests
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alpha_vantage.throttling import AuthAnonMinThrottle


@throttle_classes([AuthAnonMinThrottle])
class AlphaVantageViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path="get-stock")
    def get_stock(self, request):
        try:
            data = []
            symbol = request.query_params.get('symbol', None)
            response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey=X86NOH6II01P7R24')
            time_series_dict = response.json()["Time Series (Daily)"]
            variation = self._get_variation(time_series_dict)
            data.append(variation)

            for date, values in time_series_dict.items():
                data.append({
                    date: {
                        "open": values["1. open"],
                        "higher": values["2. high"],
                        "lower": values["3. low"],
                    }
                })
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def _get_variation(self, time_series: dict) -> dict:
        time_series_keys = list(time_series.keys())
        if len(time_series_keys) <= 1:
            return {"variation": None}
        new_value = float(time_series[time_series_keys[0]]['4. close'])
        old_value = float(time_series[time_series_keys[1]]['4. close'])
        return {"variation": f"{(new_value - old_value) / old_value * 100} %"}

