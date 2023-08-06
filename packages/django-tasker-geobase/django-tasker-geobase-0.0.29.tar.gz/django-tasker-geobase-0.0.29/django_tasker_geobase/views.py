import json
import os

import requests
from django.conf import settings

from rest_framework import response, request, status, views
from . import serializer, models, geocoder


class GeoObject(views.APIView):
    serializer_class = serializer.GeoBase

    def get(self, request: request.Request, geobase: models.Geobase):
        serializer_obj = self.serializer_class(data=geobase.dict())
        if not serializer_obj.is_valid():
            return response.Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(serializer_obj.validated_data)


class Search(views.APIView):
    serializer_class = serializer.Search

    def get(self, request: request.Request):
        serializer_obj = self.serializer_class(data=request.GET)
        if not serializer_obj.is_valid():
            return response.Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

        result = geocoder.geo(query=serializer_obj.validated_data.get('query'))
        if result:
            return response.Response(result.dict())
        else:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)


class Suggestion(views.APIView):
    serializer_class = serializer.Search

    def get(self, request: request.Request):
        serializer_obj = self.serializer_class(data=request.GET)
        if not serializer_obj.is_valid():
            return response.Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

        data_key = getattr(settings, 'GEOBASE_DADATA', os.environ.get('GEOBASE_DADATA'))
        if not data_key:
            raise Exception("not found key GEOBASE_DADATA")

        data = {"query": serializer_obj.validated_data.get('query'), "count": 10, "restrict_value": True}

        locations = []
        if serializer_obj.validated_data.get('locality') and serializer_obj.validated_data.get('street'):
            street = serializer_obj.validated_data.get('street')
            street = street.replace("проспект", "")

            locations.append({
                "city": serializer_obj.validated_data.get('locality'),
                "street": street,
            })
        elif serializer_obj.validated_data.get('locality'):
            locations.append({"city": serializer_obj.validated_data.get('locality')})

        if locations:
            data.update({"locations": locations})

        res = requests.post(
            url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
            data=json.dumps(data),
            headers={
                'Authorization': "Token {token}".format(token=data_key),
                'Content-Type': "application/json",
                'Accept': "application/json",
            }
        )

        dadata = []
        if 'suggestions' in res.json():
            for item in res.json().get('suggestions'):

                # geo_res = []
                # if item.get('data').get('country'):
                #     geo_res.append("{country}".format(country=item.get('data').get('country')))
                #
                # if item.get('data').get('region'):
                #     geo_res.append("{region}".format(region=item.get('data').get('region')))
                #
                # if item.get('data').get('city'):
                #     geo_res.append("{city}".format(city=item.get('data').get('city')))
                #
                # if item.get('data').get('street'):
                #     geo_res.append("{street}".format(street=item.get('data').get('street')))
                #
                # if item.get('data').get('house'):
                #     geo_res.append("{house}".format(house=item.get('data').get('house')))
                #
                # if item.get('data').get('block_type_full'):
                #     geo_res.append("{block_type_full}".format(block_type_full=item.get('data').get('block_type_full')))
                #
                # if item.get('data').get('block'):
                #     geo_res.append("{block}".format(block=item.get('data').get('block')))
                # ", ".join(geo_res)

                res = geocoder.geo(query=item.get('unrestricted_value'))
                if res:
                    dadata.append(res.dict())

                #print(res.dict())
                # dadata.append({
                #     'value': item.get('value'),
                #     'unrestricted_value': item.get('unrestricted_value'),
                #     'country': item.get('data').get('country'),
                #     'province': item.get('data').get('region'),
                #     'locality': item.get('data').get('city'),
                #     'street': item.get('data').get('street'),
                #     'house': item.get('data').get('house'),
                # })

        return response.Response({'result': dadata})
