import json
import csv
import sys
import time

def carregar_automato(arquivo_aut):
    with open(arquivo_aut, 'r') as f:
        return json.load(f)

def carregar_testes(arquivo_testes):
    with open(arquivo_testes, 'r') as f:
        return [linha.strip().split(';') for linha in f.readlines()]

def simular_automato(automato, palavra):
    estado_atual = automato['initial']
    for simbolo in palavra:
        transicao = next((t for t in automato['transitions'] if t['from'] == estado_atual and t['read'] == simbolo), None)
        if transicao:
            estado_atual = transicao['to']
        else:
            return 0  # rejeita
    return 1 if estado_atual in automato['final'] else 0  # aceita ou rejeita

def salvar_resultados(arquivo_saida, resultados):
    with open(arquivo_saida, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['palavra de entrada', 'resultado esperado', 'resultado obtido', 'tempo'])
        for resultado in resultados:
            writer.writerow(resultado)

def main():
    if len(sys.argv) != 4:
        print("Uso: python simulador.py arquivo_do_automato.aut arquivo_de_testes.in arquivo_de_saida.out")
        sys.exit(1)

    arquivo_aut = sys.argv[1]
    arquivo_testes = sys.argv[2]
    arquivo_saida = sys.argv[3]

    automato = carregar_automato(arquivo_aut)
    testes = carregar_testes(arquivo_testes)

    resultados = []

    for palavra, resultado_esperado in testes:
        inicio = time.time()
        resultado_obtido = simular_automato(automato, palavra)
        tempo = time.time() - inicio
        resultados.append([palavra, resultado_esperado, resultado_obtido, f"{tempo:.6f}"])

    salvar_resultados(arquivo_saida, resultados)

if __name__ == "__main__":
    main()
