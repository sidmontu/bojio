/***********************************************************************************
 * MIT License
 *
 * Copyright (c) [2021] [Siddhartha (sidmontu@gmail.com)]
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
************************************************************************************/


#include "include/config.h"
#include "include/utils.h"

std::vector<std::string> move_gen(BoardState* board_state, bool white_turn) {
    std::vector<std::string> legal_moves;

    // pawn move forward one
    if (white_turn) {
        for (bitboard_t pawn : board_state->white_pawns) {
            printf("0x%" PRIu64 "\n", pawn);
        }
    }

    return legal_moves;
}

int main(int argc, char** argv) {
    BoardState bs = init_standard_game();
    print_board_state(&bs);

    std::vector<std::string> legal_moves = move_gen(&bs, true);

    // print legal moves
    for (std::string move : legal_moves) printf("Legal move: %s\n", move.c_str());

    return 0;
}
