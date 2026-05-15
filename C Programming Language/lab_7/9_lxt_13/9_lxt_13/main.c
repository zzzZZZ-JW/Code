//
//  main.c
//  9_lxt_13
//
//  Created by 张佳伟 on 2025/11/27.
//

#include <stdio.h>

int evaluate_position(char board[8][8]){
    int white_score = 0;
    int black_score = 0;
    
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            char piece = board[i][j];
            
            switch (piece) {
                case 'Q': white_score += 9;
                    break;
                case 'R': white_score += 5;
                    break;
                case 'B': white_score += 3;
                    break;
                case 'N': white_score += 3;
                    break;
                case 'P': white_score += 1;
                    break;
            }
            
            switch (piece) {
                case 'q': black_score += 9;
                    break;
                case 'r': black_score += 5;
                    break;
                case 'b': black_score += 3;
                    break;
                case 'n': black_score += 3;
                    break;
                case 'p': black_score += 1;
                    break;
            }
        }
    }
    
    return white_score - black_score;
}
