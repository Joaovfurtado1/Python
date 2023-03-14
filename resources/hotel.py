from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
        {
            'hotel_id': 'alpha',
            'nome' : 'Alpha Hotel',
            'estrelas': 4.3,
            'diaria' : 420.60,
            'cidade': 'São Paulo'
        },
        {
            'hotel_id': 'beta',
            'nome' : 'Beta Hotel',
            'estrelas': 3.0,
            'diaria' : 300.00,
            'cidade': 'São Paulo'
        },
        {
            'hotel_id': 'delta',
            'nome' : 'Delta Hotel',
            'estrelas': 5.0,
            'diaria' : 750.99,
            'cidade': 'Rio de Janeiro'
        }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id): # metodo usado para encontrar o ID de hotel igual ao informado no parametro e retorna esse hotel caso o mesmo seja encontrado na lista de hoteis
        for hotel in hoteis: 
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None


    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404 #notfound}

    def post(self, hotel_id):
        

        dados = Hotel.argumentos.parse_args() # input dos novos dados informados usando o argumento da classe Hotel
        hotel_objeto = HotelModel(hotel_id, **dados)
        #novo_hotel = { 'hotel_id': hotel_id, **dados } # usa a kward para desempacotar os dados para o Json
        novo_hotel= hotel_objeto.json()
        hoteis.append(novo_hotel) # adiciona o novo hotel na lista de hoteis
        return novo_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        #novo_hotel = { 'hotel_id': hotel_id, **dados }
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel= hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id] # passa por todos os hoteis da lista e os salva na variavel hotel que posteriormente será passada para a lista raiz hoteis
        return {'message' : 'Hotel deleted'}
