from flask import Flask, Blueprint, render_template, request, jsonify
import random

api = Blueprint('api', __name__, template_folder='templates', )

charades = [
    {'id': 1, 'charade': 'O que é, o que é: quanto mais se tira, maior fica?', 'responses': [
        {'response': 'Buraco', 'correct': 'true'},
        {'response': 'Dinheiro', 'correct': 'false'},
        {'response': 'Roupa', 'correct': 'false'},
        {'response': 'Comida', 'correct': 'false'},
        {'response': 'Tempo', 'correct': 'false'}]},
    {'id': 2, 'charade': 'O que é, o que é: tem boca, mas não fala, tem asas, mas não voa?', 'responses': [
        {'response': 'Xícara', 'correct': 'true'},
        {'response': 'Livro', 'correct': 'false'},
        {'response': 'Árvore', 'correct': 'false'},
        {'response': 'Carro', 'correct': 'false'},
        {'response': 'Casa', 'correct': 'false'}]},
    {'id': 3, 'charade': 'O que é, o que é: anda com os pés na cabeça?', 'responses': [
        {'response': 'Piolho', 'correct': 'true'},
        {'response': 'Chapéu', 'correct': 'false'},
        {'response': 'Cabelo', 'correct': 'false'},
        {'response': 'Óculos', 'correct': 'false'},
        {'response': 'Brinco', 'correct': 'false'}]},
    {'id': 4, 'charade': 'O que é, o que é: quanto mais se perde, mais se tem?', 'responses': [
        {'response': 'Sono', 'correct': 'true'},
        {'response': 'Dinheiro', 'correct': 'false'},
        {'response': 'Roupa', 'correct': 'false'},
        {'response': 'Comida', 'correct': 'false'},
        {'response': 'Tempo', 'correct': 'false'}]},
    {'id': 5, 'charade': 'O que é, o que é: tem dentes, mas não morde?', 'responses': [
        {'response': 'Alho', 'correct': 'true'},
        {'response': 'Serra', 'correct': 'false'},
        {'response': 'Garfo', 'correct': 'false'},
        {'response': 'Tesoura', 'correct': 'false'},
        {'response': 'Pente', 'correct': 'false'}]},
    {'id': 6, 'charade': 'O que é, o que é: tem rio, mas não tem água, tem cidade, mas não tem prédio, e tem floresta, mas não tem árvore?', 'responses': [
        {'response': 'Mapa', 'correct': 'true'},
        {'response': 'Livro', 'correct': 'false'},
        {'response': 'Globo', 'correct': 'false'},
        {'response': 'Quadro', 'correct': 'false'},
        {'response': 'Bola', 'correct': 'false'}]},
    {'id': 7, 'charade': 'O que é, o que é: quanto mais se lava, mais sujo fica?', 'responses': [
        {'response': 'Água', 'correct': 'true'},
        {'response': 'Roupa', 'correct': 'false'},
        {'response': 'Carro', 'correct': 'false'},
        {'response': 'Chão', 'correct': 'false'},
        {'response': 'Corpo', 'correct': 'false'}]},
    {'id': 8, 'charade': 'O que é, o que é: tem coroa, mas não é rei, tem espinho, mas não é peixe?', 'responses': [
        {'response': 'Abacaxi', 'correct': 'true'},
        {'response': 'Cacto', 'correct': 'false'},
        {'response': 'Rosa', 'correct': 'false'},
        {'response': 'Estrela do mar', 'correct': 'false'},
        {'response': 'Ouriço', 'correct': 'false'}]},
    {'id': 9, 'charade': 'O que é, o que é: tem pescoço, mas não tem cabeça, tem boca, mas não fala?', 'responses': [
        {'response': 'Garrafa', 'correct': 'true'},
        {'response': 'Vaso', 'correct': 'false'},
        {'response': 'Copo', 'correct': 'false'},
        {'response': 'Chaleira', 'correct': 'false'},
        {'response': 'Panela', 'correct': 'false'}]},
    {'id': 10, 'charade': 'O que é, o que é: quanto mais se enche, mais leve fica?', 'responses': [
        {'response': 'Balão', 'correct': 'true'},
        {'response': 'Saco', 'correct': 'false'},
        {'response': 'Mochila', 'correct': 'false'},
        {'response': 'Caixa', 'correct': 'false'},
        {'response': 'Bolsa', 'correct': 'false'}]},
    {'id': 11, 'charade': 'O que é, o que é: tem agulha, mas não costura, tem linha, mas não tricota?', 'responses': [
        {'response': 'Disco', 'correct': 'true'},
        {'response': 'Relógio', 'correct': 'false'},
        {'response': 'Calculadora', 'correct': 'false'},
        {'response': 'Termômetro', 'correct': 'false'},
        {'response': 'Bússola', 'correct': 'false'}]},
    {'id': 12, 'charade': 'O que é, o que é: tem casa, mas não tem porta, tem cama, mas não tem lençol?', 'responses': [
        {'response': 'Caracol', 'correct': 'true'},
        {'response': 'Tartaruga', 'correct': 'false'},
        {'response': 'Concha', 'correct': 'false'},
        {'response': 'Ostra', 'correct': 'false'},
        {'response': 'Lesma', 'correct': 'false'}]},
    {'id': 13, 'charade': 'O que é, o que é: tem asas, mas não voa, tem boca, mas não fala?', 'responses': [
        {'response': 'Bule', 'correct': 'true'},
        {'response': 'Chaleira', 'correct': 'false'},
        {'response': 'Xícara', 'correct': 'false'},
        {'response': 'Caneca', 'correct': 'false'},
        {'response': 'Garrafa', 'correct': 'false'}]},
    {'id': 14, 'charade': 'O que é, o que é: quanto mais se tira, maior fica o buraco?', 'responses': [
        {'response': 'Terra', 'correct': 'true'},
        {'response': 'Areia', 'correct': 'false'},
        {'response': 'Água', 'correct': 'false'},
        {'response': 'Grama', 'correct': 'false'},
        {'response': 'Pedra', 'correct': 'false'}]},
    {'id': 15, 'charade': 'O que é, o que é: tem chapéu, mas não tem cabeça, tem boca, mas não fala?', 'responses': [
        {'response': 'Cogumelo', 'correct': 'true'},
        {'response': 'Árvore', 'correct': 'false'},
        {'response': 'Flor', 'correct': 'false'},
        {'response': 'Abajur', 'correct': 'false'},
        {'response': 'Luminária', 'correct': 'false'}]},
    {'id': 16, 'charade': 'O que é, o que é: tem agulha, mas não costura, tem botão, mas não é roupa?', 'responses': [
        {'response': 'Calculadora', 'correct': 'true'},
        {'response': 'Máquina de costura', 'correct': 'false'},
        {'response': 'Computador', 'correct': 'false'},
        {'response': 'Celular', 'correct': 'false'},
        {'response': 'Tablet', 'correct': 'false'}]},
    {'id': 17, 'charade': 'O que é, o que é: tem cabeça, tem dente, tem barba, não é bicho nem é gente?', 'responses': [
        {'response': 'Alho', 'correct': 'true'},
        {'response': 'Cebola', 'correct': 'false'},
        {'response': 'Milho', 'correct': 'false'},
        {'response': 'Abacaxi', 'correct': 'false'},
        {'response': 'Coco', 'correct': 'false'}]},
    {'id': 18, 'charade': 'O que é, o que é: tem coroa, mas não é rei, tem escamas, mas não é peixe?', 'responses': [
        {'response': 'Abacaxi', 'correct': 'true'},
        {'response': 'Cacto', 'correct': 'false'},
        {'response': 'Melancia', 'correct': 'false'},
        {'response': 'Laranja', 'correct': 'false'},
        {'response': 'Morango', 'correct': 'false'}]},
    {'id': 19, 'charade': 'O que é, o que é: tem nariz, mas não espirra, tem boca, mas não mastiga?', 'responses': [
        {'response': 'Fogão', 'correct': 'true'},
        {'response': 'Chuveiro', 'correct': 'false'},
        {'response': 'Televisão', 'correct': 'false'},
        {'response': 'Rádio', 'correct': 'false'},
        {'response': 'Geladeira', 'correct': 'false'}]},
    {'id': 20, 'charade': 'O que é, o que é: quanto mais se perde, mais se tem?', 'responses': [
        {'response': 'Sono', 'correct': 'true'},
        {'response': 'Dinheiro', 'correct': 'false'},
        {'response': 'Roupa', 'correct': 'false'},
        {'response': 'Comida', 'correct': 'false'},
        {'response': 'Tempo', 'correct': 'false'}]},
    {'id': 21, 'charade': 'O que é, o que é: tem dentes, mas não morde?', 'responses': [
        {'response': 'Pente', 'correct': 'true'},
        {'response': 'Garfo', 'correct': 'false'},
        {'response': 'Serra', 'correct': 'false'},
        {'response': 'Tesoura', 'correct': 'false'},
        {'response': 'Alho', 'correct': 'false'}]},
    {'id': 22, 'charade': 'O que é, o que é: tem rio, mas não tem água, tem cidade, mas não tem prédio, e tem floresta, mas não tem árvore?', 'responses': [
        {'response': 'Mapa', 'correct': 'true'},
        {'response': 'Livro', 'correct': 'false'},
        {'response': 'Globo', 'correct': 'false'},
        {'response': 'Quadro', 'correct': 'false'},
        {'response': 'Bola', 'correct': 'false'}]},
    {'id': 23, 'charade': 'O que é, o que é: quanto mais se lava, mais sujo fica?', 'responses': [
        {'response': 'Água', 'correct': 'true'},
        {'response': 'Roupa', 'correct': 'false'},
        {'response': 'Carro', 'correct': 'false'},
        {'response': 'Chão', 'correct': 'false'},
        {'response': 'Corpo', 'correct': 'false'}]},
    {'id': 24, 'charade': 'O que é, o que é: tem pescoço, mas não tem cabeça, tem boca, mas não fala?', 'responses': [
        {'response': 'Garrafa', 'correct': 'true'},
        {'response': 'Vaso', 'correct': 'false'},
        {'response': 'Copo', 'correct': 'false'},
        {'response': 'Chaleira', 'correct': 'false'},
        {'response': 'Panela', 'correct': 'false'}]},
    {'id': 25, 'charade': 'O que é, o que é: quanto mais se enche, mais leve fica?', 'responses': [
        {'response': 'Balão', 'correct': 'true'},
        {'response': 'Saco', 'correct': 'false'},
        {'response': 'Mochila', 'correct': 'false'},
        {'response': 'Caixa', 'correct': 'false'},
        {'response': 'Bolsa', 'correct': 'false'}]},
    {'id': 26, 'charade': 'O que é, o que é: tem agulha, mas não costura, tem linha, mas não tricota?', 'responses': [
        {'response': 'Disco', 'correct': 'true'},
        {'response': 'Relógio', 'correct': 'false'},
        {'response': 'Calculadora', 'correct': 'false'},
        {'response': 'Termômetro', 'correct': 'false'},
        {'response': 'Bússola', 'correct': 'false'}]},
    {'id': 27, 'charade': 'O que é, o que é: tem casa, mas não tem porta, tem cama, mas não tem lençol?', 'responses': [
        {'response': 'Caracol', 'correct': 'true'},
        {'response': 'Tartaruga', 'correct': 'false'},
        {'response': 'Concha', 'correct': 'false'},
        {'response': 'Ostra', 'correct': 'false'},
        {'response': 'Lesma', 'correct': 'false'}]},
    {'id': 28, 'charade': 'O que é, o que é: tem asas, mas não voa, tem boca, mas não fala?', 'responses': [
        {'response': 'Bule', 'correct': 'true'},
        {'response': 'Chaleira', 'correct': 'false'},
        {'response': 'Xícara', 'correct': 'false'},
        {'response': 'Caneca', 'correct': 'false'},
        {'response': 'Garrafa', 'correct': 'false'}]},
    {'id': 29, 'charade': 'O que é, o que é: quanto mais se tira, maior fica o buraco?', 'responses': [
        {'response': 'Terra', 'correct': 'true'},
        {'response': 'Areia', 'correct': 'false'},
        {'response': 'Água', 'correct': 'false'},
        {'response': 'Grama', 'correct': 'false'},
        {'response': 'Pedra', 'correct': 'false'}]},
    {'id': 30, 'charade': 'O que é, o que é: tem chapéu, mas não tem cabeça, tem boca, mas não fala?', 'responses': [
        {'response': 'Cogumelo', 'correct': 'true'},
        {'response': 'Árvore', 'correct': 'false'},
        {'response': 'Flor', 'correct': 'false'},
        {'response': 'Abajur', 'correct': 'false'},
        {'response': 'Luminária', 'correct': 'false'}]},
    {'id': 31, 'charade': 'O que é, o que é: tem agulha, mas não costura, tem botão, mas não é roupa?', 'responses': [
        {'response': 'Calculadora', 'correct': 'true'},
        {'response': 'Máquina de costura', 'correct': 'false'},
        {'response': 'Computador', 'correct': 'false'},
        {'response': 'Celular', 'correct': 'false'},
        {'response': 'Tablet', 'correct': 'false'}]},
    {'id': 32, 'charade': 'O que é, o que é: tem cabeça, tem dente, tem barba, não é bicho nem é gente?', 'responses': [
        {'response': 'Alho', 'correct': 'true'},
        {'response': 'Cebola', 'correct': 'false'},
        {'response': 'Milho', 'correct': 'false'},
        {'response': 'Abacaxi', 'correct': 'false'},
        {'response': 'Coco', 'correct': 'false'}]},
    {'id': 33, 'charade': 'O que é, o que é: tem muitas casas, mas não tem parede, tem muitos quartos, mas não tem cama?', 'responses': [
        {'response': 'Colmeia', 'correct': 'true'},
        {'response': 'Prédio', 'correct': 'false'},
        {'response': 'Castelo', 'correct': 'false'},
        {'response': 'Hotel', 'correct': 'false'},
        {'response': 'Condomínio', 'correct': 'false'}]},
    {'id': 34, 'charade': 'O que é, o que é: quanto mais quente está, mais fresco é?', 'responses': [
        {'response': 'Pão', 'correct': 'true'},
        {'response': 'Chá', 'correct': 'false'},
        {'response': 'Café', 'correct': 'false'},
        {'response': 'Sopa', 'correct': 'false'},
        {'response': 'Chocolate quente', 'correct': 'false'}]}
        
        ]

@api.route('/status', methods=['GET'])
def status():
    return 'The API is currently online.', 200

@api.route('/api/charades', methods=['GET'])
def random_charade():
    return jsonify(random.choice(charades))

@api.route('/api/charades/<int:id>', methods=['GET'])
def charade(id):
    if request.method == 'GET':
            
        for charade in charades:
            if charade['id'] == id:
                return jsonify(charade)
