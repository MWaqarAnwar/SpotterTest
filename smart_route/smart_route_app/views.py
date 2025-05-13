from django.shortcuts import render
from rest_framework.views import APIView
import requests, os, json
from requests.structures import CaseInsensitiveDict
from .serializers import SmartRouteSerializer
from rest_framework.response import Response
from .utils import SmartRouteUtils
from dotenv import load_dotenv

load_dotenv()

class FetchSmartRouteAPIView(APIView):
    def post(self, request):
        serializer = SmartRouteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        x1 = serializer.validated_data['x1']
        y1 = serializer.validated_data['y1']
        x2 = serializer.validated_data['x2']
        y2 = serializer.validated_data['y2']
        fuel_prices_csv = serializer.validated_data['fuel_prices_csv']

        fuel_prices_df = SmartRouteUtils.load_csv_data(fuel_prices_csv)
        addresses_list = SmartRouteUtils.convert_df_to_list_of_full_addresses(fuel_prices_df)

        geoapify_api_key = os.getenv('GEOAPIFY_API_KEY')

        headers_geocode = CaseInsensitiveDict()
        headers_geocode["Accept"] = "application/json"

        url_geocode = f"https://api.geoapify.com/v1/batch/geocode/search?apiKey={geoapify_api_key}"
        print(addresses_list)
        geocode_response = requests.post(url_geocode, headers=headers_geocode, json=addresses_list[:1000])
        print("geocode_response=======", geocode_response.json())
        #url = f"https://api.geoapify.com/v1/routing?waypoints=50.96209827745463%2C4.414458883409225%7C50.429137079078345%2C5.00088081232559&mode=drive&apiKey={geoapify_api_key}"
        url_routing = f"https://api.geoapify.com/v1/routing?waypoints={x1}%2C{y1}%7C{x2}%2C{y2}&mode=drive&apiKey={geoapify_api_key}"
        
        headers_routing = CaseInsensitiveDict()
        headers_routing["Accept"] = "application/json"

        resp = requests.get(url_routing, headers=headers_routing)
        json_response = resp.json()
        try:
           route = json_response['features'][0]['geometry']
        except:
            return Response({"Error":"Error getting route coordinates"}, status=400)
        
        # static_map_url = f"https://maps.geoapify.com/v1/staticmap?geometry={route}"
        static_map_url = f"https://maps.geoapify.com/v1/staticmap?apiKey={geoapify_api_key}"

        static_map_response = requests.post(static_map_url, headers=headers_routing, json={"width": 600, "height": 400,"geometries":json_response['features'][0]['geometry']['coordinates']})
        return Response(static_map_response, status=200)