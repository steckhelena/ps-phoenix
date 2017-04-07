/*
* placa_externa.c
*
* Autor: Marco Antonio Steck Filho
*/

#include<stdlib.h>

#define LEFT_STICK_Y 1
#define RIGHT_STICK_X 4
#define BUTTON_X 1
#define BUTTON_R2 1
#define BUTTON_L2 1

#define DEADZONE 4096 // Valor que deve ser calibrado dependendo do estado do controle.

// Mapeia um valor no range [min-max] para um no novo range [nmin-nmax]
int map(int value, int min, int max, int nmin, int nmax) {
    return (value - min) * (nmax - nmin) / (max - min) + nmin;
}

// Retorna o sinal de um inteiro.
int sign(int x) {
    return (x > 0) - (x < 0);
}

int main(int argc, char const *argv[]) {
    int left_stick_y, right_stick_x; // Salva a inclinacao de cada analogico.
    unsigned char left_y_sign, right_x_sign; // Guarda os sinais dos analogicos.
    int x_pressed, r2_pressed, l2_pressed; // Monitoram o estado dos botoes importantes.

    // Primeiramente inicializamos todas as configuracoes de baixo nivel para que possamos invocar todas.
    configuraPerifericosPlacaExterna();

    // Inicializamos o loop de execucao principal da placa.
    while (1) {
        // Le os valores dos analogicos
        left_stick_y = leAnalogicoControle(LEFT_STICK_Y);
        right_stick_x = leAnalogicoControle(RIGHT_STICK_X);

        // Aplica a deadzone nesses analogicos para nao termos problema de imprecisao quando o analogico estiver em
        // repouso.
        left_stick_y = (abs(left_stick_y) > DEADZONE) ? left_stick_y : 0;
        right_stick_x = (abs(right_stick_x) > DEADZONE) ? right_stick_x : 0;

        // Pega os sinais antes de mapear para os novos valores.
        left_y_sign = sign(left_stick_y);
        right_x_sign = sign(right_stick_x);

        // Mapeia cada variavel para o tamanho de um byte para nao ter overflow.
        left_stick_y = map(left_stick_y, -2147483648, 2147483647, 0, 255);
        right_stick_x = map(right_stick_x, -2147483648, 2147483647, 0, 255);

        // Le os valores dos botoes que controlam o robo.
        x_pressed = leBotaoControle(BUTTON_X);
        r2_pressed = leBotaoControle(BUTTON_R2);
        l2_pressed = leBotaoControle(BUTTON_L2);

        // Envia os dados lidos para a placa interna.
        enviaDados(7, left_stick_y, left_y_sign, right_stick_x, right_x_sign, x_pressed, r2_pressed, l2_pressed);
    }

    return 0;
}
