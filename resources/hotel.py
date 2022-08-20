from flask_restful import Resource, reqparse
from model.hotel import HotelModel

hoteis = [
    {
        'hotel_id' : 'alpha',
        'nome' : 'Alpha Hotel',
        'estrelas' : 4.3,
        'diaria': 420.50,
        'cidade': 'Rio'
    },
    {
        'hotel_id' : 'bravo',
        'nome' : 'Bravo Hotel',
        'estrelas' : 4.5,
        'diaria': 460.90,
        'cidade': 'Santa'
    },
    {
        'hotel_id' : 'charlie',
        'nome' : 'Charlie Hotel',
        'estrelas' : 3.8,
        'diaria': 340.0,
        'cidade': 'Santa'
    }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}



class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return{'message': 'Hotel not found.'}, 404


    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id \'{}\' already exists.'.format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'},500 #Erro de servidor
        return hotel.json()


    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'},500 #Erro de servidor
        return hotel.json(), 201


    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'},500 #Erro de servidor
            return {'message':' Hotel deleted.'}
        return {'message': 'Hotel not found.'}