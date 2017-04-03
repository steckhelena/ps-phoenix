def otsus_method(matrix):
    # Retorna um threshold para ser utilizado para se criar a imagem binária pelo método de Otsu. Matrix deve ser uma
    # imagem em escala de cinza. Este método não é tão computacionalmente intensivo

    # Calcula o histograma de intensidades.
    histogram = [0 for _ in range(256)] # inicializa o histograma para o intervalo [0-255]
    for i in range(480):
        for j in range(640):
            histogram[] += 1

    # Número total de pixeis = 640*480, calculado previamente para não gastar processamento com isso.
    total = 307200

    soma = 0.0
    for i in range(256):
        soma += i*histogram[i]

    sumB = 0.0
    wB = 0
    wF = 0

    varMax = 0.0
    threshold = 0

    for i in range(256):
        wB += histogram[i] # Peso do background da imagem.
        if wB == 0:
            continue

        wF = total - wB # Peso do foreground da imagem.
        if wF == 0:
            break

        sumB += i*histogram[i]

        mB = sumB/wB # Media do background
        mF = (soma - sumB)/wF # Média do foreground

        # Calcula a variância entre classes.
        varBetween = wB*wF*(mB-mF)*(mB-mF)

        # Checa se o novo máximo foi encontrado:
        if varBetween > varMax:
            varMax = varBetween
            threshold = i

    return threshold


def max_point(ponto1, ponto2):
    # Retorna o ponto de maior área entre os dois pontos fornecidos.
    if (ponto1[2]*ponto1[3] > ponto2[2]*ponto2[3]):
        return ponto1
    else:
        return ponto2

def max_blob(matriz):
    # Assume-se que a imagem não tem um céu ou outro objeto branco grande pois para filtrar isto e escolher
    # corretamente a base seria necessária uma análise de cada um dos pontos retornados, considerando-se suas posições
    # e seus tamanhos. Um algorítimo simples que faz isso é um que analisa a altura do ponto e o compara com suas
    # dimensões, checando por exemplo se a largura é maior que a altura para a identificação do céu.

    points = blob(matriz) # Gera uma lista de todos os pontos brancos na imagem tratada
    retpoint = (0, 0, 0, 0) # Cria um ponto pequeno para se iniciar a busca pelo maior ponto
    for point in points:
        retpoint = max_point(point, retpoint)

    return retpoint

def main():
    #lendo a imagem de um dispositivo
    M = read_image()

    #você tem que dar o valor correto às duas variáveis abaixo.
    #cone_x e cone_y são os pontos x e y, respectivamente, do centro
    #do retângulo que encobre completamente o cone.
    cone_x, cone_y = 0, 0

    #bônus: dê valor corretamente à variável abaixo
    hor_angle = 0.0

    #----COMPLETE O CÓDIGO AQUI-----

    # Primeiramente convertemos a imagem para uma matriz em escala de cinza para facilitar o seu manuseamento.
    MGS = grayscale(M)

    # Agora suavizamos a imagem com a função de gaussian_blur para suavizar os pequenos detalhes.
    MB = gaussian_blur(binary_matrix)

    # Agora decidimos os valores para se utilizar na função threshold
    threshold = otsus_method(MB)

    # Agora transformamos a matriz hsl em uma matriz binária  para a área de interesse ser facilmente encontrada.
    binary_matrix = threshold(MB, threshold)

    # Agora extraimos o retangulo alvo da imagem final
    retangulo = max_blob(binary_matrix)

    # Agora calculamos o centro do retangulo maior
    cone_x = (retangulo[0] + retangulo[2]//2)
    cone_y = (retangulo[1] + retangulo[3]//2)

    # Agora calculamos a distância do centro do retângulo ao centro da imagem e então multiplicamos pela constante
    # calculada como o valor de angulo/pixel da imagem:
    # Como 75graus correspondem à 1,309 radianos e como a imagem tem dimensão horizontal de 640pixels então podemos
    # realizar a seguinte conta 1,309/640 = 0.0020453125 que é a constante citada anteriormente.
    K = 0.0020453125
    hor_angle = abs(K*(cone_x - 319))

    #-------------------------------

if __name__ == "__main__":
    main()
