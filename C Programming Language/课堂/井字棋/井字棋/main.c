//
//  main.c
//  井字棋
//
//  Created by 张佳伟 on 2025/11/19.
//

#include <stdio.h>

int main()
{
    int winner = 0;
    int board [3][3] = {
        {1,2,3},
        {2,1,2},
        {1,0,0},
    };
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
            if (board[i][0] == 1) {
                winner = 1;
            }else{
                winner = 2;
            }
            break;
        }
    }
    
    for (int j = 0; j < 3; j++) {
        if (board[0][j] == board[1][j] && board[1][j] == board[2][j]) {
            if (board[0][j] == 1) {
                winner = 1;
            }else{
                winner = 2;
            }
            break;
        }
    }
}
